# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.8.1 -> 14.0.1.9.0
#
# Changes: plan, objective, initiative and review gain a required
#          ``title`` column. The ORM adds the NOT NULL constraint when it
#          loads the field, which fails on existing rows unless every
#          row already has a value. The title of an old record is copied
#          from its document number.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

TABLES = (
    "strategy_plan",
    "strategy_objective",
    "strategy_initiative",
    "strategy_review",
)


@openupgrade.migrate()
def migrate(env, version):
    """Add the ``title`` column and fill it from the document number.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; updates the ``title`` column of the four tables
    """
    cr = env.cr
    for table in TABLES:
        openupgrade.logged_query(
            cr,
            "ALTER TABLE %s ADD COLUMN IF NOT EXISTS title VARCHAR" % table,
        )
        rows = openupgrade.logged_query(
            cr,
            "UPDATE %s SET title = name WHERE title IS NULL" % table,
        )
        _logger.info("Filled title on %s row(s) of %s.", rows, table)
