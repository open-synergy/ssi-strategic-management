# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiStrategyPlanType(HttpSavepointCase):
    """Tour tests for the ``strategy_plan_type`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the sequence template the Generate Code step needs."""
        super().setUpClass()
        # Pre-Condition for Generate Code (docs/strategy_plan_type/01-create.md):
        # an active sequence.template for this model is required, or
        # clicking the button raises a UserError instead of assigning a
        # code.
        cls.code_sequence = cls.env["ir.sequence"].create(
            {
                "name": "TOUR Plan Type Code Sequence",
                "code": "ssi_strategic_management.tour.strategy_plan_type",
                "prefix": "TOURSEQYPE",
                "padding": 4,
            }
        )
        cls.code_sequence_template = cls.env["sequence.template"].create(
            {
                "name": "TOUR Plan Type Sequence Template",
                "model_id": cls.env["ir.model"]._get_id("strategy_plan_type"),
                "sequence_field_id": cls.env["ir.model.fields"]
                ._get("strategy_plan_type", "code")
                .id,
                "date_field_id": cls.env["ir.model.fields"]
                ._get("strategy_plan_type", "create_date")
                .id,
                "sequence_selection_method": "use_sequence",
                "sequence_id": cls.code_sequence.id,
            }
        )

    def test_create(self):
        """Run the create tour for ``strategy_plan_type``.

        IK: docs/strategy_plan_type/01-create.md
        """
        self.start_tour(
            "/web", "ssi_strategic_management_strategy_plan_type_create", login="admin"
        )
