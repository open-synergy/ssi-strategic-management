# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StrategyInitiativeMilestone(models.Model):
    """Represents a milestone of a strategic initiative.

    A milestone carries a weight; the progress of an initiative that
    uses the milestone method is the share of the weight of the
    completed milestones. The completion date is filled when the
    milestone is marked as done.
    """

    _name = "strategy_initiative.milestone"
    _description = "Strategy Initiative - Milestone"
    _order = "initiative_id, sequence, id"

    initiative_id = fields.Many2one(
        string="Initiative",
        comodel_name="strategy_initiative",
        required=True,
        ondelete="cascade",
        help="Initiative that this milestone belongs to.",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Order of the milestone inside the initiative.",
    )
    name = fields.Char(
        string="Name",
        required=True,
        help="Short description of the milestone.",
    )
    weight = fields.Float(
        string="Weight (%)",
        default=0.0,
        help="Share of the initiative that this milestone carries. The "
        "weights of the milestones must add up to 100% before the "
        "initiative starts.",
    )
    date_deadline = fields.Date(
        string="Deadline",
        help="Date by which the milestone should be completed.",
    )
    is_done = fields.Boolean(
        string="Done",
        default=False,
        help="Tick when the milestone has been completed.",
    )
    date_done = fields.Date(
        string="Date Done",
        compute="_compute_date_done",
        store=True,
        readonly=False,
        compute_sudo=True,
        help="Date on which the milestone was completed. It is filled "
        "when the milestone is ticked as done and can be adjusted.",
    )
    evidence = fields.Text(
        string="Evidence",
        help="Evidence that the milestone has been completed.",
    )

    @api.depends("is_done")
    def _compute_date_done(self):
        """Fill the completion date when the milestone is done.

        Ticking the milestone fills today's date, unticking it clears
        the date.
        """
        today = fields.Date.context_today(self)
        for record in self:
            result = today if record.is_done else False
            record.date_done = result
