# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StrategyKpiTarget(models.Model):
    """Represents the target of a KPI for one period.

    A target holds the value to reach in a period, the manual
    measurements recorded during the period, the resulting realization
    and the score of that realization. The score follows the score
    method of the KPI and is expressed on the score scale of the plan
    type.
    """

    _name = "strategy_kpi.target"
    _description = "Strategy KPI - Target"
    _order = "kpi_id, date_start, id"

    name = fields.Char(
        string="Name",
        compute="_compute_name",
        store=True,
        compute_sudo=True,
        help="Name of the target, built from the KPI and the period.",
    )
    kpi_id = fields.Many2one(
        string="KPI",
        comodel_name="strategy_kpi",
        required=True,
        ondelete="cascade",
        help="KPI that this target belongs to.",
    )
    objective_id = fields.Many2one(
        string="Objective",
        related="kpi_id.objective_id",
        store=True,
        compute_sudo=True,
        help="Strategy objective of the KPI.",
    )
    date_range_id = fields.Many2one(
        string="Period",
        comodel_name="date.range",
        ondelete="restrict",
        help="Date range that fills the start and end date of the " "target.",
    )
    date_start = fields.Date(
        string="Date Start",
        required=True,
        help="First day of the target period.",
    )
    date_end = fields.Date(
        string="Date End",
        required=True,
        help="Last day of the target period.",
    )
    target = fields.Float(
        string="Target",
        compute="_compute_target",
        store=True,
        readonly=False,
        compute_sudo=True,
        help="Value to reach in the period. Proposed from the default "
        "target of the KPI and editable.",
    )
    measurement_ids = fields.One2many(
        string="Measurements",
        comodel_name="strategy_kpi.measurement",
        inverse_name="target_id",
        help="Realizations recorded for this target.",
    )
    realization = fields.Float(
        string="Realization",
        compute="_compute_realization",
        store=True,
        compute_sudo=True,
        help="Value of the measurements rolled up with the aggregation "
        "of the KPI. 0 when there is no measurement.",
    )
    score = fields.Float(
        string="Score",
        compute="_compute_score",
        store=True,
        compute_sudo=True,
        help="Score of the realization against the target, following "
        "the score method of the KPI.",
    )
    final_score = fields.Float(
        string="Final Score",
        compute="_compute_final_score",
        store=True,
        compute_sudo=True,
        help="Score multiplied by the weight of the KPI.",
    )

    @api.depends("kpi_id.name", "date_start", "date_end")
    def _compute_name(self):
        """Build the name of the target from the KPI and the period."""
        for record in self:
            result = "/"
            if record.kpi_id:
                result = "%s (%s - %s)" % (
                    record.kpi_id.name,
                    record.date_start or "",
                    record.date_end or "",
                )
            record.name = result

    @api.depends("kpi_id")
    def _compute_target(self):
        """Propose the default target of the KPI."""
        for record in self:
            result = 0.0
            if record.kpi_id:
                result = record.kpi_id.target
            record.target = result

    @api.depends(
        "kpi_id.aggregation",
        "measurement_ids.value",
        "measurement_ids.date",
    )
    def _compute_realization(self):
        """Roll the measurements up with the aggregation of the KPI.

        ``sum`` adds the values, ``avg`` takes their mean and ``last``
        takes the value of the measurement with the latest date, the
        greatest id breaking ties.
        """
        for record in self:
            result = 0.0
            measurements = record.measurement_ids
            if measurements:
                aggregation = record.kpi_id.aggregation
                if aggregation == "sum":
                    result = sum(measurements.mapped("value"))
                elif aggregation == "avg":
                    result = sum(measurements.mapped("value")) / len(measurements)
                else:
                    ordered = measurements.sorted(key=lambda r: (r.date, r.id))
                    result = ordered[-1].value
            record.realization = result

    @api.depends(
        "realization",
        "target",
        "kpi_id.score_method",
        "kpi_id.score_min",
        "kpi_id.score_max",
        "kpi_id.score_range_ids.min_value",
        "kpi_id.score_range_ids.max_value",
        "kpi_id.score_range_ids.score",
        "kpi_id.objective_id.plan_id.type_id.score_scale",
    )
    def _compute_score(self):
        """Score the realization against the target.

        The raw score depends on the score method of the KPI: higher is
        better gives ``realization / target * 100`` (0 for a target of
        0), lower is better gives ``target / realization * 100`` (the
        maximum score for a realization of 0) and within range gives the
        score of the range that contains the realization (0 when none
        does). It is then clamped to the score limits of the KPI. On a
        plan type with the OKR score scale the result is divided by 100
        and clamped to 0.0 - 1.0.
        """
        for record in self:
            kpi = record.kpi_id
            result = 0.0
            method = kpi.score_method
            if method == "higher":
                if record.target:
                    result = record.realization * 100.0 / record.target
            elif method == "lower":
                if record.realization:
                    result = record.target * 100.0 / record.realization
                else:
                    result = kpi.score_max
            elif method == "range":
                for score_range in kpi.score_range_ids.sorted(
                    key=lambda r: (r.min_value, r.id)
                ):
                    if (
                        score_range.min_value
                        <= record.realization
                        <= score_range.max_value
                    ):
                        result = score_range.score
                        break
            if method:
                result = min(max(result, kpi.score_min), kpi.score_max)
            scale = kpi.objective_id.plan_id.type_id.score_scale
            if scale == "okr":
                result = min(max(result / 100.0, 0.0), 1.0)
            record.score = result

    @api.depends("score", "kpi_id.weight")
    def _compute_final_score(self):
        """Multiply the score by the weight of the KPI."""
        for record in self:
            result = record.score * record.kpi_id.weight / 100.0
            record.final_score = result

    @api.onchange("date_range_id")
    def onchange_date_start(self):
        """Fill the start date from the selected date range."""
        if self.date_range_id:
            self.date_start = self.date_range_id.date_start

    @api.onchange("date_range_id")
    def onchange_date_end(self):
        """Fill the end date from the selected date range."""
        if self.date_range_id:
            self.date_end = self.date_range_id.date_end

    @api.constrains("kpi_id", "date_start", "date_end")
    def _check_plan_period(self):
        """Reject targets outside the period of the plan.

        :raises ValidationError: when the condition method returns False
        """
        for record in self.sudo():
            if not record._check_plan_period_condition():
                error_message = """
Context: Create or update KPI target
Database ID: %s
Problem: Target period must be within the plan period.
Solution: Change the start or end date of the target
""" % (
                    record.id,
                )
                raise ValidationError(_(error_message))

    def _check_plan_period_condition(self):
        """Tell whether the target period lies inside the plan period.

        Extension point: override to relax or tighten the rule.

        :return: True when the target period lies inside it
        """
        self.ensure_one()
        plan = self.kpi_id.objective_id.plan_id
        return plan.date_start <= self.date_start and self.date_end <= plan.date_end

    @api.constrains("kpi_id", "date_start", "date_end")
    def _check_period_overlap(self):
        """Reject targets that overlap another target of the same KPI.

        :raises ValidationError: when the condition method returns False
        """
        for record in self.sudo():
            if not record._check_period_overlap_condition():
                error_message = """
Context: Create or update KPI target
Database ID: %s
Problem: Target periods of a KPI must not overlap.
Solution: Change the start or end date of the target
""" % (
                    record.id,
                )
                raise ValidationError(_(error_message))

    def _check_period_overlap_condition(self):
        """Tell whether no other target of the KPI shares days with this one.

        Extension point: override to relax or tighten the rule.

        :return: True when the period does not overlap the period of any
            other target of the same KPI
        """
        self.ensure_one()
        result = True
        for other in self.kpi_id.target_ids - self:
            if other.date_start <= self.date_end and self.date_start <= other.date_end:
                result = False
                break
        return result
