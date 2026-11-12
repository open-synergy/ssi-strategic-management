# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StrategyMeasure(models.Model):
    """Represents an entry of the strategic measure library.

    A measure defines how an indicator is expressed and scored: its unit,
    polarity, reporting frequency, aggregation and the score range
    mapping. Key results and KPIs of a plan reuse these definitions.
    """

    _name = "strategy_measure"
    _inherit = ["mixin.master_data"]
    _description = "Strategy Measure"

    uom_label = fields.Char(
        string="Unit",
        help="Unit label shown next to values of this measure.",
    )
    polarity = fields.Selection(
        string="Polarity",
        selection=[
            ("higher", "Higher is Better"),
            ("lower", "Lower is Better"),
            ("range", "Within Range"),
        ],
        required=True,
        default="higher",
        help=(
            "Direction in which the measure improves: "
            "Higher is Better = larger values score better, "
            "Lower is Better = smaller values score better, "
            "Within Range = values must stay inside a target range."
        ),
    )
    frequency = fields.Selection(
        string="Frequency",
        selection=[
            ("monthly", "Monthly"),
            ("quarterly", "Quarterly"),
            ("semesterly", "Semesterly"),
            ("yearly", "Yearly"),
        ],
        required=True,
        default="monthly",
        help="How often a realization of this measure is expected.",
    )
    indicator_type = fields.Selection(
        string="Indicator Type",
        selection=[
            ("lagging", "Lagging"),
            ("leading", "Leading"),
        ],
        required=True,
        default="lagging",
        help=(
            "Lagging = reports an outcome that already happened. "
            "Leading = predicts a future outcome."
        ),
    )
    aggregation = fields.Selection(
        string="Aggregation",
        selection=[
            ("sum", "Sum"),
            ("avg", "Average"),
            ("last", "Last Value"),
        ],
        required=True,
        default="last",
        help=(
            "How periodic realizations roll up into a longer period: "
            "Sum = add them, Average = mean value, "
            "Last Value = value of the latest period."
        ),
    )
    definition = fields.Text(
        string="Definition",
        help="Business definition and formula of the measure.",
    )
    data_source = fields.Text(
        string="Data Source",
        help="Where the realization data of this measure comes from.",
    )
    score_min = fields.Float(
        string="Minimum Score",
        default=0.0,
        help="Lowest score a realization can receive.",
    )
    score_max = fields.Float(
        string="Maximum Score",
        default=120.0,
        help="Highest score a realization can receive.",
    )
    score_range_ids = fields.One2many(
        string="Score Ranges",
        comodel_name="strategy_measure.score_range",
        inverse_name="measure_id",
        help="Mapping from realization value ranges to scores.",
    )

    @api.constrains("score_min", "score_max")
    def _check_score_limit(self):
        """Reject measures whose minimum score exceeds the maximum.

        :raises ValidationError: when the condition method returns False
        """
        for measure in self.sudo():
            if not measure._check_score_limit_condition():
                error_message = """
Context: Create or update strategy measure
Database ID: %s
Problem: Minimum score must not be greater than maximum score
Solution: Change minimum or maximum score
""" % (
                    measure.id,
                )
                raise ValidationError(_(error_message))

    def _check_score_limit_condition(self):
        """Tell whether the score limits of the measure are consistent.

        Extension point: override to relax or tighten the rule.

        :return: True when score_min <= score_max; never raises
        """
        self.ensure_one()
        return self.score_min <= self.score_max
