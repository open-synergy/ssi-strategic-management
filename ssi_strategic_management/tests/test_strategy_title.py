# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import importlib.util
import os

from odoo_yaml_test import YamlTransactionCase
from psycopg2 import IntegrityError

from odoo.modules.module import get_module_path
from odoo.tests import tagged
from odoo.tools import mute_logger

MODULE = "ssi_strategic_management"
TABLES = (
    "strategy_plan",
    "strategy_objective",
    "strategy_initiative",
    "strategy_review",
)


@tagged("post_install", "-at_install")
class TestStrategyTitle(YamlTransactionCase):
    """Cover the title of plan, objective, initiative and review.

    The positive display name scenarios live in YAML. This class holds
    the checks the YAML runner cannot express: the database level
    required constraint, the return value of ``name_search`` and the
    migration scripts of version 14.0.1.9.0.
    """

    def setUp(self):
        """Create one titled document of each of the four models.

        :return: None
        """
        super().setUp()
        env = self.env
        self.plan_type = env["strategy_plan_type"].create(
            {
                "name": "Title test plan type",
                "code": "TTL%s" % env["strategy_plan_type"].search_count([]),
                "methodology": "bsc",
                "cascade_level": "department",
            }
        )
        self.department = env["hr.department"].create({"name": "Title Test Dept"})
        self.perspective = env.ref(
            "ssi_strategic_management.strategy_perspective_financial"
        )
        self.plan = env["strategy_plan"].create(self._vals("strategy_plan", True))
        self.objective = env["strategy_objective"].create(
            self._vals("strategy_objective", True)
        )
        self.initiative = env["strategy_initiative"].create(
            self._vals("strategy_initiative", True)
        )
        self.review = env["strategy_review"].create(self._vals("strategy_review", True))

    def _vals(self, model, with_title, title="Growth"):
        """Return valid create values for a model.

        :param model: technical name of one of the four models
        :param with_title: whether the ``title`` key is included
        :param title: the title to write when it is included
        :return: dict of values for ``create``
        """
        vals = {}
        if model == "strategy_plan":
            vals = {
                "type_id": self.plan_type.id,
                "date_start": "2026-01-01",
                "date_end": "2026-12-31",
            }
        elif model == "strategy_objective":
            vals = {
                "plan_id": self.plan.id,
                "department_id": self.department.id,
                "perspective_id": self.perspective.id,
            }
        elif model == "strategy_initiative":
            vals = {
                "plan_id": self.plan.id,
                "department_id": self.department.id,
                "progress_method": "manual",
                "date_start": "2026-01-01",
                "date_end": "2026-12-31",
            }
        elif model == "strategy_review":
            vals = {
                "plan_id": self.plan.id,
                "date_start": "2026-01-01",
                "date_end": "2026-03-31",
            }
        if with_title:
            vals["title"] = title
        return vals

    def test_title_is_required(self):
        """Reject a create without title in all four models.

        Pure Python because of P5 and L-22: a ``required`` column without
        a value fails in PostgreSQL with ``IntegrityError``, which
        ``expect_error`` does not know.
        """
        for model in TABLES:
            vals = self._vals(model, False)
            with mute_logger("odoo.sql_db"):
                with self.assertRaises(IntegrityError) as ctx:
                    with self.env.cr.savepoint():
                        self.env[model].create(vals)
            self.assertEqual(ctx.exception.diag.column_name, "title", model)

    def test_name_search_finds_title(self):
        """Find each document from a fragment of its title.

        Pure Python because of P1 and L-01: ``action: call`` drops the
        return value of ``name_search``, so the YAML runner cannot assert
        on it.
        """
        for record in (self.plan, self.objective, self.initiative, self.review):
            found = self.env[record._name].name_search("Grow")
            self.assertIn(record.id, [item[0] for item in found], record._name)
            missing = self.env[record._name].name_search("No such title")
            self.assertNotIn(record.id, [item[0] for item in missing], record._name)

    def _load_script(self, filename):
        """Load a migration script of version 14.0.1.9.0 from its file.

        :param filename: ``pre-migration.py`` or ``post-migration.py``
        :return: the loaded module
        """
        path = os.path.join(
            get_module_path(MODULE), "migrations", "14.0.1.9.0", filename
        )
        spec = importlib.util.spec_from_file_location(
            "ssi_strategic_management_%s" % filename.replace("-", "_"), path
        )
        script = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(script)
        return script

    def test_pre_migration_copies_name_into_title(self):
        """Fill a NULL title with the document number.

        Pure Python because of P10 and L-11: the script must be loaded
        from its file, which ``EVAL:`` cannot do.
        """
        cr = self.env.cr
        self.env["strategy_plan"].flush()
        for index, table in enumerate(TABLES):
            cr.execute("ALTER TABLE %s ALTER COLUMN title DROP NOT NULL" % table)
            cr.execute(
                "UPDATE %s SET title = NULL, name = %%s" % table,
                ("MIG-%s" % index,),
            )
        self._load_script("pre-migration.py").migrate(cr, "14.0.1.8.1")
        for index, table in enumerate(TABLES):
            cr.execute(
                "SELECT title FROM %s" % table + " WHERE name = %s", ("MIG-%s" % index,)
            )
            self.assertEqual(cr.fetchone()[0], "MIG-%s" % index, table)

    def test_post_migration_rebuilds_display_name(self):
        """Rebuild a stale stored display name from number and title.

        Pure Python because of P10 and L-11: the script must be loaded
        from its file, which ``EVAL:`` cannot do.
        """
        cr = self.env.cr
        self.env["strategy_plan"].flush()
        for table in TABLES:
            cr.execute("UPDATE %s SET display_name = 'stale'" % table)
        for model in TABLES:
            self.env[model].invalidate_cache()
        self._load_script("post-migration.py").migrate(cr, "14.0.1.8.1")
        for model in TABLES:
            self.env[model].invalidate_cache()
        for record in (self.plan, self.objective, self.initiative, self.review):
            self.assertEqual(record.display_name, "Growth", record._name)
