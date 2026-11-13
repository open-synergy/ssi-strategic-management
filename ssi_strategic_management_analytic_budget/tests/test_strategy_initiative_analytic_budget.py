# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestStrategyInitiativeAnalyticBudget(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the analytic budget extension of ``strategy_initiative``.

    The scenarios exercise the budget amounts and the absorption, the
    budgets that are left out, the health gap and the initiatives
    shown on the budget.
    """

    def test_strategy_initiative_analytic_budget(self):
        """Run the budget amount, absorption and health scenarios."""
        self.run_yaml_scenario("test_data_strategy_initiative_analytic_budget.yaml")
