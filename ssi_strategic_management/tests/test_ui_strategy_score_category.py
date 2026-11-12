# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiStrategyScoreCategory(HttpSavepointCase):
    """Tour tests for the ``strategy_score_category`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the sequence template the Generate Code step needs."""
        super().setUpClass()
        # Pre-Condition for Generate Code (docs/strategy_score_category/01-create.md):
        # an active sequence.template for this model is required, or
        # clicking the button raises a UserError instead of assigning a
        # code.
        cls.code_sequence = cls.env["ir.sequence"].create(
            {
                "name": "TOUR Score Category Code Sequence",
                "code": "ssi_strategic_management.tour.strategy_score_category",
                "prefix": "TOURSEQORY",
                "padding": 4,
            }
        )
        cls.code_sequence_template = cls.env["sequence.template"].create(
            {
                "name": "TOUR Score Category Sequence Template",
                "model_id": cls.env["ir.model"]._get_id("strategy_score_category"),
                "sequence_field_id": cls.env["ir.model.fields"]
                ._get("strategy_score_category", "code")
                .id,
                "date_field_id": cls.env["ir.model.fields"]
                ._get("strategy_score_category", "create_date")
                .id,
                "sequence_selection_method": "use_sequence",
                "sequence_id": cls.code_sequence.id,
            }
        )

    def test_create(self):
        """Run the create tour for ``strategy_score_category``.

        IK: docs/strategy_score_category/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_strategic_management_strategy_score_category_create",
            login="admin",
        )
