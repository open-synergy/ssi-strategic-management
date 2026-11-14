# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.8.1 -> 14.0.1.9.0
#
# Changes: the stored display name now depends on the title as well as
#          on the document number, so the stored value of every existing
#          record is stale and must be rebuilt.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

MODELS = (
    "strategy_plan",
    "strategy_objective",
    "strategy_initiative",
    "strategy_review",
)


@openupgrade.migrate()
def migrate(env, version):
    """Recompute the stored ``display_name`` of the four models.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; recomputes ``display_name`` of every record
    """
    for model in MODELS:
        records = env[model].with_context(active_test=False).search([])
        env.add_to_compute(records._fields["display_name"], records)
        records.flush(["display_name"])
        _logger.info(
            "Recomputed display_name on %s record(s) of %s.", len(records), model
        )
