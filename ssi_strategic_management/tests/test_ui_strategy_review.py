# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0 only SavepointCase prepares
# ``cls.env`` in ``setUpClass``, which is where every work instruction
# Pre-Condition below is built.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiStrategyReview(HttpSavepointCase):
    """Tour tests for the ``strategy_review`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create one review per tour, in the state its IK requires.

        ``base.user_admin`` is already a member of
        ``strategy_review_validator_group`` (which implies the ``User``
        and ``Viewer`` groups) and of ``strategy_review_all_group``
        through ``security/res_groups/strategy_review.xml``, so it can
        run every tour below and can see every fixture. Each review still
        gets an explicit ``user_id`` so that the record rule
        ``strategy_review_internal_user_rule`` cannot hide it from the
        tour session. Every review gets a summary token of its own: the
        document number is only assigned when the review is finished, so
        the token is the only stable key to find its row in the list.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")

        # Pre-Condition 10-cancel.md: the wizard lists the reasons of
        # ``ir.model``, so the fixture must be global to show up
        # regardless of demo data.
        cls.cancel_reason = (
            cls.env["base.cancel_reason"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Review Cancel Reason",
                    "code": "TOURRVCR",
                    "global_use": True,
                }
            )
        )

        # Pre-Conditions of every IK: a plan with an objective whose KPI
        # has a target inside the reviewed period, so that the snapshot
        # has lines. The plan carries a literal name so the tour can pick
        # it in the dropdown, and the KPI a literal name so the tour can
        # recognise its snapshot line.
        plan_type = (
            cls.env["strategy_plan_type"]
            .with_user(cls.admin)
            .create({"name": "Tour Review Plan Type", "code": "TOURRVPT"})
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
        cls.plan.sudo().write({"name": "Tour Review Plan"})
        objective = (
            cls.env["strategy_objective"]
            .with_user(cls.admin)
            .create(
                {
                    "plan_id": cls.plan.id,
                    "perspective_id": cls.env.ref(
                        "ssi_strategic_management.strategy_perspective_financial"
                    ).id,
                    "user_id": cls.admin.id,
                }
            )
        )
        measure = (
            cls.env["strategy_measure"]
            .sudo()
            .create(
                {
                    "name": "Tour Review Measure",
                    "code": "TOURRVM",
                    "polarity": "higher",
                    "aggregation": "sum",
                }
            )
        )
        kpi = (
            cls.env["strategy_kpi"]
            .sudo()
            .create(
                {
                    "objective_id": objective.id,
                    "measure_id": measure.id,
                    "name": "Tour Review KPI",
                    "weight": 100.0,
                }
            )
        )
        cls.env["strategy_kpi.target"].sudo().create(
            {
                "kpi_id": kpi.id,
                "date_start": "2026-01-01",
                "date_end": "2026-03-31",
                "target": 100.0,
            }
        )

        # Pre-Condition 04-confirm.md: Draft with a snapshot.
        cls.review_confirm = cls._create_review("TRV-CONFIRM")

        # Pre-Condition 05-approve.md: Waiting for Approval, with
        # ``admin`` among the record's active approvers -- the standard
        # approval.template routes approval to
        # ``strategy_review_validator_group``.
        cls.review_approve = cls._create_review("TRV-APPROVE")
        cls._run_transition(cls.review_approve, "action_confirm")

        # Pre-Condition 09-finish.md: Waiting for Approval and fully
        # approved.
        cls.review_finish = cls._create_review("TRV-FINISH")
        cls._run_transition(cls.review_finish, "action_confirm")
        cls._run_transition(cls.review_finish, "action_approve_approval")

        # Pre-Condition 10-cancel.md: Draft, one of the states the cancel
        # policy allows.
        cls.review_cancel = cls._create_review("TRV-CANCEL")

    @classmethod
    def _create_review(cls, token):
        """Create one Draft review with a snapshot, dedicated to one tour.

        :param token: summary of the review, e.g. ``"TRV-CONFIRM"``; it
            is the key the tour uses to find its row in the list
        :return: the new ``strategy_review`` record, in Draft, whose
            snapshot is taken
        """
        review = (
            cls.env["strategy_review"]
            .with_user(cls.admin)
            .create(
                {
                    "plan_id": cls.plan.id,
                    "date_start": "2026-01-01",
                    "date_end": "2026-03-31",
                    "summary": token,
                    "user_id": cls.admin.id,
                }
            )
        )
        cls._run_transition(review, "action_take_snapshot")
        return review

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
        """Run the create tour for ``strategy_review``.

        IK: docs/strategy_review/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_strategic_management_strategy_review_create",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``strategy_review``.

        IK: docs/strategy_review/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_strategic_management_strategy_review_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for ``strategy_review``.

        IK: docs/strategy_review/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_strategic_management_strategy_review_approve",
            login="admin",
        )

    def test_finish(self):
        """Run the finish tour for ``strategy_review``.

        IK: docs/strategy_review/09-finish.md
        """
        self.start_tour(
            "/web",
            "ssi_strategic_management_strategy_review_finish",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``strategy_review``.

        IK: docs/strategy_review/10-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_strategic_management_strategy_review_cancel",
            login="admin",
        )
