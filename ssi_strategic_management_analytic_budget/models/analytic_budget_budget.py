# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AnalyticBudgetBudget(models.Model):
    _inherit = "analytic_budget.budget"

    # Extension of the analytic budget. It lists the strategy
    # initiatives that are linked to the analytic account of the
    # budget, for display on the budget form only.

    strategy_initiative_ids = fields.Many2many(
        string="Strategic Initiatives",
        comodel_name="strategy_initiative",
        relation="rel_analytic_budget_2_strategy_initiative",
        column1="budget_id",
        column2="initiative_id",
        compute="_compute_strategy_initiative_ids",
        compute_sudo=True,
        store=False,
        help="Strategy initiatives that use the analytic account of this " "budget.",
    )

    @api.depends("analytic_account_id")
    def _compute_strategy_initiative_ids(self):
        """Compute the initiatives of the analytic account of the budget.

        Empty when the budget has no analytic account.

        :return: None
        """
        Initiative = self.env["strategy_initiative"].sudo()
        for record in self:
            record.strategy_initiative_ids = Initiative.search(
                [("analytic_account_id", "in", record.analytic_account_id.ids)]
            )
