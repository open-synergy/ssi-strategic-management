# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from odoo.addons.ssi_decorator import ssi_decorator


class StrategyReview(models.Model):
    """Represents a periodic review of a strategy plan.

    A review freezes the scores of a plan for a period, optionally for
    one department only. Taking a snapshot copies the score of every
    objective, the target, the realization and the score of every KPI
    target that overlaps the period, and the progress and health of
    every initiative, together with the score of the plan. The copies
    stay untouched when their sources change afterwards.

    The review moves through ``draft`` -> ``confirm`` (approval) ->
    ``done``, with ``cancel`` available from ``draft``, ``confirm`` and
    ``done``. A review that is done locks the measurements recorded
    inside its period, and cancelling it unlocks them again.
    """

    _name = "strategy_review"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
        "mixin.transaction_date_duration",
    ]
    _description = "Strategy Review"

    # Multiple approval attributes. The final approval does NOT finish the
    # review: the user finishes it explicitly with the Done button.
    _approval_from_state = "draft"
    _approval_to_state = "confirm"
    _approval_state = "confirm"
    _after_approved_method = False

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True
    _automatically_insert_done_policy_fields = True
    _automatically_insert_done_button = True

    _statusbar_visible_label = "draft,confirm,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "done_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "action_done",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "done"

    plan_id = fields.Many2one(
        string="Plan",
        comodel_name="strategy_plan",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Strategy plan that is reviewed.",
    )
    department_id = fields.Many2one(
        string="Department",
        comodel_name="hr.department",
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Department that is reviewed. Leave empty to review the " "whole plan.",
    )
    plan_score = fields.Float(
        string="Plan Score",
        readonly=True,
        copy=False,
        help="Score of the plan at the time the snapshot was taken. It "
        "is a copy and does not follow the plan afterwards.",
    )
    summary = fields.Text(
        string="Summary",
        readonly=True,
        states={
            "draft": [("readonly", False)],
            "confirm": [("readonly", False)],
        },
        help="Conclusion of the review.",
    )
    line_ids = fields.One2many(
        string="Snapshot Lines",
        comodel_name="strategy_review.line",
        inverse_name="review_id",
        readonly=True,
        copy=False,
        states={
            "draft": [("readonly", False)],
            "confirm": [("readonly", False)],
        },
        help="Scores copied from the plan when the snapshot was taken, "
        "with the comment and the corrective action of the reviewers.",
    )

    @api.model
    def _get_locking_reviews(self, target, date):
        """Find the done reviews that lock a measurement date of a target.

        A done review locks the measurements of the targets of its plan
        that are dated inside its period, for every objective when the
        review has no department, or for the objectives of its department.

        :param target: the ``strategy_kpi.target`` of the measurement
        :param date: the date of the measurement
        :return: recordset of the done reviews that lock it; empty when
            the date is not locked
        """
        objective = target.sudo().objective_id
        return self.sudo().search(
            [
                ("state", "=", "done"),
                ("plan_id", "=", objective.plan_id.id),
                ("date_start", "<=", date),
                ("date_end", ">=", date),
                "|",
                ("department_id", "=", False),
                ("department_id", "=", objective.department_id.id),
            ]
        )

    def _get_snapshot_objectives(self):
        """Return the objectives that the snapshot copies.

        Cancelled objectives are left out, and so are the objectives of
        other departments when the review has a department.

        :return: recordset of objectives of the plan of the review
        """
        self.ensure_one()
        domain = [
            ("plan_id", "=", self.plan_id.id),
            ("state", "!=", "cancel"),
        ]
        if self.department_id:
            domain.append(("department_id", "=", self.department_id.id))
        return self.env["strategy_objective"].sudo().search(domain)

    def _get_snapshot_initiatives(self):
        """Return the initiatives that the snapshot copies.

        When the review has a department only the initiatives of that
        department are copied.

        :return: recordset of initiatives of the plan of the review
        """
        self.ensure_one()
        domain = [("plan_id", "=", self.plan_id.id)]
        if self.department_id:
            domain.append(("department_id", "=", self.department_id.id))
        return self.env["strategy_initiative"].sudo().search(domain)

    def _get_snapshot_target(self, kpi):
        """Pick the target of a KPI that the snapshot copies.

        The targets that overlap the period of the review are
        candidates, and the one that ends last wins.

        :param kpi: the ``strategy_kpi`` to look at
        :return: the chosen ``strategy_kpi.target``; empty when no target
            of the KPI overlaps the period of the review
        """
        self.ensure_one()
        targets = kpi.target_ids.filtered(
            lambda r: r.date_start <= self.date_end and r.date_end >= self.date_start
        )
        return targets.sorted(key=lambda r: (r.date_end, r.id))[-1:]

    def _prepare_snapshot_lines(self):
        """Build the snapshot lines of the review.

        Every objective gives a line with its score, followed by one
        line for each of its KPIs that has a target in the period, with
        the target, the realization and the score of that target. The
        initiatives follow, with their progress and health.

        :return: list of ``create`` commands for ``line_ids``
        """
        self.ensure_one()
        result = []
        for objective in self._get_snapshot_objectives():
            result.append(
                (
                    0,
                    0,
                    {
                        "line_type": "objective",
                        "objective_id": objective.id,
                        "score": objective.score,
                    },
                )
            )
            for kpi in objective.kpi_ids:
                target = self._get_snapshot_target(kpi)
                if target:
                    result.append(
                        (
                            0,
                            0,
                            {
                                "line_type": "kpi",
                                "objective_id": objective.id,
                                "kpi_id": kpi.id,
                                "target": target.target,
                                "realization": target.realization,
                                "score": target.score,
                            },
                        )
                    )
        for initiative in self._get_snapshot_initiatives():
            result.append(
                (
                    0,
                    0,
                    {
                        "line_type": "initiative",
                        "initiative_id": initiative.id,
                        "progress": initiative.progress,
                        "health": initiative.health,
                    },
                )
            )
        return result

    def action_take_snapshot(self):
        """Copy the scores of the plan into the lines of the review.

        The existing lines are deleted first, so the button can be
        clicked again to refresh the snapshot. The score of the plan is
        copied too.

        :raises UserError: when the review is not a draft
        """
        for record in self:
            if record.state != "draft":
                error_message = """
Context: Take review snapshot
Database ID: %s
Problem: A snapshot can only be taken while the review is a draft.
Solution: Restart the review before taking a new snapshot
""" % (
                    record.id,
                )
                raise UserError(_(error_message))
            record.line_ids.unlink()
            record.write(
                {
                    "plan_score": record.plan_id.score,
                    "line_ids": record._prepare_snapshot_lines(),
                }
            )

    @ssi_decorator.pre_confirm_check()
    def _10_check_snapshot_taken(self):
        """Reject confirming a review that has no snapshot line.

        Runs in the ``pre_confirm_check`` slot, so the review stays a
        draft when the check fails.

        :raises UserError: when the review has no line
        """
        self.ensure_one()
        if not self.line_ids:
            error_message = """
Context: Confirm review
Database ID: %s
Problem: Take a snapshot before confirming the review.
Solution: Click the Take Snapshot button, then confirm the review
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
            "done_ok",
            "cancel_ok",
            "restart_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res
