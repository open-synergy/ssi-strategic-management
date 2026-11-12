# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestStrategyScoreCategory(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the ``strategy_score_category`` model.

    The scenarios exercise the create, edit and delete flows run by a
    configurator user, the read-only access of an internal user and the
    validation rules of the model.
    """

    def test_strategy_score_category(self):
        """Run the score category CRUD, access and constraint scenarios."""
        self.run_yaml_scenario("test_data_strategy_score_category.yaml")
