# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged

from odoo.addons.queue_job.tests.common import trap_jobs


@tagged("post_install", "-at_install")
class TestStrategyKpiCronOrder(YamlTransactionCase):
    """Cover the order of the realization jobs and the period time zone.

    The cron chains the jobs of the child KPIs before the jobs of the
    parent KPIs, and a datetime field is cut at midnight of the time
    zone of the company, of the user, or UTC.
    """

    def test_cron_jobs_run_children_before_parents(self):
        """Run the queued jobs by their graph and compare the rollup.

        Pure Python test, trigger P6 (L-15: the YAML runner cannot trap
        the queued jobs nor run them following their dependencies).
        """
        with trap_jobs() as trap:
            self.run_yaml_scenario("test_data_strategy_kpi_cron_order.yaml")
            trap.perform_enqueued_jobs()
        target_obj = self.env["strategy_kpi.target"]
        parent = target_obj.search([("kpi_id.name", "=", "Cascade parent KPI")])
        child = target_obj.search([("kpi_id.name", "=", "Cascade child KPI")])
        parent.invalidate_cache()
        child.invalidate_cache()
        self.assertEqual(child.realization, 2.0)
        self.assertEqual(parent.realization, child.realization)

    def test_cron_without_target_queues_no_job(self):
        """Queue nothing when no running target uses the frequency.

        Pure Python test, trigger P6 (L-15: the YAML runner cannot trap
        the queued jobs to count them).
        """
        target_obj = self.env["strategy_kpi.target"]
        self.assertFalse(target_obj.search([]))
        with trap_jobs() as trap:
            target_obj._cron_compute_realization("yearly")
            trap.assert_jobs_count(0)

    def test_period_domain_time_zone_fallback(self):
        """Return the datetime bounds of the period in each time zone.

        Pure Python test, trigger P1 (L-01: the ``call`` action discards
        the value returned by ``_get_period_domain``).
        """
        field = self.env["ir.model.fields"]._get("mail.message", "date")
        target = self.env["strategy_kpi.target"].new(
            {"date_start": date(2026, 3, 1), "date_end": date(2026, 3, 31)}
        )
        partner = self.env.company.partner_id
        partner.tz = "Asia/Jakarta"
        domain = target._get_period_domain(field)
        self.assertEqual(domain[0][2].isoformat(), "2026-02-28T17:00:00")
        self.assertEqual(domain[1][1], "<")
        self.assertEqual(domain[1][2].isoformat(), "2026-03-31T17:00:00")
        partner.tz = False
        self.env.user.tz = "Asia/Tokyo"
        domain = target._get_period_domain(field)
        self.assertEqual(domain[0][2].isoformat(), "2026-02-28T15:00:00")
        self.env.user.tz = False
        domain = target._get_period_domain(field)
        self.assertEqual(domain[0][2].isoformat(), "2026-03-01T00:00:00")
        self.assertEqual(domain[1][2].isoformat(), "2026-04-01T00:00:00")

    def test_period_domain_date_field(self):
        """Keep the plain dates of the period for a date field.

        Pure Python test, trigger P1 (L-01: the ``call`` action discards
        the value returned by ``_get_period_domain``).
        """
        field = self.env["ir.model.fields"]._get("hr.employee", "birthday")
        target = self.env["strategy_kpi.target"].new(
            {"date_start": date(2026, 3, 1), "date_end": date(2026, 3, 31)}
        )
        domain = target._get_period_domain(field)
        self.assertEqual(
            domain,
            [
                ("birthday", ">=", date(2026, 3, 1)),
                ("birthday", "<=", date(2026, 3, 31)),
            ],
        )
