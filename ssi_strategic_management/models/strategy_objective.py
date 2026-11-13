# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare

from odoo.addons.ssi_decorator import ssi_decorator


class StrategyObjective(models.Model):
    """Represents a strategic objective of a strategy plan.

    An objective belongs to a plan and to an organization unit (a
    department, optionally narrowed down to one employee when the plan
    type cascades down to employees). Objectives are cascaded from a
    parent objective to child objectives. A child either contributes to
    the parent (the weights of the contributing children must add up to
    100%) or only aligns with it, which is the way an OKR objective
    aligns with a Balanced Scorecard objective.

    It moves through a simple lifecycle without approval: ``draft`` ->
    ``open`` -> ``done``, with ``cancel`` available from ``draft`` and
    ``open``.
    """

    _name = "strategy_objective"
    _inherit = [
        "mixin.transaction_open",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
    ]
    _description = "Strategy Objective"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True

    # Attributes related to add element on form view automatically
    _automatically_insert_open_policy_fields = True
    _automatically_insert_open_button = True
    _automatically_insert_done_policy_fields = True
    _automatically_insert_done_button = True

    _statusbar_visible_label = "draft,open,done"

    _policy_field_order = [
        "open_ok",
        "done_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_open",
        "action_done",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_open",
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "open"

    plan_id = fields.Many2one(
        string="Plan",
        comodel_name="strategy_plan",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Strategy plan that owns this objective.",
    )
    perspective_id = fields.Many2one(
        string="Perspective",
        comodel_name="strategy_perspective",
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Balanced Scorecard perspective of this objective. Required "
        "for plans that follow the Balanced Scorecard methodology.",
    )
    department_id = fields.Many2one(
        string="Department",
        comodel_name="hr.department",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Department that this objective is cascaded to.",
    )
    employee_id = fields.Many2one(
        string="Employee",
        comodel_name="hr.employee",
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Employee that this objective is cascaded to. Only plans "
        "whose type cascades down to employees allow it, and the employee "
        "must belong to the department of the objective.",
    )
    owner_id = fields.Many2one(
        string="Owner",
        comodel_name="hr.employee",
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Employee who is accountable for achieving this objective.",
    )
    parent_id = fields.Many2one(
        string="Parent Objective",
        comodel_name="strategy_objective",
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Objective that this objective is cascaded from. It must "
        "belong to the same plan or to an ancestor plan.",
    )
    child_ids = fields.One2many(
        string="Child Objectives",
        comodel_name="strategy_objective",
        inverse_name="parent_id",
        readonly=True,
        help="Objectives that are cascaded from this objective.",
    )
    cascade_method = fields.Selection(
        string="Cascade Method",
        selection=[
            ("direct", "Direct"),
            ("contributive", "Contributive"),
        ],
        required=True,
        default="contributive",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="How this objective is derived from its parent: Direct = "
        "taken over as is, Contributive = a share of the parent "
        "objective.",
    )
    weight = fields.Float(
        string="Contribution Weight (%)",
        default=0.0,
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Share of the parent objective that this objective carries. "
        "The weights of the contributing children of one parent must add "
        "up to 100%.",
    )
    influence_ids = fields.Many2many(
        string="Influences",
        comodel_name="strategy_objective",
        relation="rel_strategy_objective_2_influence",
        column1="objective_id",
        column2="influenced_objective_id",
        help="Objectives that are influenced by this objective (cause and "
        "effect links of the strategy map).",
    )
    objective_type = fields.Selection(
        string="Objective Type",
        related="plan_id.type_id.methodology",
        store=True,
        compute_sudo=True,
        help="Methodology of the plan type of the plan: Balanced " "Scorecard or OKR.",
    )
    contribute_to_parent = fields.Boolean(
        string="Contribute to Parent",
        compute="_compute_contribute_to_parent",
        store=True,
        readonly=False,
        help="Whether the score of this objective contributes to its "
        "parent. Balanced Scorecard objectives contribute by default, "
        "OKR objectives only align with their parent.",
    )

    @api.depends("objective_type")
    def _compute_contribute_to_parent(self):
        """Default the contribution flag from the objective type.

        Balanced Scorecard objectives contribute to their parent, OKR
        objectives do not. The value stays editable.
        """
        for record in self:
            result = record.objective_type == "bsc"
            record.contribute_to_parent = result

    @api.constrains("plan_id", "perspective_id")
    def _check_perspective_required(self):
        """Require a perspective on Balanced Scorecard objectives.

        :raises ValidationError: when the condition method returns False
        """
        for record in self.sudo():
            if not record._check_perspective_required_condition():
                error_message = """
Context: Create or update strategy objective
Database ID: %s
Problem: Balanced Scorecard objectives require a perspective.
Solution: Select a perspective for the objective
""" % (
                    record.id,
                )
                raise ValidationError(_(error_message))

    def _check_perspective_required_condition(self):
        """Tell whether the perspective rule is satisfied.

        Extension point: override to relax or tighten the rule.

        :return: False only for a Balanced Scorecard objective without a
            perspective
        """
        self.ensure_one()
        methodology = self.plan_id.type_id.methodology
        return not (methodology == "bsc" and not self.perspective_id)

    @api.constrains("plan_id", "employee_id")
    def _check_employee_cascade_level(self):
        """Reject employees on plans that only cascade to departments.

        :raises ValidationError: when the condition method returns False
        """
        for record in self.sudo():
            if not record._check_employee_cascade_level_condition():
                error_message = """
Context: Create or update strategy objective
Database ID: %s
Problem: This plan type does not allow cascading objectives to employees.
Solution: Remove the employee or use a plan type that cascades to employees
""" % (
                    record.id,
                )
                raise ValidationError(_(error_message))

    def _check_employee_cascade_level_condition(self):
        """Tell whether the plan type allows the chosen employee.

        Extension point: override to relax or tighten the rule.

        :return: True when there is no employee or the plan type
            cascades down to employees
        """
        self.ensure_one()
        if not self.employee_id:
            return True
        return self.plan_id.type_id.cascade_level == "employee"

    @api.constrains("department_id", "employee_id")
    def _check_employee_department(self):
        """Reject employees outside the department of the objective.

        :raises ValidationError: when the condition method returns False
        """
        for record in self.sudo():
            if not record._check_employee_department_condition():
                error_message = """
Context: Create or update strategy objective
Database ID: %s
Problem: The employee must belong to the objective department.
Solution: Choose an employee of the objective department
""" % (
                    record.id,
                )
                raise ValidationError(_(error_message))

    def _check_employee_department_condition(self):
        """Tell whether the employee belongs to the objective department.

        Extension point: override to relax or tighten the rule.

        :return: True when there is no employee or the employee works
            in the department of the objective
        """
        self.ensure_one()
        if not self.employee_id:
            return True
        return self.employee_id.department_id == self.department_id

    @api.constrains("parent_id")
    def _check_parent_recursion(self):
        """Reject a parent objective hierarchy that contains a cycle.

        :raises ValidationError: when an objective is its own ancestor
        """
        if not self._check_recursion():
            error_message = """
Context: Set parent objective
Problem: An objective cannot be its own ancestor.
Solution: Choose a parent objective that is not a child of this objective
"""
            raise ValidationError(_(error_message))

    @api.constrains("plan_id", "parent_id")
    def _check_parent_plan(self):
        """Reject parent objectives from an unrelated plan.

        :raises ValidationError: when the condition method returns False
        """
        for record in self.sudo():
            if not record._check_parent_plan_condition():
                error_message = """
Context: Set parent objective
Database ID: %s
Problem: The parent objective must belong to the same plan or an ancestor plan.
Solution: Choose a parent objective of the same plan or of a parent plan
""" % (
                    record.id,
                )
                raise ValidationError(_(error_message))

    def _check_parent_plan_condition(self):
        """Tell whether the parent objective plan is the plan or above it.

        Extension point: override to relax or tighten the rule.

        :return: True when there is no parent objective or its plan is
            the plan of this objective or one of the ancestor plans
        """
        self.ensure_one()
        if not self.parent_id:
            return True
        allowed_plan = self.plan_id
        while allowed_plan:
            if allowed_plan == self.parent_id.plan_id:
                return True
            allowed_plan = allowed_plan.parent_id
        return False

    @ssi_decorator.pre_open_check()
    def _10_check_plan_open(self):
        """Reject starting an objective before its plan is in progress.

        Runs in the ``pre_open_check`` slot, so the objective stays
        untouched when the check fails.

        :raises UserError: when the plan is not in progress
        """
        self.ensure_one()
        if self.plan_id.state != "open":
            error_message = """
Context: Start objective
Database ID: %s
Problem: The plan must be in progress before opening objectives.
Solution: Start the plan before starting this objective
""" % (
                self.id,
            )
            raise UserError(_(error_message))

    @ssi_decorator.pre_open_check()
    def _20_check_child_weight(self):
        """Reject starting a parent whose contributing weights are not 100%.

        Runs in the ``pre_open_check`` slot, after the plan check.

        :raises UserError: when the total weight of the contributing
            child objectives differs from 100%
        """
        self.ensure_one()
        contributing = self.child_ids.filtered(lambda r: r.contribute_to_parent)
        if not contributing:
            return
        total_weight = sum(contributing.mapped("weight"))
        if float_compare(total_weight, 100.0, precision_digits=2) != 0:
            error_message = """
Context: Start objective
Database ID: %s
Problem: Total weight of contributing child objectives must be 100%%.
Solution: Change the weights of the child objectives so that they add up to 100%%
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
            "open_ok",
            "done_ok",
            "cancel_ok",
            "restart_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res
