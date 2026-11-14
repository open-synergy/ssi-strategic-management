# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestStrategyKpiReport(YamlTransactionCase):
    """Cover the KPI scorecard, the objective scorecard and the tree.

    The related fields of the target are covered by the YAML scenarios.
    The Python tests read the groups that the pivot views ask the
    server for, and open every view and action of the reports.
    """

    def setUp(self):
        """Create two departments with scored objectives.

        Department A holds a financial objective whose KPI has a target
        in January (score 50) and one in February (score 100), and a
        financial objective without KPI. Department B holds a customer
        objective whose KPI has one target in January (score 50).

        :return: None
        """
        super().setUp()
        env = self.env
        perspective_fin = env.ref(
            "ssi_strategic_management.strategy_perspective_financial"
        )
        perspective_cus = env.ref(
            "ssi_strategic_management.strategy_perspective_customer"
        )
        self.dept_a = env["hr.department"].create({"name": "Report Test Dept A"})
        self.dept_b = env["hr.department"].create({"name": "Report Test Dept B"})
        plan_type = env["strategy_plan_type"].create(
            {
                "name": "Report test plan type",
                "code": "RPT%s" % self.dept_a.id,
                "methodology": "bsc",
                "cascade_level": "department",
            }
        )
        plan = env["strategy_plan"].create(
            {
                "title": "Fixture plan",
                "type_id": plan_type.id,
                "date_start": "2026-01-01",
                "date_end": "2026-12-31",
            }
        )
        measure = env["strategy_measure"].create(
            {
                "name": "Report test measure",
                "code": "RPM%s" % self.dept_a.id,
                "polarity": "higher",
                "aggregation": "sum",
            }
        )
        self.objective_a = self._create_objective(plan, self.dept_a, perspective_fin)
        self.objective_a2 = self._create_objective(plan, self.dept_a, perspective_fin)
        self.objective_b = self._create_objective(plan, self.dept_b, perspective_cus)
        self.target_a_jan = self._create_target(
            self.objective_a, measure, "2026-01-01", "2026-01-31", 100.0, 50.0
        )
        self.target_a_feb = self._create_target(
            self.objective_a, measure, "2026-02-01", "2026-02-28", 100.0, 100.0
        )
        self.target_b_jan = self._create_target(
            self.objective_b, measure, "2026-01-01", "2026-01-31", 200.0, 100.0
        )

    def test_strategy_kpi_report(self):
        """Run the report related fields and objective tree scenarios."""
        self.run_yaml_scenario("test_data_strategy_kpi_report.yaml")

    def _create_objective(self, plan, department, perspective):
        """Create an objective of a plan for a department.

        :param plan: the ``strategy_plan`` of the objective
        :param department: the ``hr.department`` it is cascaded to
        :param perspective: the ``strategy_perspective`` of the objective
        :return: the created ``strategy_objective``
        """
        return self.env["strategy_objective"].create(
            {
                "title": "Fixture objective",
                "plan_id": plan.id,
                "department_id": department.id,
                "perspective_id": perspective.id,
            }
        )

    def _create_target(
        self, objective, measure, date_start, date_end, target, realization
    ):
        """Create a measured target on a new KPI of an objective.

        :param objective: the ``strategy_objective`` that owns the KPI
        :param measure: the ``strategy_measure`` of the KPI
        :param date_start: first day of the target period
        :param date_end: last day of the target period
        :param target: value to reach in the period
        :param realization: manual value measured in the period
        :return: the created ``strategy_kpi.target``
        """
        kpi = objective.kpi_ids[:1]
        if not kpi:
            kpi = self.env["strategy_kpi"].create(
                {
                    "objective_id": objective.id,
                    "measure_id": measure.id,
                    "name": "Report test KPI %s" % objective.id,
                    "weight": 100.0,
                }
            )
        result = self.env["strategy_kpi.target"].create(
            {
                "kpi_id": kpi.id,
                "date_start": date_start,
                "date_end": date_end,
                "target": target,
            }
        )
        self.env["strategy_kpi.measurement"].create(
            {
                "target_id": result.id,
                "date": date_start,
                "manual_value": realization,
            }
        )
        return result

    def test_kpi_scorecard_groups_by_department_and_month(self):
        """Group the targets as the KPI scorecard pivot does.

        Pure Python - trigger P1 (L-01: the ``call`` action discards the
        return value of a method, here ``read_group``). The scores of a
        department are averaged and the final scores are summed.
        """
        targets = self.target_a_jan | self.target_a_feb | self.target_b_jan
        domain = [("id", "in", targets.ids)]
        by_department = self.env["strategy_kpi.target"].read_group(
            domain,
            ["score:avg", "final_score:sum", "realization:sum", "target:sum"],
            ["department_id"],
            orderby="department_id",
        )
        scores = {
            group["department_id"][0]: group
            for group in by_department
            if group["department_id"]
        }
        self.assertEqual(scores[self.dept_a.id]["score"], 75.0)
        self.assertEqual(scores[self.dept_a.id]["final_score"], 150.0)
        self.assertEqual(scores[self.dept_a.id]["realization"], 150.0)
        self.assertEqual(scores[self.dept_a.id]["target"], 200.0)
        self.assertEqual(scores[self.dept_b.id]["score"], 50.0)
        by_month = self.env["strategy_kpi.target"].read_group(
            domain + [("department_id", "=", self.dept_a.id)],
            ["score:avg"],
            ["date_start:month"],
        )
        self.assertEqual([group["score"] for group in by_month], [50.0, 100.0])
        by_perspective = self.env["strategy_kpi.target"].read_group(
            domain + [("department_id", "=", self.dept_a.id)],
            ["score:avg"],
            ["department_id", "perspective_id"],
            lazy=False,
        )
        self.assertEqual(len(by_perspective), 1)
        self.assertEqual(
            by_perspective[0]["perspective_id"][0],
            self.objective_a.perspective_id.id,
        )

    def test_objective_scorecard_averages_the_scores(self):
        """Group the objectives as the objective scorecard pivot does.

        Pure Python - trigger P1 (L-01: the ``call`` action discards the
        return value of a method, here ``read_group``). The score of a
        department and perspective is the mean of its objectives.
        """
        self.assertEqual(self.objective_a.score, 100.0)
        self.assertEqual(self.objective_a2.score, 0.0)
        objectives = self.objective_a | self.objective_a2 | self.objective_b
        groups = self.env["strategy_objective"].read_group(
            [("id", "in", objectives.ids)],
            ["score:avg"],
            ["department_id", "perspective_id"],
            lazy=False,
        )
        by_department = {group["department_id"][0]: group for group in groups}
        self.assertEqual(len(groups), 2)
        self.assertEqual(by_department[self.dept_a.id]["score"], 50.0)
        self.assertEqual(by_department[self.dept_b.id]["score"], 50.0)

    def test_report_views_and_actions_open(self):
        """Open every view of the three reports and read the menus.

        Pure Python - trigger P1 (L-01: the ``call`` action discards the
        return value of a method, here ``fields_view_get``). Each view
        type of an action must compile for the model of the action.
        """
        module = "ssi_strategic_management"
        expected = {
            "strategy_kpi_target_action": ["pivot", "graph", "tree"],
            "strategy_objective_scorecard_action": ["pivot", "graph", "tree"],
            "strategy_objective_tree_action": ["hierarchy", "tree", "form"],
        }
        for xml_id, view_types in expected.items():
            action = self.env.ref("%s.%s" % (module, xml_id))
            self.assertEqual(action.view_mode.split(","), view_types)
            for view_type in view_types:
                result = self.env[action.res_model].fields_view_get(view_type=view_type)
                self.assertEqual(result["type"], view_type)
        for xml_id in (
            "strategy_kpi_target_menu",
            "strategy_objective_scorecard_menu",
            "strategy_objective_tree_menu",
        ):
            menu = self.env.ref("%s.%s" % (module, xml_id))
            self.assertEqual(
                menu.parent_id,
                self.env.ref("%s.menu_strategic_management_reporting" % module),
            )
