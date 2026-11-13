# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestStrategyInitiative(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the ``strategy_initiative`` model.

    The scenarios exercise the lifecycle, the cancel and terminate
    flows, the three progress methods, the health thresholds and the
    daily cron, and the start pre-checks.
    """

    def test_strategy_initiative(self):
        """Run the initiative lifecycle, progress and health scenarios."""
        self.run_yaml_scenario("test_data_strategy_initiative.yaml")
