# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0 only SavepointCase prepares
# ``cls.env`` in ``setUpClass``, which is where every work instruction
# Pre-Condition below is built.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiStrategyPlan(HttpSavepointCase):
    """Tour tests for the ``strategy_plan`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create one plan per tour, in the state its IK requires.

        ``base.user_admin`` is already a member of
        ``strategy_plan_validator_group`` (which implies the ``User`` and
        ``Viewer`` groups) and of ``strategy_plan_all_group`` through
        ``security/res_groups/strategy_plan.xml``, so it can run every
        tour below and can see every fixture. Each plan still gets an
        explicit ``user_id`` so that the record rule
        ``strategy_plan_internal_user_rule`` cannot hide it from the tour
        session. Every plan gets a plan type of its own: the type name is
        the only stable key to find its row in the list.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")

        # Pre-Condition 10-cancel.md: the wizard lists the reasons of
        # ``ir.model.all_cancel_reason_ids``, so the fixture must be
        # global to show up regardless of demo data.
        cls.cancel_reason = (
            cls.env["base.cancel_reason"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Plan Cancel Reason",
                    "code": "TOURPLANCR",
                    "global_use": True,
                }
            )
        )

        # Pre-Condition 01-create.md: a plan type to select. The tour
        # creates the plan itself.
        cls.type_create = cls._create_plan_type("Create")

        # Pre-Condition 04-confirm.md: Draft.
        cls.plan_confirm = cls._create_plan("Confirm")

        # Pre-Condition 05-approve.md: Waiting for Approval, with
        # ``admin`` among the record's active approvers -- the standard
        # approval.template routes approval to
        # ``strategy_plan_validator_group``.
        cls.plan_approve = cls._create_plan("Approve")
        cls._run_transition(cls.plan_approve, "action_confirm")

        # Pre-Condition 07-start.md: Waiting for Approval and fully
        # approved.
        cls.plan_start = cls._create_plan("Start")
        cls._run_transition(cls.plan_start, "action_confirm")
        cls._run_transition(cls.plan_start, "action_approve_approval")

        # Pre-Condition 09-finish.md: On Progress.
        cls.plan_finish = cls._create_plan("Finish")
        cls._run_transition(cls.plan_finish, "action_confirm")
        cls._run_transition(cls.plan_finish, "action_approve_approval")
        cls._run_transition(cls.plan_finish, "action_open")

        # Pre-Condition 10-cancel.md: Draft, one of the states the
        # cancel policy allows.
        cls.plan_cancel = cls._create_plan("Cancel")

        # Pre-Condition 12-restart.md: Cancelled.
        cls.plan_restart = cls._create_plan("Reopen")
        cls._run_transition(cls.plan_restart, "action_cancel")

        # Pre-Condition 14-restart-approval.md: Waiting for Approval with
        # no approval.template assigned. The standard template is cleared
        # on the fixture the way a plan stuck without approvers looks.
        cls.plan_restart_approval = cls._create_plan("Restart Approval")
        cls._run_transition(cls.plan_restart_approval, "action_confirm")
        cls.plan_restart_approval.invalidate_cache()
        cls.plan_restart_approval.sudo().write({"approval_template_id": False})

    @classmethod
    def _create_plan_type(cls, label):
        """Create one plan type dedicated to a single tour.

        :param label: short scenario name, e.g. ``"Confirm"``
        :return: the new ``strategy_plan_type`` record whose name is
            ``"Tour Plan Type <label>"``
        """
        return (
            cls.env["strategy_plan_type"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Plan Type %s" % label,
                    "code": "TOURPT%s" % label.upper().replace(" ", ""),
                }
            )
        )

    @classmethod
    def _create_plan(cls, label):
        """Create one Draft plan dedicated to a single tour.

        :param label: short scenario name, e.g. ``"Confirm"``
        :return: the new ``strategy_plan`` record, in Draft, whose plan
            type name is the key the tour uses to find its row
        """
        plan_type = cls._create_plan_type(label)
        return (
            cls.env["strategy_plan"]
            .with_user(cls.admin)
            .create(
                {
                    "type_id": plan_type.id,
                    "date_start": "2026-01-01",
                    "date_end": "2026-12-31",
                    "user_id": cls.admin.id,
                }
            )
        )

    @classmethod
    def _run_transition(cls, plan, method):
        """Advance a fixture plan to the next state.

        The policy fields guarding each button are computed from
        ``policy.template`` against the state written by the previous
        transition, so the cache is dropped before every call.

        :param plan: the ``strategy_plan`` record to advance
        :param method: name of the workflow method, e.g.
            ``"action_confirm"``
        """
        plan.invalidate_cache()
        getattr(
            plan.with_user(cls.admin).with_context(bypass_policy_check=True),
            method,
        )()

    def test_create(self):
        """Run the create tour for ``strategy_plan``.

        IK: docs/strategy_plan/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_strategic_management_strategy_plan_create",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``strategy_plan``.

        IK: docs/strategy_plan/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_strategic_management_strategy_plan_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for ``strategy_plan``.

        IK: docs/strategy_plan/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_strategic_management_strategy_plan_approve",
            login="admin",
        )

    def test_start(self):
        """Run the start tour for ``strategy_plan``.

        IK: docs/strategy_plan/07-start.md
        """
        self.start_tour(
            "/web",
            "ssi_strategic_management_strategy_plan_start",
            login="admin",
        )

    def test_finish(self):
        """Run the finish tour for ``strategy_plan``.

        IK: docs/strategy_plan/09-finish.md
        """
        self.start_tour(
            "/web",
            "ssi_strategic_management_strategy_plan_finish",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``strategy_plan``.

        IK: docs/strategy_plan/10-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_strategic_management_strategy_plan_cancel",
            login="admin",
        )

    def test_restart(self):
        """Run the restart tour for ``strategy_plan``.

        IK: docs/strategy_plan/12-restart.md
        """
        self.start_tour(
            "/web",
            "ssi_strategic_management_strategy_plan_restart",
            login="admin",
        )

    def test_restart_approval(self):
        """Run the restart approval tour for ``strategy_plan``.

        IK: docs/strategy_plan/14-restart-approval.md
        """
        self.start_tour(
            "/web",
            "ssi_strategic_management_strategy_plan_restart_approval",
            login="admin",
        )
