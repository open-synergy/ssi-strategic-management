# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from unittest import mock

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestStrategyReview(YamlTransactionCase):  # pylint: disable=too-few-public-methods
    """Cover the ``strategy_review`` model and its measurement lock.

    The scenarios exercise the snapshot of the scores, the department
    filter, the lifecycle with approval, the guards of the snapshot and
    of the confirmation, and the lock that a done review puts on the
    measurements of its period.
    """

    def test_strategy_review(self):
        """Run the snapshot and lifecycle scenarios."""
        self.run_yaml_scenario("test_data_strategy_review.yaml")

    def test_strategy_review_lock(self):
        """Run the measurement lock scenarios."""
        self.run_yaml_scenario("test_data_strategy_review_lock.yaml")

    def test_insert_form_element_switched_off(self):
        """Assert the form view is left untouched when the switch is off.

        Pure Python - trigger P6 (L-15: the YAML runner cannot patch a
        class attribute). The switch is ``True`` on the model, so the
        ``else`` path is only reachable by patching it.
        """
        review_model = self.env["strategy_review"]
        view_arch = object()
        with mock.patch.object(
            type(review_model), "_automatically_insert_view_element", False
        ):
            result = review_model._insert_form_element(view_arch)
        self.assertIs(result, view_arch)
