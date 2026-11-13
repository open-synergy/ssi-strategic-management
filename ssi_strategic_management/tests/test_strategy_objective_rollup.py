# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestStrategyObjectiveRollup(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the score rollup of ``strategy_objective`` and ``strategy_plan``.

    The scenarios exercise the KPI portion defaults, the KPI score, the
    child score and the objective score, the exclusion of cancelled and
    non contributing children, the rollup of a measurement change up to
    the plan, the score category ranges and the KPI portion limits.
    """

    def test_strategy_objective_rollup(self):
        """Run the objective and plan score rollup scenarios."""
        self.run_yaml_scenario("test_data_strategy_objective_rollup.yaml")
