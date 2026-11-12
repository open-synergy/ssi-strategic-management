# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestStrategyMeasure(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the ``strategy_measure`` model.

    The scenarios exercise the create, edit and delete flows run by a
    configurator user, the read-only access of an internal user and the
    validation rules of the model.
    """

    def test_strategy_measure(self):
        """Run the measure CRUD, access and constraint scenarios."""
        self.run_yaml_scenario("test_data_strategy_measure.yaml")
