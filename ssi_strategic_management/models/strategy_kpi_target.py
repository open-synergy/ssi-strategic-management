# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, time

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.safe_eval import safe_eval


class StrategyKpiTarget(models.Model):
    """Represents the target of a KPI for one period.

    A target holds the value to reach in a period, the manual
    measurements recorded during the period, the resulting realization
    and the score of that realization. The score follows the score
    method of the KPI and is expressed on the score scale of the plan
    type.

    The realization can also be computed automatically, by the
    aggregate engine (no code), by Python code, or by rolling up the
    same-period targets of the child KPIs, either on demand with the
    Compute button or on a schedule.
    """

    _name = "strategy_kpi.target"
    _inherit = ["mixin.localdict"]
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
    is_automatic = fields.Boolean(
        string="Automatic Realization",
        compute="_compute_is_automatic",
        compute_sudo=True,
        help="Checked when the realization of this target can be "
        "computed: the KPI is not manual, or it has child KPIs.",
    )
    final_score = fields.Float(
        string="Final Score",
        compute="_compute_final_score",
        store=True,
        compute_sudo=True,
        help="Score multiplied by the weight of the KPI.",
    )

    @api.depends("kpi_id.realization_method", "kpi_id.child_kpi_ids")
    def _compute_is_automatic(self):
        """Tell whether the realization of the target can be computed."""
        for record in self:
            result = False
            if record.kpi_id:
                result = bool(
                    record.kpi_id.realization_method != "manual"
                    or record.kpi_id.child_kpi_ids
                )
            record.is_automatic = result

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

    def action_compute_realization(self):
        """Compute the realization of the targets into an auto measurement.

        Creates the automatic measurement of the target, or updates its
        automatic value and date when it already exists, so that a
        target never holds more than one. The measurement is dated today,
        limited to the period of the target. A manual override of the
        measurement is kept.

        :raises UserError: when the KPI of a target is manual and has no
            child KPI
        """
        measurement_obj = self.env["strategy_kpi.measurement"]
        for record in self:
            if not record.is_automatic:
                error_message = """
Context: Compute KPI realization
Database ID: %s
Problem: Only automatic KPIs or KPIs with child KPIs can be computed.
Solution: Change the realization method of the KPI or add child KPIs
""" % (
                    record.id,
                )
                raise UserError(_(error_message))
            today = fields.Date.context_today(record)
            measure_date = max(min(today, record.date_end), record.date_start)
            vals = {
                "date": measure_date,
                "automatic_value": record._compute_automatic_value(),
            }
            automatic = record.measurement_ids.filtered(lambda r: r.mode == "auto")
            if automatic:
                automatic[0].write(vals)
            else:
                vals.update({"target_id": record.id, "mode": "auto"})
                measurement_obj.create(vals)

    def _compute_automatic_value(self):
        """Compute the automatic realization of the target.

        A KPI with child KPIs is always rolled up from them, whatever its
        realization method. Otherwise the aggregate engine or the Python
        code is used, following the realization method of the KPI.

        :return: the computed realization as a float; 0.0 for a manual
            KPI without child KPIs
        """
        self.ensure_one()
        kpi = self.kpi_id
        if kpi.child_kpi_ids:
            return self._compute_cascade_value()
        if kpi.realization_method == "aggregate":
            return self._compute_aggregate_value()
        if kpi.realization_method == "python":
            return self._compute_python_value()
        return 0.0

    def _compute_cascade_value(self):
        """Roll up the same-period targets of the child KPIs.

        The realizations are added when the aggregation of the KPI is
        ``sum`` and averaged otherwise.

        :return: the rolled up realization; 0.0 when no child target
            covers exactly the same period
        """
        self.ensure_one()
        children = self.sudo().search(
            [
                ("kpi_id", "in", self.kpi_id.child_kpi_ids.ids),
                ("date_start", "=", self.date_start),
                ("date_end", "=", self.date_end),
            ]
        )
        values = children.mapped("realization")
        if not values:
            return 0.0
        result = sum(values)
        if self.kpi_id.aggregation != "sum":
            result = result / len(values)
        return result

    def _compute_aggregate_value(self):
        """Compute the realization with the aggregate engine.

        With the ratio option the aggregate is divided by the
        denominator aggregate and expressed as a percentage; a zero
        denominator gives 0.0.

        :return: the aggregated realization as a float
        """
        self.ensure_one()
        measure = self.kpi_id.measure_id
        result = self._read_aggregate(measure, "aggregate")
        if measure.use_ratio:
            denominator = self._read_aggregate(measure, "denominator")
            result = result * 100.0 / denominator if denominator else 0.0
        return result

    def _read_aggregate(self, measure, prefix):
        """Read one aggregate definition of a measure over the period.

        The records are filtered by the domain of the definition, by the
        period of the target on the date field and, when the fields are
        set, by the department and the employee of the objective.

        :param measure: the ``strategy_measure`` holding the definition
        :param prefix: ``aggregate`` for the numerator or
            ``denominator`` for the divisor
        :return: the aggregated figure as a float; 0.0 when no record
            matches
        """
        self.ensure_one()
        model = self.env[measure["%s_model_id" % prefix].model].sudo()
        domain = safe_eval(
            measure["%s_domain" % prefix] or "[]",
            self._get_default_localdict(),
        )
        domain = list(domain) + self._get_period_domain(
            measure["%s_date_field_id" % prefix]
        )
        objective = self.objective_id
        department_field = measure["%s_department_field_id" % prefix]
        if department_field and objective.department_id:
            domain.append((department_field.name, "=", objective.department_id.id))
        employee_field = measure["%s_employee_field_id" % prefix]
        if employee_field and objective.employee_id:
            domain.append((employee_field.name, "=", objective.employee_id.id))
        function = measure["%s_function" % prefix]
        if function == "count":
            return float(model.read_group(domain, ["__count"], [])[0]["__count"])
        value_field = measure["%s_field_id" % prefix].name
        data = model.read_group(domain, ["%s:%s" % (value_field, function)], [])
        return float(data[0][value_field] or 0.0)

    def _get_period_domain(self, date_field):
        """Build the domain that keeps the records inside the period.

        A datetime field is compared from the start of the first day to
        the end of the last day of the period.

        :param date_field: the ``ir.model.fields`` date or datetime field
        :return: a list of two domain leaves
        """
        self.ensure_one()
        date_start = self.date_start
        date_end = self.date_end
        if date_field.ttype == "datetime":
            date_start = datetime.combine(date_start, time.min)
            date_end = datetime.combine(date_end, time(23, 59, 59))
        return [
            (date_field.name, ">=", date_start),
            (date_field.name, "<=", date_end),
        ]

    def _compute_python_value(self):
        """Compute the realization with the Python code of the KPI.

        The code assigns the figure to ``result``.

        :return: the value of ``result`` as a float
        :raises UserError: when the code fails
        """
        self.ensure_one()
        localdict = self._get_default_localdict()
        localdict["result"] = 0.0
        try:
            safe_eval(
                self.kpi_id.python_code or "", localdict, mode="exec", nocopy=True
            )
            result = float(localdict["result"] or 0.0)
        except Exception as error:  # pylint: disable=broad-except
            error_message = """
Context: Compute KPI realization
Database ID: %s
Problem: Error evaluating realization code: %s
Solution: Correct the Python code of the KPI
""" % (
                self.id,
                error,
            )
            raise UserError(_(error_message))
        return result

    def _get_default_localdict(self):
        """Extend the default local dict with the target context.

        :return: the dict of the mixin plus ``date_start``, ``date_end``,
            ``department``, ``employee`` and ``company``
        """
        self.ensure_one()
        result = super()._get_default_localdict()
        objective = self.objective_id
        result.update(
            {
                "date_start": self.date_start,
                "date_end": self.date_end,
                "department": objective.department_id,
                "employee": objective.employee_id,
                "company": objective.company_id or self.env.company,
            }
        )
        return result

    @api.model
    def _cron_compute_realization(self, frequency):
        """Queue the computation of the running automatic targets.

        One job is queued for each target whose period holds today,
        whose objective is in progress, and whose KPI is not manual (or
        has child KPIs) and uses a measure of the given frequency.

        :param frequency: ``monthly``, ``quarterly``, ``semesterly`` or
            ``yearly``
        """
        today = fields.Date.context_today(self)
        targets = self.search(
            [
                ("date_start", "<=", today),
                ("date_end", ">=", today),
                ("kpi_id.measure_id.frequency", "=", frequency),
                ("objective_id.state", "=", "open"),
                "|",
                ("kpi_id.realization_method", "!=", "manual"),
                ("kpi_id.child_kpi_ids", "!=", False),
            ]
        )
        for target in targets:
            target.with_delay().action_compute_realization()
