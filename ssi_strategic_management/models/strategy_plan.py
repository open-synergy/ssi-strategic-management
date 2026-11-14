# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression

from odoo.addons.ssi_decorator import ssi_decorator


class StrategyPlan(models.Model):
    """Represents a strategic plan of the company.

    A plan is the parent document of every objective, KPI and initiative.
    It moves through the standard transaction lifecycle: ``draft`` ->
    ``confirm`` (approval) -> ``open`` -> ``done``, with ``cancel``
    available from ``draft``, ``confirm`` and ``open``.

    Plans can be nested: a long term plan can own yearly plans, which in
    turn own quarterly plans. The period of a sub-plan must stay within
    the period of its parent, and a sub-plan can only be started after
    its parent plan is in progress.
    """

    _name = "strategy_plan"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_open",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
        "mixin.transaction_date_duration",
    ]
    _description = "Strategy Plan"

    # Multiple approval attributes. The final approval does NOT start the
    # plan: the user starts it explicitly with the Start button, which is
    # where the parent plan pre-check is evaluated.
    _approval_from_state = "draft"
    _approval_to_state = "confirm"
    _approval_state = "confirm"
    _after_approved_method = False

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True
    _automatically_insert_open_policy_fields = True
    _automatically_insert_open_button = True
    _automatically_insert_done_policy_fields = True
    _automatically_insert_done_button = True

    _statusbar_visible_label = "draft,confirm,open,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "open_ok",
        "done_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "action_open",
        "action_done",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_open",
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "open"

    title = fields.Char(
        string="Title",
        required=True,
        tracking=True,
        help="Short title that identifies this document. It is shown "
        "next to the document number in the document name.",
    )

    type_id = fields.Many2one(
        string="Plan Type",
        comodel_name="strategy_plan_type",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Plan type that fixes the methodology of this plan.",
    )
    parent_id = fields.Many2one(
        string="Parent Plan",
        comodel_name="strategy_plan",
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Plan that contains this plan, e.g. the yearly plan of a "
        "quarterly plan.",
    )
    child_ids = fields.One2many(
        string="Sub-Plans",
        comodel_name="strategy_plan",
        inverse_name="parent_id",
        readonly=True,
        help="Plans that are contained in this plan.",
    )
    objective_ids = fields.One2many(
        string="Objectives",
        comodel_name="strategy_objective",
        inverse_name="plan_id",
        readonly=True,
        help="Strategic objectives that belong to this plan.",
    )
    initiative_ids = fields.One2many(
        string="Initiatives",
        comodel_name="strategy_initiative",
        inverse_name="plan_id",
        readonly=True,
        help="Strategic initiatives that belong to this plan.",
    )
    vision = fields.Text(
        string="Vision",
        help="Vision statement that this plan works toward.",
    )
    mission = fields.Text(
        string="Mission",
        help="Mission statement that this plan carries out.",
    )
    score = fields.Float(
        string="Score",
        compute="_compute_score",
        store=True,
        compute_sudo=True,
        help="Weighted average of the scores of the top objectives of "
        "this plan, using their weights. A simple average when the "
        "weights add up to zero, 0 without objectives.",
    )
    score_category_range_id = fields.Many2one(
        string="Score Category",
        comodel_name="strategy_score_category.range",
        compute="_compute_score_category_range_id",
        store=True,
        compute_sudo=True,
        help="Range of the score category of the plan type that contains "
        "the score of this plan.",
    )

    def _get_top_objectives(self):
        """Return the top objectives of this plan.

        A top objective has no parent objective or a parent objective in
        another plan. Cancelled objectives are left out.

        :return: recordset of top objectives of the plan
        """
        self.ensure_one()
        return self.objective_ids.filtered(
            lambda r: r.state != "cancel"
            and (not r.parent_id or r.parent_id.plan_id != self)
        )

    @api.depends(
        "objective_ids.score",
        "objective_ids.weight",
        "objective_ids.state",
        "objective_ids.parent_id",
    )
    def _compute_score(self):
        """Average the scores of the top objectives of the plan.

        The average is weighted by the objective weights, simple when
        the weights add up to zero, and 0 without top objectives.
        """
        for record in self:
            result = 0.0
            objectives = record._get_top_objectives()
            if objectives:
                total_weight = sum(objectives.mapped("weight"))
                if total_weight:
                    result = sum(o.score * o.weight for o in objectives) / total_weight
                else:
                    result = sum(objectives.mapped("score")) / len(objectives)
            record.score = result

    @api.depends(
        "score",
        "type_id.score_category_id.range_ids.min_value",
        "type_id.score_category_id.range_ids.max_value",
    )
    def _compute_score_category_range_id(self):
        """Pick the range of the plan type score category for the score.

        Empty when the plan type has no category or no range matches.
        """
        for record in self:
            result = False
            category = record.type_id.score_category_id
            matching = category.range_ids.filtered(
                lambda r, score=record.score: r.min_value <= score <= r.max_value
            )
            if matching:
                result = matching[0]
            record.score_category_range_id = result

    @api.constrains("parent_id")
    def _check_parent_recursion(self):
        """Reject a parent plan hierarchy that contains a cycle.

        :raises ValidationError: when a plan is its own ancestor
        """
        if not self._check_recursion():
            error_message = """
Context: Set parent plan
Problem: A plan cannot be its own ancestor.
Solution: Choose a parent plan that is not a sub-plan of this plan
"""
            raise ValidationError(_(error_message))

    @api.constrains("parent_id", "date_start", "date_end")
    def _check_period_within_parent(self):
        """Reject sub-plans whose period leaves the period of the parent.

        Both the changed plans and their sub-plans are checked, so that
        shrinking the period of a parent is rejected when a sub-plan
        would fall outside of it.

        :raises ValidationError: when the period condition fails
        """
        for plan in (self | self.mapped("child_ids")).sudo():
            if not plan._check_period_within_parent_condition():
                error_message = """
Context: Set plan period
Database ID: %s
Problem: Plan period must be within its parent plan period.
Solution: Change the plan period to fit the parent plan period
""" % (
                    plan.id,
                )
                raise ValidationError(_(error_message))

    def _check_period_within_parent_condition(self):
        """Tell whether the period fits in the period of the parent.

        Extension point: override to relax or tighten the rule.

        :return: True when there is no parent or the period is inside
            the parent period
        """
        self.ensure_one()
        parent = self.parent_id
        if not parent:
            return True
        if not (self.date_start and self.date_end):
            return True
        if not (parent.date_start and parent.date_end):
            return True
        return self.date_start >= parent.date_start and self.date_end <= parent.date_end

    @ssi_decorator.pre_open_check()
    def _10_check_parent_plan_open(self):
        """Reject starting a sub-plan before its parent plan is open.

        Runs in the ``pre_open_check`` slot, so the plan stays untouched
        when the check fails.

        :raises UserError: when the parent plan is not in progress
        """
        self.ensure_one()
        if self.parent_id and self.parent_id.state != "open":
            error_message = """
Context: Start plan
Database ID: %s
Problem: The parent plan must be in progress first.
Solution: Start the parent plan before starting this plan
""" % (
                self.id,
            )
            raise UserError(_(error_message))

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch

    @api.model
    def _get_policy_field(self):
        res = super()._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "reject_ok",
            "restart_approval_ok",
            "open_ok",
            "done_ok",
            "cancel_ok",
            "restart_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @api.depends("name", "title")
    def _compute_display_name(self):
        """Recompute the stored display name.

        The depends cover the document number and the title, so the
        stored name follows a title change.
        """
        super()._compute_display_name()

    def name_get(self):
        """Return ``number - title``, or the title for unnumbered records.

        :return: list of ``(id, display name)`` tuples
        :rtype: list
        """
        result = []
        for record in self:
            title = record.title or ""
            if record.name and record.name != "/":
                name = "%s - %s" % (record.name, title) if title else record.name
            else:
                name = title or "*%s" % record.id
            result.append((record.id, name))
        return result

    @api.model
    def _name_search(
        self, name="", args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        """Search by document number or by title.

        :param name: text typed by the user
        :param args: extra domain
        :param operator: comparison operator requested by the caller
        :param limit: maximum number of records
        :param name_get_uid: user used to resolve the names
        :return: ids of the matching records
        """
        args = list(args or [])
        domain = []
        if name:
            connector = "&" if operator in expression.NEGATIVE_TERM_OPERATORS else "|"
            domain = [connector, ("name", operator, name), ("title", operator, name)]
        return self._search(
            expression.AND([domain, args]),
            limit=limit,
            access_rights_uid=name_get_uid,
        )
