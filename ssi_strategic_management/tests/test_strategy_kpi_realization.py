# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestStrategyKpiRealization(  # pylint: disable=too-few-public-methods
    YamlTransactionCase
):
    """Cover the automatic realization of the KPI targets.

    The scenarios exercise the aggregate engine (count, ratio, value
    field, employee filter), the Python engine, the direct cascade from
    child KPIs, the override of an automatic measurement, the
    configuration constraints and the scheduled queueing of jobs.
    """

    def test_strategy_kpi_realization(self):
        """Run the automatic realization scenarios."""
        self.run_yaml_scenario("test_data_strategy_kpi_realization.yaml")
