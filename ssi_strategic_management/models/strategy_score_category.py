# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StrategyScoreCategory(models.Model):
    """Represents a scoring scale that classifies a numeric score.

    A score category is a named set of ranges, for example Poor, Fair and
    Good, used to translate the score of an objective or a KPI into a
    label. Plan types point to the category their plans use.
    """

    _name = "strategy_score_category"
    _inherit = ["mixin.master_data"]
    _description = "Strategy Score Category"

    range_ids = fields.One2many(
        string="Ranges",
        comodel_name="strategy_score_category.range",
        inverse_name="category_id",
        help="Score ranges and the label each of them carries.",
    )
