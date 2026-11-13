# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestStrategyKpiPythonAccess(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the access to the Python code of a ``strategy_kpi``.

    Only the measure configurators may write the Python code of a KPI or
    switch its realization method to Python beyond what the measure
    carries; an objective user may only pick a measure prepared by them.
    """

    def test_strategy_kpi_python_access(self):
        """Run the Python code access scenarios of the KPI."""
        self.run_yaml_scenario("test_data_strategy_kpi_python_access.yaml")
