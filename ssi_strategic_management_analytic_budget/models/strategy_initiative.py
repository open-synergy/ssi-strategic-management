# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date

from odoo import api, fields, models


class StrategyInitiative(models.Model):
    _inherit = "strategy_initiative"

    # Extension of the strategy initiative. The initiative is linked to
    # an analytic account and reads the planned amount and the
    # realization of the analytic budgets of that account. No budget
    # figure is stored on the initiative: every figure below is
    # computed on read from ``analytic_budget.budget``.

    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Analytic account whose budgets fund this initiative. The "
        "budgets of its child accounts are counted as well.",
    )
    analytic_budget_ids = fields.Many2many(
        string="Analytic Budgets",
        comodel_name="analytic_budget.budget",
        relation="rel_strategy_initiative_2_analytic_budget",
        column1="initiative_id",
        column2="budget_id",
        compute="_compute_analytic_budget_ids",
        compute_sudo=True,
        store=False,
        help="Open and done budgets of the analytic account (and of its "
        "child accounts) whose period overlaps the period of this "
        "initiative.",
    )
    company_currency_id = fields.Many2one(
        string="Company Currency",
        comodel_name="res.currency",
        related="company_id.currency_id",
        readonly=True,
        help="Currency of the company that owns the initiative.",
    )
    amount_planned_cost = fields.Monetary(
        string="Planned Cost",
        compute="_compute_budget_amount",
        compute_sudo=True,
        store=False,
        currency_field="company_currency_id",
        help="Sum of the planned cost of the analytic budgets of the " "initiative.",
    )
    amount_cost_realization = fields.Monetary(
        string="Cost Realization",
        compute="_compute_budget_amount",
        compute_sudo=True,
        store=False,
        currency_field="company_currency_id",
        help="Sum of the cost realization of the analytic budgets of the "
        "initiative.",
    )
    budget_absorption = fields.Float(
        string="Budget Absorption (%)",
        compute="_compute_budget_amount",
        compute_sudo=True,
        store=False,
        help="Cost realization as a percentage of the planned cost. Zero "
        "when nothing is planned.",
    )

    def _get_analytic_budget_criteria(self):
        """Build the criteria of the analytic budgets of the initiative.

        A budget counts when it is open or done, belongs to the same
        company, sits on the analytic account of the initiative or on
        one of its descendants, and its period overlaps the period of
        the initiative. A budget that has no period is not limited in
        time and always overlaps. An initiative that is still missing a
        date is not limited on that side.

        :return: search domain on ``analytic_budget.budget``
        :rtype: list
        """
        self.ensure_one()
        date_start = self.date_start or date.min
        date_end = self.date_end or date.max
        return [
            ("state", "in", ["open", "done"]),
            ("company_id", "=", self.company_id.id),
            ("analytic_account_id", "child_of", self.analytic_account_id.id),
            "|",
            ("date_start", "=", False),
            ("date_start", "<=", date_end),
            "|",
            ("date_end", "=", False),
            ("date_end", ">=", date_start),
        ]

    @api.depends(
        "analytic_account_id",
        "company_id",
        "date_start",
        "date_end",
    )
    def _compute_analytic_budget_ids(self):
        """Compute the analytic budgets that fund the initiative.

        Empty when the initiative has no analytic account.

        :return: None
        """
        Budget = self.env["analytic_budget.budget"].sudo()
        for record in self:
            result = Budget
            if record.analytic_account_id:
                result = Budget.search(record._get_analytic_budget_criteria())
            record.analytic_budget_ids = result

    @api.depends(
        "analytic_account_id",
        "company_id",
        "date_start",
        "date_end",
    )
    def _compute_budget_amount(self):
        """Compute the planned cost, the realization and the absorption.

        The amounts are the sums of the matching fields of the
        analytic budgets of the initiative. The absorption is the
        realization over the planned cost, and zero when the planned
        cost is zero.

        :return: None
        """
        for record in self:
            budgets = record.analytic_budget_ids
            planned = sum(budgets.mapped("amount_planned_cost"))
            realization = sum(budgets.mapped("amount_cost_realization"))
            absorption = 0.0
            if planned:
                absorption = realization * 100.0 / planned
            record.amount_planned_cost = planned
            record.amount_cost_realization = realization
            record.budget_absorption = absorption

    def _get_health_gap(self):
        """Tell how far the initiative is behind, budget included.

        Adds the budget absorption as a source of gap: spending that
        runs ahead of the progress counts as being behind. The largest
        of the schedule gap and the budget gap is returned. An
        initiative without analytic account keeps the schedule gap.

        :return: the gap in percentage points
        """
        self.ensure_one()
        result = super()._get_health_gap()
        if self.analytic_account_id:
            result = max(result, self.budget_absorption - self.progress)
        return result
