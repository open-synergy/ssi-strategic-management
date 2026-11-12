# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiStrategyMeasure(HttpSavepointCase):
    """Tour tests for the ``strategy_measure`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the sequence template the Generate Code step needs."""
        super().setUpClass()
        # Pre-Condition for Generate Code (docs/strategy_measure/01-create.md):
        # an active sequence.template for this model is required, or
        # clicking the button raises a UserError instead of assigning a
        # code.
        cls.code_sequence = cls.env["ir.sequence"].create(
            {
                "name": "TOUR Measure Code Sequence",
                "code": "ssi_strategic_management.tour.strategy_measure",
                "prefix": "TOURSEQURE",
                "padding": 4,
            }
        )
        cls.code_sequence_template = cls.env["sequence.template"].create(
            {
                "name": "TOUR Measure Sequence Template",
                "model_id": cls.env["ir.model"]._get_id("strategy_measure"),
                "sequence_field_id": cls.env["ir.model.fields"]
                ._get("strategy_measure", "code")
                .id,
                "date_field_id": cls.env["ir.model.fields"]
                ._get("strategy_measure", "create_date")
                .id,
                "sequence_selection_method": "use_sequence",
                "sequence_id": cls.code_sequence.id,
            }
        )

    def test_create(self):
        """Run the create tour for ``strategy_measure``.

        IK: docs/strategy_measure/01-create.md
        """
        self.start_tour(
            "/web", "ssi_strategic_management_strategy_measure_create", login="admin"
        )
