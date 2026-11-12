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
