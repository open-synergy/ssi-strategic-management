# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0 only SavepointCase prepares
# ``cls.env`` in ``setUpClass``; this tour needs no fixture, the delta
# assertion only needs the create form to be rendered.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiStrategyInitiative(HttpSavepointCase):
    """Tour test for the Analytic Account field of the initiative."""

    def test_create(self):
        """Run the create tour for ``strategy_initiative``.

        IK: docs/strategy_initiative/01-create.md (E1 delta --
        Additional Fields)
        """
        self.start_tour(
            "/web",
            "ssi_strategic_management_analytic_budget_strategy_initiative_create",
            login="admin",
        )
