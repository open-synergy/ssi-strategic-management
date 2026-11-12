# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestStrategyPlan(YamlTransactionCase):  # pylint: disable=too-few-public-methods
    """Cover the ``strategy_plan`` model.

    The scenarios exercise the draft, confirm, approve, open and done
    lifecycle, the cancel flow and the parent/sub-plan rules: period
    containment, hierarchy recursion and the parent plan pre-check of
    the start action.
    """

    def test_strategy_plan(self):
        """Run the plan lifecycle and hierarchy scenarios."""
        self.run_yaml_scenario("test_data_strategy_plan.yaml")
