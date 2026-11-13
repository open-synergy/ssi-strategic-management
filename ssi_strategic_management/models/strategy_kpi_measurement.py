# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StrategyKpiMeasurement(models.Model):
    """Represents one realization recorded for a KPI target.

    A measurement holds the value observed on a date within the period
    of its target. The value is entered manually; the ``value`` field
    carries the figure that the target rolls up, so that other ways of
    measuring can extend it later.
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
    manual_value = fields.Float(
        string="Value",
        default=0.0,
        help="Value entered manually.",
    )
    value = fields.Float(
        string="Measured Value",
        compute="_compute_value",
        store=True,
        compute_sudo=True,
        help="Value that the target rolls up. Equals the manual value.",
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

    @api.depends("manual_value")
    def _compute_value(self):
        """Take the manual value as the measured value."""
        for record in self:
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
