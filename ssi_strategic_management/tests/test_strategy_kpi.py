# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestStrategyKpi(YamlTransactionCase):  # pylint: disable=too-few-public-methods
    """Cover the ``strategy_kpi`` models.

    The scenarios exercise the score of a target for every score method
    and score scale, the aggregation of measurements, the score of a
    KPI, the defaults copied from the measure and the date range, every
    validation rule of the KPI, its targets and its measurements, and
    the KPI weight check of the objective start action.
    """

    def test_strategy_kpi(self):
        """Run the KPI, target and measurement scenarios."""
        self.run_yaml_scenario("test_data_strategy_kpi.yaml")
