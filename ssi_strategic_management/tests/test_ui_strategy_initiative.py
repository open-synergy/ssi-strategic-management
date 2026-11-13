# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0 only SavepointCase prepares
# ``cls.env`` in ``setUpClass``, which is where every work instruction
# Pre-Condition below is built.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiStrategyInitiative(HttpSavepointCase):
    """Tour tests for the ``strategy_initiative`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create one initiative per tour, in the state its IK requires.

        ``base.user_admin`` is already a member of
        ``strategy_initiative_validator_group`` (which implies the
        ``User`` and ``Viewer`` groups) and of
        ``strategy_initiative_all_group`` through
        ``security/res_groups/strategy_initiative.xml``, so it can run
        every tour below and can see every fixture. Each initiative still
        gets an explicit ``user_id`` so that the record rule
        ``strategy_initiative_internal_user_rule`` cannot hide it from
        the tour session. Every initiative gets a department of its own:
        the department name is the only stable key to find its row in the
        list, because the document number is only assigned on start.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")

        # Pre-Condition 10-cancel.md and 11-terminate.md: the wizards list
        # the reasons of ``ir.model``, so the fixtures must be global to
        # show up regardless of demo data.
        cls.cancel_reason = (
            cls.env["base.cancel_reason"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Initiative Cancel Reason",
                    "code": "TOURINITCR",
                    "global_use": True,
                }
            )
        )
        cls.terminate_reason = (
            cls.env["base.terminate_reason"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Initiative Terminate Reason",
                    "code": "TOURINITTR",
                    "global_use": True,
                }
            )
        )

        # Pre-Conditions of every IK: a plan that is On Progress. The plan
        # carries a literal name so the tour can pick it in the dropdown.
        plan_type = (
            cls.env["strategy_plan_type"]
            .with_user(cls.admin)
            .create({"name": "Tour Initiative Plan Type", "code": "TOURINITPT"})
        )
        cls.plan = (
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
        cls._run_transition(cls.plan, "action_open")
        cls.plan.sudo().write({"name": "Tour Initiative Plan"})

        # Pre-Condition 04-confirm.md: Draft.
        cls.initiative_confirm = cls._create_initiative("Confirm")

        # Pre-Condition 05-approve.md: Waiting for Approval, with
        # ``admin`` among the record's active approvers -- the standard
        # approval.template routes approval to
        # ``strategy_initiative_validator_group``.
        cls.initiative_approve = cls._create_initiative("Approve")
        cls._run_transition(cls.initiative_approve, "action_confirm")

        # Pre-Condition 07-start.md: Waiting for Approval and fully
        # approved.
        cls.initiative_start = cls._create_initiative("Start")
        cls._run_transition(cls.initiative_start, "action_confirm")
        cls._run_transition(cls.initiative_start, "action_approve_approval")

        # Pre-Condition 09-finish.md: On Progress.
        cls.initiative_finish = cls._create_initiative("Finish")
        cls._run_transition(cls.initiative_finish, "action_confirm")
        cls._run_transition(cls.initiative_finish, "action_approve_approval")
        cls._run_transition(cls.initiative_finish, "action_open")

        # Pre-Condition 10-cancel.md: Draft, one of the states the
        # cancel policy allows.
        cls.initiative_cancel = cls._create_initiative("Cancel")

        # Pre-Condition 11-terminate.md: On Progress.
        cls.initiative_terminate = cls._create_initiative("Terminate")
        cls._run_transition(cls.initiative_terminate, "action_confirm")
        cls._run_transition(cls.initiative_terminate, "action_approve_approval")
        cls._run_transition(cls.initiative_terminate, "action_open")

        # Pre-Condition 12-restart.md: Cancelled.
        cls.initiative_restart = cls._create_initiative("Reopen")
        cls._run_transition(cls.initiative_restart, "action_cancel")

        # Pre-Condition 14-restart-approval.md: Waiting for Approval with
        # no approval.template assigned. The standard template is cleared
        # on the fixture the way an initiative stuck without approvers
        # looks.
        cls.initiative_restart_approval = cls._create_initiative("Restart Approval")
        cls._run_transition(cls.initiative_restart_approval, "action_confirm")
        cls.initiative_restart_approval.invalidate_cache()
        cls.initiative_restart_approval.sudo().write({"approval_template_id": False})

    @classmethod
    def _create_initiative(cls, label):
        """Create one Draft initiative dedicated to a single tour.

        The progress method is Manual so that starting the fixture does
        not need milestones.

        :param label: short scenario name, e.g. ``"Confirm"``
        :return: the new ``strategy_initiative`` record, in Draft, whose
            department name is the key the tour uses to find its row
        """
        department = (
            cls.env["hr.department"]
            .with_user(cls.admin)
            .create({"name": "Tour Init Dept %s" % label})
        )
        return (
            cls.env["strategy_initiative"]
            .with_user(cls.admin)
            .create(
                {
                    "plan_id": cls.plan.id,
                    "department_id": department.id,
                    "progress_method": "manual",
                    "date_start": "2026-01-01",
                    "date_end": "2026-12-31",
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

        :param record: the fixture record to advance
        :param method: name of the workflow method, e.g.
            ``"action_confirm"``
        """
        record.invalidate_cache()
        getattr(
            record.with_user(cls.admin).with_context(bypass_policy_check=True),
            method,
        )()

    def test_create(self):
        """Run the create tour for ``strategy_initiative``.

        IK: docs/strategy_initiative/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_strategic_management_strategy_initiative_create",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``strategy_initiative``.

        IK: docs/strategy_initiative/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_strategic_management_strategy_initiative_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for ``strategy_initiative``.

        IK: docs/strategy_initiative/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_strategic_management_strategy_initiative_approve",
            login="admin",
        )

    def test_start(self):
        """Run the start tour for ``strategy_initiative``.

        IK: docs/strategy_initiative/07-start.md
        """
        self.start_tour(
            "/web",
            "ssi_strategic_management_strategy_initiative_start",
            login="admin",
        )

    def test_finish(self):
        """Run the finish tour for ``strategy_initiative``.

        IK: docs/strategy_initiative/09-finish.md
        """
        self.start_tour(
            "/web",
            "ssi_strategic_management_strategy_initiative_finish",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``strategy_initiative``.

        IK: docs/strategy_initiative/10-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_strategic_management_strategy_initiative_cancel",
            login="admin",
        )

    def test_terminate(self):
        """Run the terminate tour for ``strategy_initiative``.

        IK: docs/strategy_initiative/11-terminate.md
        """
        self.start_tour(
            "/web",
            "ssi_strategic_management_strategy_initiative_terminate",
            login="admin",
        )

    def test_restart(self):
        """Run the restart tour for ``strategy_initiative``.

        IK: docs/strategy_initiative/12-restart.md
        """
        self.start_tour(
            "/web",
            "ssi_strategic_management_strategy_initiative_restart",
            login="admin",
        )

    def test_restart_approval(self):
        """Run the restart approval tour for ``strategy_initiative``.

        IK: docs/strategy_initiative/14-restart-approval.md
        """
        self.start_tour(
            "/web",
            "ssi_strategic_management_strategy_initiative_restart_approval",
            login="admin",
        )
