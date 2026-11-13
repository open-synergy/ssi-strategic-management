# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from unittest import mock

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

    def test_insert_form_element_switched_off(self):
        """Assert the form view is left untouched when the switch is off.

        Pure Python - trigger P6 (L-15: the YAML runner cannot patch a
        class attribute). The switch is ``True`` on the model, so the
        ``else`` path is only reachable by patching it.
        """
        initiative_model = self.env["strategy_initiative"]
        view_arch = object()
        with mock.patch.object(
            type(initiative_model), "_automatically_insert_view_element", False
        ):
            result = initiative_model._insert_form_element(view_arch)
        self.assertIs(result, view_arch)
