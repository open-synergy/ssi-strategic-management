# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiStrategyPerspective(HttpSavepointCase):
    """Tour tests for the ``strategy_perspective`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the sequence template the Generate Code step needs."""
        super().setUpClass()
        # Pre-Condition for Generate Code (docs/strategy_perspective/01-create.md):
        # an active sequence.template for this model is required, or
        # clicking the button raises a UserError instead of assigning a
        # code.
        cls.code_sequence = cls.env["ir.sequence"].create(
            {
                "name": "TOUR Perspective Code Sequence",
                "code": "ssi_strategic_management.tour.strategy_perspective",
                "prefix": "TOURSEQIVE",
                "padding": 4,
            }
        )
        cls.code_sequence_template = cls.env["sequence.template"].create(
            {
                "name": "TOUR Perspective Sequence Template",
                "model_id": cls.env["ir.model"]._get_id("strategy_perspective"),
                "sequence_field_id": cls.env["ir.model.fields"]
                ._get("strategy_perspective", "code")
                .id,
                "date_field_id": cls.env["ir.model.fields"]
                ._get("strategy_perspective", "create_date")
                .id,
                "sequence_selection_method": "use_sequence",
                "sequence_id": cls.code_sequence.id,
            }
        )

    def test_create(self):
        """Run the create tour for ``strategy_perspective``.

        IK: docs/strategy_perspective/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_strategic_management_strategy_perspective_create",
            login="admin",
        )
