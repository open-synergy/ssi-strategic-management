# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare
from odoo.tools.safe_eval import safe_eval

from odoo.addons.ssi_decorator import ssi_decorator


class StrategyInitiative(models.Model):
    """Represents a strategic initiative of a strategy plan.

    An initiative is a project that closes a gap and is meant to move
    one or more objectives and KPIs of the plan. It moves through the
    standard transaction lifecycle: ``draft`` -> ``confirm`` (approval)
    -> ``open`` -> ``done``, with ``cancel`` available from ``draft``,
    ``confirm`` and ``open`` and ``terminate`` available from ``open``.

    The progress of an initiative is entered manually, derived from the
    weighted milestones, or computed by Python code. While the
    initiative is in progress its health compares the progress with
    the share of the period that has elapsed. Other modules can add
    their own sources of gap by extending ``_get_health_gap``.
    """

    _name = "strategy_initiative"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_open",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
        "mixin.transaction_terminate",
        "mixin.transaction_date_duration",
        "mixin.localdict",
    ]
    _description = "Strategy Initiative"

    # Multiple approval attributes. The final approval does NOT start the
    # initiative: the user starts it explicitly with the Start button,
    # which is where the pre-checks are evaluated.
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
        "terminate_ok",
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
        "%(ssi_transaction_terminate_mixin.base_select_terminate_reason_action)d",
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
        "dom_terminate",
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
        help="Strategy plan that owns this initiative.",
    )
    objective_ids = fields.Many2many(
        string="Objectives",
        comodel_name="strategy_objective",
        relation="rel_strategy_initiative_2_objective",
        column1="initiative_id",
        column2="objective_id",
        domain="[('plan_id', '=', plan_id)]",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Objectives of the plan that this initiative is meant to move.",
    )
    kpi_ids = fields.Many2many(
        string="KPIs",
        comodel_name="strategy_kpi",
        relation="rel_strategy_initiative_2_kpi",
        column1="initiative_id",
        column2="kpi_id",
        domain="[('objective_id', 'in', objective_ids)]",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="KPIs of the selected objectives that this initiative is "
        "meant to move.",
    )
    owner_id = fields.Many2one(
        string="Owner",
        comodel_name="hr.employee",
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Employee who is accountable for this initiative.",
    )
    department_id = fields.Many2one(
        string="Department",
        comodel_name="hr.department",
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Department that carries out this initiative.",
    )
    progress_method = fields.Selection(
        string="Progress Method",
        selection=[
            ("manual", "Manual"),
            ("milestone", "Milestones"),
            ("python", "Python Code"),
        ],
        required=True,
        default="milestone",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="How the progress is determined: Manual = entered by hand, "
        "Milestones = weight of the completed milestones, Python Code = "
        "computed by the code below.",
    )
    manual_progress = fields.Float(
        string="Manual Progress (%)",
        default=0.0,
        readonly=True,
        states={
            "draft": [("readonly", False)],
            "open": [("readonly", False)],
        },
        help="Progress entered by hand. Used when the progress method is " "Manual.",
    )
    python_code = fields.Text(
        string="Progress Code",
        readonly=True,
        states={
            "draft": [("readonly", False)],
            "open": [("readonly", False)],
        },
        help="Python code that assigns the progress to ``result``. Used "
        "when the progress method is Python Code. Available variables: "
        "``document`` (this initiative), ``env``, ``time``, ``datetime`` "
        "and ``dateutil``.",
    )
    python_progress = fields.Float(
        string="Computed Progress (%)",
        default=0.0,
        readonly=True,
        copy=False,
        help="Progress computed by the Compute Progress button from the "
        "progress code.",
    )
    milestone_ids = fields.One2many(
        string="Milestones",
        comodel_name="strategy_initiative.milestone",
        inverse_name="initiative_id",
        readonly=True,
        states={
            "draft": [("readonly", False)],
            "open": [("readonly", False)],
        },
        help="Milestones that make up the initiative.",
    )
    progress = fields.Float(
        string="Progress (%)",
        compute="_compute_progress",
        store=True,
        compute_sudo=True,
        help="Progress of the initiative, from 0 to 100, according to "
        "the progress method.",
    )
    health = fields.Selection(
        string="Health",
        selection=[
            ("green", "On Track"),
            ("yellow", "At Risk"),
            ("red", "Off Track"),
        ],
        compute="_compute_health",
        store=True,
        compute_sudo=True,
        help="Health of the initiative while it is in progress: the gap "
        "between the elapsed share of the period and the progress is "
        "compared with the thresholds of the plan type.",
    )

    @api.depends(
        "progress_method",
        "manual_progress",
        "python_progress",
        "milestone_ids.weight",
        "milestone_ids.is_done",
    )
    def _compute_progress(self):
        """Compute the progress according to the progress method.

        Manual takes the entered figure, Python Code takes the figure
        computed by the button, and Milestones takes the share of the
        weight of the completed milestones, or 0 when no milestone has
        any weight.
        """
        for record in self:
            result = 0.0
            if record.progress_method == "manual":
                result = record.manual_progress
            elif record.progress_method == "python":
                result = record.python_progress
            else:
                total = sum(record.milestone_ids.mapped("weight"))
                done = sum(record.milestone_ids.filtered("is_done").mapped("weight"))
                if total:
                    result = done * 100.0 / total
            record.progress = result

    @api.depends(
        "state",
        "progress",
        "date_start",
        "date_end",
        "plan_id.type_id.health_yellow_threshold",
        "plan_id.type_id.health_red_threshold",
    )
    def _compute_health(self):
        """Compute the health of the initiatives that are in progress.

        The health stays empty outside the ``open`` state. Otherwise
        the gap returned by ``_get_health_gap`` is compared with the
        thresholds of the plan type: up to the at-risk threshold the
        initiative is on track, up to the off-track threshold it is at
        risk, and beyond it is off track.

        The elapsed share of the period changes with the date, so the
        daily cron recomputes the health of the running initiatives.
        """
        for record in self:
            result = False
            if record.state == "open":
                gap = record._get_health_gap()
                plan_type = record.plan_id.type_id
                if gap <= plan_type.health_yellow_threshold:
                    result = "green"
                elif gap <= plan_type.health_red_threshold:
                    result = "yellow"
                else:
                    result = "red"
            record.health = result

    def _get_expected_progress(self):
        """Tell the share of the period that has elapsed today.

        :return: percentage from 0 to 100; a period that has not
            started gives 0 and a period that has ended gives 100
        """
        self.ensure_one()
        today = fields.Date.context_today(self)
        total_days = max((self.date_end - self.date_start).days, 1)
        elapsed_days = (today - self.date_start).days
        return max(0.0, min(100.0, elapsed_days * 100.0 / total_days))

    def _get_health_gap(self):
        """Tell how far the initiative is behind where it should be.

        Extension point: other modules extend it with their own source
        of gap, for example budget absorption, and return the largest
        gap.

        :return: the expected progress minus the actual progress, in
            percentage points; negative when the initiative is ahead
        """
        self.ensure_one()
        return self._get_expected_progress() - self.progress

    def action_compute_progress(self):
        """Compute the progress with the Python code of the initiative.

        The code assigns the figure to ``result``. The figure is stored
        in ``python_progress`` and used when the progress method is
        Python Code.

        :raises UserError: when the code fails
        """
        for record in self:
            localdict = record._get_default_localdict()
            localdict["result"] = 0.0
            try:
                safe_eval(record.python_code or "", localdict, mode="exec", nocopy=True)
                result = float(localdict["result"] or 0.0)
            except Exception as error:  # pylint: disable=broad-except
                error_message = """
Context: Compute initiative progress
Database ID: %s
Problem: Error evaluating progress code: %s
Solution: Correct the progress code of the initiative
""" % (
                    record.id,
                    error,
                )
                raise UserError(_(error_message))
            record.python_progress = result

    @api.model
    def _cron_update_health(self):
        """Recompute the health of the initiatives that are in progress.

        The elapsed share of the period moves every day while none of
        the stored dependencies changes, so the health is recomputed
        explicitly.
        """
        initiatives = self.search([("state", "=", "open")])
        self.env.add_to_compute(self._fields["health"], initiatives)
        self.recompute(["health"])

    @ssi_decorator.pre_open_check()
    def _10_check_plan_open(self):
        """Reject starting an initiative before its plan is in progress.

        Runs in the ``pre_open_check`` slot, so the initiative stays
        untouched when the check fails.

        :raises UserError: when the plan is not in progress
        """
        self.ensure_one()
        if self.plan_id.state != "open":
            error_message = """
Context: Start initiative
Database ID: %s
Problem: The plan must be in progress before starting initiatives.
Solution: Start the plan before starting this initiative
""" % (
                self.id,
            )
            raise UserError(_(error_message))

    @ssi_decorator.pre_confirm_check()
    def _10_check_milestone_weight(self):
        """Reject confirming a milestone based initiative with wrong weights.

        Runs in the ``pre_confirm_check`` slot, so the initiative stays
        a draft and its milestones can still be corrected. Initiatives
        that do not use milestones pass.

        :raises UserError: when the total weight of the milestones
            differs from 100%
        """
        self.ensure_one()
        self._check_total_milestone_weight("Confirm initiative", " before confirming")

    @ssi_decorator.pre_open_check()
    def _20_check_milestone_weight(self):
        """Reject starting a milestone based initiative with wrong weights.

        Runs in the ``pre_open_check`` slot, after the plan check.
        Initiatives that do not use milestones pass.

        :raises UserError: when the total weight of the milestones
            differs from 100%
        """
        self.ensure_one()
        self._check_total_milestone_weight("Start initiative", "")

    def _check_total_milestone_weight(self, context_label, solution_suffix):
        """Raise when milestone weights of this initiative do not total 100.

        :param context_label: text shown on the ``Context`` line
        :param solution_suffix: text appended to the ``Solution`` line
        :raises UserError: when the progress method is milestone and
            the total weight differs from 100%
        """
        self.ensure_one()
        if self.progress_method != "milestone":
            return
        total_weight = sum(self.milestone_ids.mapped("weight"))
        if float_compare(total_weight, 100.0, precision_digits=2) != 0:
            error_message = """
Context: %s
Database ID: %s
Problem: Total milestone weight must be 100%%.
Solution: Change the weights of the milestones so that they add up to 100%%%s
""" % (
                context_label,
                self.id,
                solution_suffix,
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
            "terminate_ok",
            "restart_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res
