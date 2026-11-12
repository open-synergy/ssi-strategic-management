# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StrategyScoreCategoryRange(models.Model):
    """Defines one labelled score range of a score category.

    A line states that scores between min_value and max_value
    belong to the label name. Lines of one category must not overlap.
    Lines are edited inline on the form of their parent category.
    """

    _name = "strategy_score_category.range"
    _description = "Strategy Score Category - Range"
    _order = "category_id, sequence, id"

    category_id = fields.Many2one(
        string="# Score Category",
        comodel_name="strategy_score_category",
        required=True,
        ondelete="cascade",
        help="Score category that owns this range line.",
    )
    name = fields.Char(
        string="Label",
        required=True,
        translate=True,
        help="Label given to scores that fall in this range.",
    )
    min_value = fields.Float(
        string="From",
        help="Lower bound of the score range.",
    )
    max_value = fields.Float(
        string="To",
        help="Upper bound of the score range.",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=10,
        help="Display order of the range inside its category.",
    )

    @api.constrains("min_value", "max_value")
    def _check_value_limit(self):
        """Reject lines whose lower bound exceeds the upper bound.

        :raises ValidationError: when the condition method returns False
        """
        for line in self.sudo():
            if not line._check_value_limit_condition():
                error_message = """
Context: Create or update score category range
Database ID: %s
Problem: Range start must not be greater than range end
Solution: Change the From or To value
""" % (
                    line.id,
                )
                raise ValidationError(_(error_message))

    def _check_value_limit_condition(self):
        """Tell whether the bounds of the line are consistent.

        Extension point: override to relax or tighten the rule.

        :return: True when min_value <= max_value; never raises
        """
        self.ensure_one()
        return self.min_value <= self.max_value

    @api.constrains("category_id", "min_value", "max_value")
    def _check_overlap(self):
        """Reject lines that overlap another line of the same category.

        :raises ValidationError: when the condition method returns False
        """
        for line in self.sudo():
            if not line._check_overlap_condition():
                error_message = """
Context: Create or update score category range
Database ID: %s
Problem: Score ranges must not overlap.
Solution: Change the From or To value so ranges do not overlap
""" % (
                    line.id,
                )
                raise ValidationError(_(error_message))

    def _check_overlap_condition(self):
        """Tell whether the line is free of overlap with its siblings.

        Two ranges overlap when each one starts before the other ends;
        ranges that merely touch at a boundary are allowed.

        Extension point: override to change the overlap definition.

        :return: True when no sibling overlaps; never raises
        """
        self.ensure_one()
        siblings = self.category_id.range_ids - self
        for sibling in siblings:
            if (
                self.min_value < sibling.max_value
                and sibling.min_value < self.max_value
            ):
                return False
        return True
