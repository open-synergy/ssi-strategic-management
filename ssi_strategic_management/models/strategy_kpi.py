# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StrategyKpi(models.Model):
    """Represents a key performance indicator of a strategy objective.

    A KPI measures the achievement of an objective through a measure of
    the measure library. It carries a weight, a default target and the
    score method used to turn a realization into a score. Its targets
    per period collect the manual measurements, and its own score is the
    score of the latest measured target.
    """

    _name = "strategy_kpi"
    _description = "Strategy KPI"
    _order = "objective_id, id"

    objective_id = fields.Many2one(
        string="Objective",
        comodel_name="strategy_objective",
        required=True,
        ondelete="cascade",
        help="Strategy objective that this KPI measures.",
    )
    name = fields.Char(
        string="Name",
        required=True,
        help="Name of the KPI.",
    )
    measure_id = fields.Many2one(
        string="Measure",
        comodel_name="strategy_measure",
        required=True,
        ondelete="restrict",
        help="Measure of the library that defines how this KPI is "
        "expressed and scored.",
    )
    uom_label = fields.Char(
        string="Unit",
        compute="_compute_uom_label",
        store=True,
        readonly=False,
        compute_sudo=True,
        help="Unit label shown next to values of this KPI. Copied from "
        "the measure and editable.",
    )
    polarity = fields.Selection(
        string="Polarity",
        selection=[
            ("higher", "Higher is Better"),
            ("lower", "Lower is Better"),
            ("range", "Within Range"),
        ],
        compute="_compute_polarity",
        store=True,
        readonly=False,
        compute_sudo=True,
        help="Direction in which the KPI improves. Copied from the "
        "measure and editable.",
    )
    aggregation = fields.Selection(
        string="Aggregation",
        selection=[
            ("sum", "Sum"),
            ("avg", "Average"),
            ("last", "Last Value"),
        ],
        compute="_compute_aggregation",
        store=True,
        readonly=False,
        compute_sudo=True,
        help="How the measurements of a target roll up into its "
        "realization: Sum = add them, Average = mean value, Last Value = "
        "value of the latest measurement. Copied from the measure and "
        "editable.",
    )
    score_min = fields.Float(
        string="Minimum Score",
        compute="_compute_score_min",
        store=True,
        readonly=False,
        compute_sudo=True,
        help="Lowest score a realization can receive. Copied from the "
        "measure and editable.",
    )
    score_max = fields.Float(
        string="Maximum Score",
        compute="_compute_score_max",
        store=True,
        readonly=False,
        compute_sudo=True,
        help="Highest score a realization can receive. Copied from the "
        "measure and editable.",
    )
    score_method = fields.Selection(
        string="Score Method",
        selection=[
            ("higher", "Higher is Better"),
            ("lower", "Lower is Better"),
            ("range", "Within Range"),
        ],
        compute="_compute_score_method",
        store=True,
        readonly=False,
        compute_sudo=True,
        help="Formula that turns a realization into a score: Higher is "
        "Better = realization / target, Lower is Better = target / "
        "realization, Within Range = score of the matching score range. "
        "Derived from the polarity and editable.",
    )
    weight = fields.Float(
        string="Weight (%)",
        default=0.0,
        help="Share of this KPI in the objective. The weights of all "
        "KPIs of an objective must add up to 100% before the objective "
        "can be started.",
    )
    baseline = fields.Float(
        string="Baseline",
        default=0.0,
        help="Value of the KPI before the plan period started.",
    )
    target = fields.Float(
        string="Default Target",
        default=0.0,
        help="Target proposed for every new period of this KPI.",
    )
    is_key_result = fields.Boolean(
        string="Key Result",
        default=False,
        help="Check to mark this KPI as a Key Result of an OKR " "objective.",
    )
    key_result_type = fields.Selection(
        string="Key Result Type",
        selection=[
            ("committed", "Committed"),
            ("aspirational", "Aspirational"),
        ],
        help="Committed = must be achieved fully, Aspirational = a "
        "stretch goal. Required for key results.",
    )
    score_range_ids = fields.One2many(
        string="Score Ranges",
        comodel_name="strategy_kpi.score_range",
        inverse_name="kpi_id",
        help="Mapping from realization value ranges to scores. Filled "
        "from the measure and editable.",
    )
    target_ids = fields.One2many(
        string="Targets",
        comodel_name="strategy_kpi.target",
        inverse_name="kpi_id",
        help="Targets of this KPI per period.",
    )
    score = fields.Float(
        string="Score",
        compute="_compute_score",
        store=True,
        compute_sudo=True,
        help="Score of the measured target with the latest end date. "
        "0 when no target has a measurement yet.",
    )

    @api.depends("measure_id")
    def _compute_uom_label(self):
        """Copy the unit label of the measure into the KPI."""
        for record in self:
            result = False
            if record.measure_id:
                result = record.measure_id.uom_label
            record.uom_label = result

    @api.depends("measure_id")
    def _compute_polarity(self):
        """Copy the polarity of the measure into the KPI."""
        for record in self:
            result = "higher"
            if record.measure_id:
                result = record.measure_id.polarity
            record.polarity = result

    @api.depends("measure_id")
    def _compute_aggregation(self):
        """Copy the aggregation of the measure into the KPI."""
        for record in self:
            result = "last"
            if record.measure_id:
                result = record.measure_id.aggregation
            record.aggregation = result

    @api.depends("measure_id")
    def _compute_score_min(self):
        """Copy the minimum score of the measure into the KPI."""
        for record in self:
            result = 0.0
            if record.measure_id:
                result = record.measure_id.score_min
            record.score_min = result

    @api.depends("measure_id")
    def _compute_score_max(self):
        """Copy the maximum score of the measure into the KPI."""
        for record in self:
            result = 120.0
            if record.measure_id:
                result = record.measure_id.score_max
            record.score_max = result

    @api.depends("polarity")
    def _compute_score_method(self):
        """Derive the score method from the polarity."""
        for record in self:
            result = "higher"
            if record.polarity:
                result = record.polarity
            record.score_method = result

    @api.depends(
        "target_ids.score",
        "target_ids.date_end",
        "target_ids.measurement_ids",
    )
    def _compute_score(self):
        """Take the score of the latest measured target.

        Targets without a measurement are ignored. The latest target is
        the one with the greatest end date, the greatest id breaking
        ties.
        """
        for record in self:
            result = 0.0
            measured = record.target_ids.filtered(lambda r: r.measurement_ids)
            if measured:
                latest = measured.sorted(key=lambda r: (r.date_end, r.id))[-1]
                result = latest.score
            record.score = result

    @api.onchange("measure_id")
    def onchange_score_range_ids(self):
        """Reload the score ranges from the selected measure."""
        result = [(5, 0, 0)]
        if self.measure_id:
            for score_range in self.measure_id.score_range_ids:
                result.append(
                    (
                        0,
                        0,
                        {
                            "min_value": score_range.min_value,
                            "max_value": score_range.max_value,
                            "score": score_range.score,
                        },
                    )
                )
        self.score_range_ids = result

    @api.constrains("is_key_result", "key_result_type")
    def _check_key_result_type(self):
        """Require a key result type on key results.

        :raises ValidationError: when the condition method returns False
        """
        for record in self.sudo():
            if not record._check_key_result_type_condition():
                error_message = """
Context: Create or update strategy KPI
Database ID: %s
Problem: Key results require a key result type.
Solution: Select a key result type or uncheck the key result flag
""" % (
                    record.id,
                )
                raise ValidationError(_(error_message))

    def _check_key_result_type_condition(self):
        """Tell whether a key result has its type.

        Extension point: override to relax or tighten the rule.

        :return: False only for a key result without a key result type
        """
        self.ensure_one()
        return not (self.is_key_result and not self.key_result_type)
