# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StrategyKpiScoreRange(models.Model):
    """Maps a realization value range of a KPI to a score.

    Each line states that a realization falling between min_value and
    max_value earns score. Lines are copied from the measure of the KPI
    and edited inline on the form of their parent KPI.
    """

    _name = "strategy_kpi.score_range"
    _description = "Strategy KPI - Score Range"
    _order = "kpi_id, min_value, id"

    kpi_id = fields.Many2one(
        string="# KPI",
        comodel_name="strategy_kpi",
        required=True,
        ondelete="cascade",
        help="KPI that owns this score range line.",
    )
    min_value = fields.Float(
        string="From",
        required=True,
        default=0.0,
        help="Lower bound of the realization value range.",
    )
    max_value = fields.Float(
        string="To",
        required=True,
        default=0.0,
        help="Upper bound of the realization value range.",
    )
    score = fields.Float(
        string="Score",
        required=True,
        default=0.0,
        help="Score earned when the realization falls in this range.",
    )

    @api.constrains("min_value", "max_value")
    def _check_value_limit(self):
        """Reject lines whose lower bound exceeds the upper bound.

        :raises ValidationError: when the condition method returns False
        """
        for line in self.sudo():
            if not line._check_value_limit_condition():
                error_message = """
Context: Create or update KPI score range
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
