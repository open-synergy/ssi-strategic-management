# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from unittest import mock

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestStrategyObjective(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the ``strategy_objective`` model.

    The scenarios exercise the draft, open and done lifecycle, the
    cancel and restart flow, the cascade to departments and employees,
    the weight check of the start action and every validation rule of
    the objective.
    """

    def test_strategy_objective(self):
        """Run the objective lifecycle and validation scenarios."""
        self.run_yaml_scenario("test_data_strategy_objective.yaml")

    def test_insert_form_element_switched_off(self):
        """Assert the form view is left untouched when the switch is off.

        Pure Python - trigger P6 (L-15: the YAML runner cannot patch a
        class attribute). The switch is ``True`` on the model, so the
        ``else`` path is only reachable by patching it.
        """
        objective_model = self.env["strategy_objective"]
        view_arch = object()
        with mock.patch.object(
            type(objective_model), "_automatically_insert_view_element", False
        ):
            result = objective_model._insert_form_element(view_arch)
        self.assertIs(result, view_arch)
