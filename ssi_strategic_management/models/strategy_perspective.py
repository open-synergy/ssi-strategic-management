# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StrategyPerspective(models.Model):
    """Represents a Balanced Scorecard perspective.

    A perspective groups strategic objectives by viewpoint, such as
    Financial, Customer, Internal Process, or Learning and Growth. It is
    master data shared by every strategic plan of the company.
    """

    _name = "strategy_perspective"
    _inherit = ["mixin.master_data"]
    _description = "Strategy Perspective"
    _order = "sequence asc, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Display order of the perspective. Lower values appear first.",
    )
    color = fields.Integer(
        string="Color Index",
        help="Color index used to tint the perspective on dashboards.",
    )
