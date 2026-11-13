# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StrategyReviewLine(models.Model):
    """Represents one snapshot line of a strategy review.

    A line copies the figures of an objective, of a KPI target or of an
    initiative at the time the snapshot was taken. The figures are plain
    copies, not related or computed fields, so they stay as they were
    when their sources change. Only the comment and the corrective
    action are written by the reviewers.
    """

    _name = "strategy_review.line"
    _description = "Strategy Review - Line"
    _order = "review_id, id"

    review_id = fields.Many2one(
        string="Review",
        comodel_name="strategy_review",
        required=True,
        ondelete="cascade",
        help="Review that this line belongs to.",
    )
    line_type = fields.Selection(
        string="Type",
        selection=[
            ("objective", "Objective"),
            ("kpi", "KPI"),
            ("initiative", "Initiative"),
        ],
        required=True,
        help="What this line reviews: an objective, a KPI or an " "initiative.",
    )
    objective_id = fields.Many2one(
        string="Objective",
        comodel_name="strategy_objective",
        ondelete="set null",
        help="Objective that is reviewed, or the objective of the " "reviewed KPI.",
    )
    kpi_id = fields.Many2one(
        string="KPI",
        comodel_name="strategy_kpi",
        ondelete="set null",
        help="KPI that is reviewed.",
    )
    initiative_id = fields.Many2one(
        string="Initiative",
        comodel_name="strategy_initiative",
        ondelete="set null",
        help="Initiative that is reviewed.",
    )
    target = fields.Float(
        string="Target",
        help="Target of the KPI at the time of the snapshot.",
    )
    realization = fields.Float(
        string="Realization",
        help="Realization of the KPI target at the time of the snapshot.",
    )
    score = fields.Float(
        string="Score",
        help="Score of the objective or of the KPI target at the time of "
        "the snapshot.",
    )
    progress = fields.Float(
        string="Progress (%)",
        help="Progress of the initiative at the time of the snapshot.",
    )
    health = fields.Selection(
        string="Health",
        selection=[
            ("green", "On Track"),
            ("yellow", "At Risk"),
            ("red", "Off Track"),
        ],
        help="Health of the initiative at the time of the snapshot.",
    )
    comment = fields.Text(
        string="Comment",
        help="Observation of the reviewers about this line.",
    )
    corrective_action = fields.Text(
        string="Corrective Action",
        help="Action decided to correct the gap found on this line. It "
        "can be written while the review is a draft or waiting for "
        "approval.",
    )
