# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StrategyKpiMeasurement(models.Model):
    """Represents one realization recorded for a KPI target.

    A measurement holds the value observed on a date within the period
    of its target. The value is either entered manually (``manual``
    mode) or computed by the realization engine of the KPI (``auto``
    mode). An automatic value can be overridden by a manual one, which
    then requires a dissenting note. The ``value`` field carries the
    figure that the target rolls up.
    """

    _name = "strategy_kpi.measurement"
    _description = "Strategy KPI - Measurement"
    _order = "target_id, date, id"

    target_id = fields.Many2one(
        string="Target",
        comodel_name="strategy_kpi.target",
        required=True,
        ondelete="cascade",
        help="Target that this measurement is recorded for.",
    )
    kpi_id = fields.Many2one(
        string="KPI",
        related="target_id.kpi_id",
        store=True,
        compute_sudo=True,
        help="KPI of the target.",
    )
    date = fields.Date(
        string="Date",
        required=True,
        default=fields.Date.context_today,
        help="Date that the value was observed. It must lie within the "
        "period of the target.",
    )
    mode = fields.Selection(
        string="Mode",
        selection=[
            ("manual", "Manual"),
            ("auto", "Automatic"),
        ],
        default="manual",
        readonly=True,
        help="Manual = entered by a user, Automatic = computed by the "
        "realization engine of the KPI.",
    )
    manual_value = fields.Float(
        string="Value",
        default=0.0,
        help="Value entered manually. For an automatic measurement it "
        "only counts when the automatic value is overridden.",
    )
    automatic_value = fields.Float(
        string="Automatic Value",
        default=0.0,
        readonly=True,
        help="Value computed by the realization engine of the KPI.",
    )
    override_automatic = fields.Boolean(
        string="Override Automatic Value",
        default=False,
        help="Check to use the manual value instead of the automatic "
        "value. A dissenting note is then required.",
    )
    dissenting_note = fields.Text(
        string="Dissenting Note",
        help="Reason why the automatic value is overridden.",
    )
    value = fields.Float(
        string="Measured Value",
        compute="_compute_value",
        store=True,
        compute_sudo=True,
        help="Value that the target rolls up. The manual value for a "
        "manual measurement or an overridden automatic one, otherwise "
        "the automatic value.",
    )
    user_id = fields.Many2one(
        string="Recorded By",
        comodel_name="res.users",
        default=lambda self: self.env.user,
        ondelete="restrict",
        help="User who recorded the measurement.",
    )
    note = fields.Text(
        string="Note",
        help="Remark about the measurement.",
    )

    @api.depends("mode", "manual_value", "automatic_value", "override_automatic")
    def _compute_value(self):
        """Pick the manual or the automatic value as the measured value.

        The manual value counts for a manual measurement and for an
        automatic one whose value is overridden; otherwise the automatic
        value counts.
        """
        for record in self:
            result = record.automatic_value
            if record.mode == "manual" or record.override_automatic:
                result = record.manual_value
            record.value = result

    @api.constrains("target_id", "date")
    def _check_date_in_period(self):
        """Reject measurements dated outside the period of the target.

        :raises ValidationError: when the condition method returns False
        """
        for record in self.sudo():
            if not record._check_date_in_period_condition():
                error_message = """
Context: Create or update KPI measurement
Database ID: %s
Problem: Measurement date must be within the target period.
Solution: Change the date of the measurement
""" % (
                    record.id,
                )
                raise ValidationError(_(error_message))

    def _check_date_in_period_condition(self):
        """Tell whether the date lies inside the period of the target.

        Extension point: override to relax or tighten the rule.

        :return: True when the date is between the start and the end
            date of the target
        """
        self.ensure_one()
        target = self.target_id
        return target.date_start <= self.date <= target.date_end

    @api.constrains("mode", "override_automatic", "dissenting_note")
    def _check_dissenting_note(self):
        """Require a dissenting note on an overridden automatic value.

        :raises ValidationError: when the condition method returns False
        """
        for record in self.sudo():
            if not record._check_dissenting_note_condition():
                error_message = """
Context: Create or update KPI measurement
Database ID: %s
Problem: A dissenting note is required when overriding an automatic value.
Solution: Type a dissenting note or uncheck the override
""" % (
                    record.id,
                )
                raise ValidationError(_(error_message))

    def _check_dissenting_note_condition(self):
        """Tell whether an overridden automatic value is justified.

        Extension point: override to relax or tighten the rule.

        :return: False only for an automatic measurement that overrides
            its automatic value without a dissenting note
        """
        self.ensure_one()
        return not (
            self.mode == "auto" and self.override_automatic and not self.dissenting_note
        )
