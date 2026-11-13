# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0 only SavepointCase prepares
# ``cls.env`` in ``setUpClass``, which is where every work instruction
# Pre-Condition below is built.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiStrategyObjective(HttpSavepointCase):
    """Tour tests for the ``strategy_objective`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create one objective per tour, in the state its IK requires.

        ``base.user_admin`` is already a member of
        ``strategy_objective_validator_group`` (which implies the
        ``User`` and ``Viewer`` groups) and of
        ``strategy_objective_all_group`` through
        ``security/res_groups/strategy_objective.xml``, so it can run
        every tour below and can see every fixture. Each objective still
        gets an explicit ``user_id`` so that the record rule
        ``strategy_objective_internal_user_rule`` cannot hide it from the
        tour session. Every objective gets a department of its own: the
        department name is the only stable key to find its row in the
        list. The one plan of the class is the only record whose number
        starts with ``SP/``, which is how the create tour finds it.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        cls.perspective = cls.env.ref(
            "ssi_strategic_management.strategy_perspective_financial"
        )

        # Pre-Condition 10-cancel.md: the wizard lists the reasons of
        # ``ir.model.all_cancel_reason_ids``, so the fixture must be
        # global to show up regardless of demo data.
        cls.cancel_reason = (
            cls.env["base.cancel_reason"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Objective Cancel Reason",
                    "code": "TOUROBJCR",
                    "global_use": True,
                }
            )
        )

        # Pre-Condition of every IK: a plan that is On Progress.
        plan_type = (
            cls.env["strategy_plan_type"]
            .with_user(cls.admin)
            .create({"name": "Tour Objective Plan Type", "code": "TOUROBJPT"})
        )
        cls.plan = (
            cls.env["strategy_plan"]
            .with_user(cls.admin)
            .create(
                {
                    "title": "Fixture plan",
                    "type_id": plan_type.id,
                    "date_start": "2026-01-01",
                    "date_end": "2026-12-31",
                    "user_id": cls.admin.id,
                }
            )
        )
        cls._run_transition(cls.plan, "action_open")

        # Pre-Condition 01-create.md: a department to select. The tour
        # creates the objective itself.
        cls.dept_create = cls._create_department("Create")

        # Pre-Condition 02-edit.md: a measure to select and a Draft
        # objective. The tour adds the KPI, target and measurement.
        cls.measure = cls.env["strategy_measure"].create(
            {"name": "Tour Edit Measure", "code": "TOUREDITM"}
        )
        cls.objective_edit = cls._create_objective("Edit")

        # Pre-Condition 02-edit.md (Compute step): a KPI that uses an
        # automatic measure, with a saved target on which the Compute
        # button is shown. The weight stays 0 so that it never counts
        # in a KPI weight check.
        cls.measure_auto = cls.env["strategy_measure"].create(
            {
                "name": "Tour Auto Measure",
                "code": "TOURAUTOM",
                "realization_method": "python",
                "python_code": "result = 1.0",
            }
        )
        kpi_auto = cls.env["strategy_kpi"].create(
            {
                "objective_id": cls.objective_edit.id,
                "measure_id": cls.measure_auto.id,
                "name": "Tour Compute KPI",
                "weight": 0.0,
            }
        )
        cls.env["strategy_kpi.target"].create(
            {
                "kpi_id": kpi_auto.id,
                "date_start": "2026-01-01",
                "date_end": "2026-03-31",
                "target": 10.0,
            }
        )

        # Pre-Condition 07-start.md: Draft, with one KPI whose weight is
        # 100 so that the KPI weight check of the start action passes.
        cls.objective_start = cls._create_objective("Start")
        cls.env["strategy_kpi"].create(
            {
                "objective_id": cls.objective_start.id,
                "measure_id": cls.measure.id,
                "name": "Tour Start KPI",
                "weight": 100.0,
            }
        )

        # Pre-Condition 09-finish.md: On Progress.
        cls.objective_finish = cls._create_objective("Finish")
        cls._run_transition(cls.objective_finish, "action_open")

        # Pre-Condition 10-cancel.md: Draft, one of the states the
        # cancel policy allows.
        cls.objective_cancel = cls._create_objective("Cancel")

        # Pre-Condition 12-restart.md: Cancelled.
        cls.objective_restart = cls._create_objective("Reopen")
        cls._run_transition(cls.objective_restart, "action_cancel")

    @classmethod
    def _create_department(cls, label):
        """Create one department dedicated to a single tour.

        :param label: short scenario name, e.g. ``"Start"``
        :return: the new ``hr.department`` record whose name is
            ``"Tour Objective Dept <label>"``
        """
        return cls.env["hr.department"].create(
            {"name": "Tour Objective Dept %s" % label}
        )

    @classmethod
    def _create_objective(cls, label):
        """Create one Draft objective dedicated to a single tour.

        :param label: short scenario name, e.g. ``"Start"``
        :return: the new ``strategy_objective`` record, in Draft, whose
            department name is the key the tour uses to find its row
        """
        department = cls._create_department(label)
        return (
            cls.env["strategy_objective"]
            .with_user(cls.admin)
            .create(
                {
                    "title": "Fixture objective",
                    "plan_id": cls.plan.id,
                    "department_id": department.id,
                    "perspective_id": cls.perspective.id,
                    "user_id": cls.admin.id,
                }
            )
        )

    @classmethod
    def _run_transition(cls, record, method):
        """Advance a fixture record to the next state.

        The policy fields guarding each button are computed from
        ``policy.template`` against the state written by the previous
        transition, so the cache is dropped before every call.

        :param record: the record to advance
        :param method: name of the workflow method, e.g.
            ``"action_open"``
        """
        record.invalidate_cache()
        getattr(
            record.with_user(cls.admin).with_context(bypass_policy_check=True),
            method,
        )()

    def test_create(self):
        """Run the create tour for ``strategy_objective``.

        IK: docs/strategy_objective/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_strategic_management_strategy_objective_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``strategy_objective``.

        IK: docs/strategy_objective/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_strategic_management_strategy_objective_edit",
            login="admin",
        )

    def test_start(self):
        """Run the start tour for ``strategy_objective``.

        IK: docs/strategy_objective/07-start.md
        """
        self.start_tour(
            "/web",
            "ssi_strategic_management_strategy_objective_start",
            login="admin",
        )

    def test_finish(self):
        """Run the finish tour for ``strategy_objective``.

        IK: docs/strategy_objective/09-finish.md
        """
        self.start_tour(
            "/web",
            "ssi_strategic_management_strategy_objective_finish",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``strategy_objective``.

        IK: docs/strategy_objective/10-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_strategic_management_strategy_objective_cancel",
            login="admin",
        )

    def test_restart(self):
        """Run the restart tour for ``strategy_objective``.

        IK: docs/strategy_objective/12-restart.md
        """
        self.start_tour(
            "/web",
            "ssi_strategic_management_strategy_objective_restart",
            login="admin",
        )
