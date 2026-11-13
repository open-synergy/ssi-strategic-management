# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StrategyPlanType(models.Model):
    """Represents a configuration profile for strategic plans.

    A plan type fixes the methodology of a plan (Balanced Scorecard or
    OKR), how deep objectives cascade into the organization, which score
    scale is used and which score category classifies the result.
    """

    _name = "strategy_plan_type"
    _inherit = ["mixin.master_data"]
    _description = "Strategy Plan Type"

    methodology = fields.Selection(
        string="Methodology",
        selection=[
            ("bsc", "Balanced Scorecard"),
            ("okr", "OKR"),
        ],
        required=True,
        default="bsc",
        help="Planning methodology that plans of this type follow.",
    )
    cascade_level = fields.Selection(
        string="Cascade Level",
        selection=[
            ("department", "Department"),
            ("employee", "Employee"),
        ],
        required=True,
        default="department",
        help=(
            "Deepest organization level objectives can be cascaded to: "
            "Department = stop at departments, "
            "Employee = continue down to employees."
        ),
    )
    score_scale = fields.Selection(
        string="Score Scale",
        selection=[
            ("percent", "Percentage (0-100+)"),
            ("okr", "OKR (0.0-1.0)"),
        ],
        required=True,
        default="percent",
        help="Scale in which scores of plans of this type are expressed.",
    )
    score_category_id = fields.Many2one(
        string="Score Category",
        comodel_name="strategy_score_category",
        ondelete="restrict",
        help="Score category used to classify scores of plans of this type.",
    )

    health_yellow_threshold = fields.Float(
        string="At-Risk Threshold (%)",
        default=10.0,
        help="Initiatives of plans of this type become At Risk when they "
        "are behind schedule by more than this number of percentage "
        "points.",
    )
    health_red_threshold = fields.Float(
        string="Off-Track Threshold (%)",
        default=25.0,
        help="Initiatives of plans of this type become Off Track when "
        "they are behind schedule by more than this number of "
        "percentage points.",
    )

    @api.constrains("health_yellow_threshold", "health_red_threshold")
    def _check_health_thresholds(self):
        """Reject an at-risk threshold above the off-track threshold.

        :raises ValidationError: when the condition method returns False
        """
        for plan_type in self.sudo():
            if not plan_type._check_health_thresholds_condition():
                error_message = """
Context: Create or update strategy plan type
Database ID: %s
Problem: The at-risk threshold must not exceed the off-track threshold.
Solution: Lower the at-risk threshold or raise the off-track threshold
""" % (
                    plan_type.id,
                )
                raise ValidationError(_(error_message))

    def _check_health_thresholds_condition(self):
        """Tell whether the health thresholds are consistent.

        Extension point: override to relax or tighten the rule.

        :return: True when the at-risk threshold does not exceed the
            off-track threshold
        """
        self.ensure_one()
        return self.health_yellow_threshold <= self.health_red_threshold

    @api.constrains("methodology", "score_scale")
    def _check_methodology_score_scale(self):
        """Reject OKR plan types that do not use the OKR score scale.

        :raises ValidationError: when the condition method returns False
        """
        for plan_type in self.sudo():
            if not plan_type._check_methodology_score_scale_condition():
                error_message = """
Context: Create or update strategy plan type
Database ID: %s
Problem: OKR plan types must use the OKR score scale.
Solution: Change score scale to OKR or change methodology
""" % (
                    plan_type.id,
                )
                raise ValidationError(_(error_message))

    def _check_methodology_score_scale_condition(self):
        """Tell whether methodology and score scale are compatible.

        Extension point: override to relax or tighten the rule.

        :return: True unless an OKR plan type uses a non OKR scale
        """
        self.ensure_one()
        if self.methodology != "okr":
            return True
        return self.score_scale == "okr"
