# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date
from unittest import mock

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

    def test_period_condition_without_dates(self):
        """Assert the period condition tolerates plans without dates.

        Pure Python - trigger P1 (L-01: the ``call`` action discards the
        boolean returned by the condition method). The guards are only
        reachable with unsaved records, because ``date_start`` and
        ``date_end`` are required in the database.
        """
        plan_model = self.env["strategy_plan"]
        parent = plan_model.new(
            {
                "date_start": date(2026, 1, 1),
                "date_end": date(2026, 12, 31),
            }
        )
        # Sub-plan without a start date: nothing to compare.
        no_start = plan_model.new({"parent_id": parent, "date_end": date(2027, 6, 30)})
        self.assertTrue(no_start._check_period_within_parent_condition())
        # Sub-plan without an end date: nothing to compare.
        no_end = plan_model.new({"parent_id": parent, "date_start": date(2025, 1, 1)})
        self.assertTrue(no_end._check_period_within_parent_condition())
        # Parent without dates: nothing to compare against.
        open_parent = plan_model.new({})
        child = plan_model.new(
            {
                "parent_id": open_parent,
                "date_start": date(2026, 4, 1),
                "date_end": date(2026, 6, 30),
            }
        )
        self.assertTrue(child._check_period_within_parent_condition())
        # Sanity check of the compared branch: a period outside the
        # parent period is not accepted.
        outside = plan_model.new(
            {
                "parent_id": parent,
                "date_start": date(2026, 4, 1),
                "date_end": date(2027, 1, 31),
            }
        )
        self.assertFalse(outside._check_period_within_parent_condition())

    def test_insert_form_element_switched_off(self):
        """Assert the form view is left untouched when the switch is off.

        Pure Python - trigger P6 (L-15: the YAML runner cannot patch a
        class attribute). The switch is ``True`` on the model, so the
        ``else`` path is only reachable by patching it.
        """
        plan_model = self.env["strategy_plan"]
        view_arch = object()
        with mock.patch.object(
            type(plan_model), "_automatically_insert_view_element", False
        ):
            result = plan_model._insert_form_element(view_arch)
        self.assertIs(result, view_arch)
