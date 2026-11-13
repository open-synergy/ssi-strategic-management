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

    realization_method = fields.Selection(
        string="Realization Method",
        selection=[
            ("manual", "Manual"),
            ("aggregate", "Aggregate (no code)"),
            ("python", "Python Code"),
        ],
        required=True,
        default="manual",
        help=(
            "How the realization of a KPI using this measure is obtained: "
            "Manual = recorded by hand, Aggregate (no code) = computed "
            "from Odoo data with a count, sum, average, minimum or "
            "maximum, Python Code = computed by the code below."
        ),
    )

    aggregate_model_id = fields.Many2one(
        string="Model",
        comodel_name="ir.model",
        ondelete="set null",
        help="Odoo model whose records are counted or aggregated.",
    )
    aggregate_domain = fields.Char(
        string="Domain",
        default="[]",
        help="Domain that selects the records of the model. Evaluated "
        "as Python; the period filter of the target is added to it.",
    )
    aggregate_date_field_id = fields.Many2one(
        string="Date Field",
        comodel_name="ir.model.fields",
        ondelete="set null",
        domain="[('model_id', '=', aggregate_model_id), "
        "('ttype', 'in', ['date', 'datetime'])]",
        help="Date or datetime field that places a record in the period "
        "of the target.",
    )
    aggregate_field_id = fields.Many2one(
        string="Value Field",
        comodel_name="ir.model.fields",
        ondelete="set null",
        domain="[('model_id', '=', aggregate_model_id), "
        "('ttype', 'in', ['integer', 'float', 'monetary'])]",
        help="Numeric stored field to aggregate. Not needed for count.",
    )
    aggregate_department_field_id = fields.Many2one(
        string="Department Field",
        comodel_name="ir.model.fields",
        ondelete="set null",
        domain="[('model_id', '=', aggregate_model_id), "
        "('ttype', '=', 'many2one'), ('relation', '=', 'hr.department')]",
        help="Many2one field to departments. When set, only records of "
        "the department of the objective are taken.",
    )
    aggregate_employee_field_id = fields.Many2one(
        string="Employee Field",
        comodel_name="ir.model.fields",
        ondelete="set null",
        domain="[('model_id', '=', aggregate_model_id), "
        "('ttype', '=', 'many2one'), ('relation', '=', 'hr.employee')]",
        help="Many2one field to employees. When set and the objective "
        "has an employee, only records of that employee are taken.",
    )
    aggregate_function = fields.Selection(
        string="Function",
        selection=[
            ("count", "Count"),
            ("sum", "Sum"),
            ("avg", "Average"),
            ("min", "Minimum"),
            ("max", "Maximum"),
        ],
        default="count",
        help="How the records are reduced to one number.",
    )
    use_ratio = fields.Boolean(
        string="Use Ratio",
        default=False,
        help="Check to divide the aggregate above by a second aggregate "
        "(the denominator) and express the result as a percentage.",
    )

    denominator_model_id = fields.Many2one(
        string="Denominator Model",
        comodel_name="ir.model",
        ondelete="set null",
        help="Odoo model whose records are counted or aggregated as the divisor.",
    )
    denominator_domain = fields.Char(
        string="Denominator Domain",
        default="[]",
        help="Domain that selects the records of the model. Evaluated "
        "as Python; the period filter of the target is added to it.",
    )
    denominator_date_field_id = fields.Many2one(
        string="Denominator Date Field",
        comodel_name="ir.model.fields",
        ondelete="set null",
        domain="[('model_id', '=', denominator_model_id), "
        "('ttype', 'in', ['date', 'datetime'])]",
        help="Date or datetime field that places a record in the period "
        "of the target.",
    )
    denominator_field_id = fields.Many2one(
        string="Denominator Value Field",
        comodel_name="ir.model.fields",
        ondelete="set null",
        domain="[('model_id', '=', denominator_model_id), "
        "('ttype', 'in', ['integer', 'float', 'monetary'])]",
        help="Numeric stored field to aggregate. Not needed for count.",
    )
    denominator_department_field_id = fields.Many2one(
        string="Denominator Department Field",
        comodel_name="ir.model.fields",
        ondelete="set null",
        domain="[('model_id', '=', denominator_model_id), "
        "('ttype', '=', 'many2one'), ('relation', '=', 'hr.department')]",
        help="Many2one field to departments. When set, only records of "
        "the department of the objective are taken.",
    )
    denominator_employee_field_id = fields.Many2one(
        string="Denominator Employee Field",
        comodel_name="ir.model.fields",
        ondelete="set null",
        domain="[('model_id', '=', denominator_model_id), "
        "('ttype', '=', 'many2one'), ('relation', '=', 'hr.employee')]",
        help="Many2one field to employees. When set and the objective "
        "has an employee, only records of that employee are taken.",
    )
    denominator_function = fields.Selection(
        string="Denominator Function",
        selection=[
            ("count", "Count"),
            ("sum", "Sum"),
            ("avg", "Average"),
            ("min", "Minimum"),
            ("max", "Maximum"),
        ],
        default="count",
        help="How the records are reduced to one number.",
    )
    python_code = fields.Text(
        string="Python Code",
        help="Python code that computes the realization. Assign the "
        "figure to the variable ``result``. Available variables: "
        "document (the KPI target), date_start, date_end, department, "
        "employee, company, env, time, datetime and dateutil.",
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

    @api.constrains(
        "realization_method",
        "aggregate_model_id",
        "aggregate_date_field_id",
        "aggregate_field_id",
        "aggregate_function",
    )
    def _check_aggregate_configuration(self):
        """Reject aggregate measures whose configuration is incomplete.

        :raises ValidationError: when the condition method returns False
        """
        for measure in self.sudo():
            if not measure._check_aggregate_configuration_condition():
                error_message = (
                    "\nContext: Create or update strategy measure\n"
                    "Database ID: %s\n"
                    "Problem: Aggregate measures require a model, a date "
                    "field and, except for count, a value field.\n"
                    "Solution: Fill the model, the date field and the value "
                    "field of the aggregate\n"
                ) % (measure.id,)
                raise ValidationError(_(error_message))

    def _check_aggregate_configuration_condition(self):
        """Tell whether an aggregate measure is completely configured.

        Extension point: override to relax or tighten the rule.

        :return: True when the measure is not an aggregate one, or when
            the model, the date field and, except for count, the value
            field are all set
        """
        self.ensure_one()
        if self.realization_method != "aggregate":
            return True
        return self._is_aggregate_complete("aggregate")

    @api.constrains(
        "realization_method",
        "use_ratio",
        "denominator_model_id",
        "denominator_date_field_id",
        "denominator_field_id",
        "denominator_function",
    )
    def _check_denominator_configuration(self):
        """Reject ratio measures whose denominator is incomplete.

        :raises ValidationError: when the condition method returns False
        """
        for measure in self.sudo():
            if not measure._check_denominator_configuration_condition():
                error_message = (
                    "\nContext: Create or update strategy measure\n"
                    "Database ID: %s\n"
                    "Problem: Ratio measures require a denominator model, "
                    "a date field and, except for count, a value field.\n"
                    "Solution: Fill the model, the date field and the value "
                    "field of the denominator\n"
                ) % (measure.id,)
                raise ValidationError(_(error_message))

    def _check_denominator_configuration_condition(self):
        """Tell whether the denominator of a ratio measure is complete.

        Extension point: override to relax or tighten the rule.

        :return: True when the measure is not an aggregate ratio, or
            when its denominator is completely configured
        """
        self.ensure_one()
        if self.realization_method != "aggregate" or not self.use_ratio:
            return True
        return self._is_aggregate_complete("denominator")

    @api.constrains(
        "aggregate_model_id",
        "aggregate_date_field_id",
        "aggregate_field_id",
        "aggregate_department_field_id",
        "aggregate_employee_field_id",
        "denominator_model_id",
        "denominator_date_field_id",
        "denominator_field_id",
        "denominator_department_field_id",
        "denominator_employee_field_id",
    )
    def _check_aggregate_field_model(self):
        """Reject measures whose fields belong to another model.

        :raises ValidationError: when the condition method returns False
        """
        for measure in self.sudo():
            if not measure._check_aggregate_field_model_condition():
                error_message = (
                    "\nContext: Create or update strategy measure\n"
                    "Database ID: %s\n"
                    "Problem: Aggregate fields must belong to the selected "
                    "model.\n"
                    "Solution: Select fields of the model of the aggregate "
                    "or of the denominator\n"
                ) % (measure.id,)
                raise ValidationError(_(error_message))

    def _check_aggregate_field_model_condition(self):
        """Tell whether every filled field belongs to its model.

        Extension point: override to relax or tighten the rule. Applies
        to the aggregate and to the denominator, whatever the
        realization method; empty fields are ignored.

        :return: True when each filled date, value, department and
            employee field has the model of its definition as model
        """
        self.ensure_one()
        suffixes = ("date_field", "field", "department_field", "employee_field")
        for prefix in ("aggregate", "denominator"):
            model = self["%s_model_id" % prefix]
            for suffix in suffixes:
                field = self["%s_%s_id" % (prefix, suffix)]
                if field and field.model_id != model:
                    return False
        return True

    def _is_aggregate_complete(self, prefix):
        """Tell whether one aggregate definition is completely filled.

        :param prefix: ``aggregate`` for the numerator or
            ``denominator`` for the divisor
        :return: True when the model and the date field are set and,
            unless the function is count, the value field is set too
        """
        self.ensure_one()
        result = bool(
            self["%s_model_id" % prefix] and self["%s_date_field_id" % prefix]
        )
        if result and self["%s_function" % prefix] != "count":
            result = bool(self["%s_field_id" % prefix])
        return result
