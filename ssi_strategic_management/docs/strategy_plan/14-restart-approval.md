# Restart Approval Process — Strategy Plan

> **Module:** `ssi_strategic_management`\
> **Model:** `strategy_plan`\
> **Menu:** Strategic Management > Strategy > Plans\
> **Actor:** user in group `Validator` (`strategy_plan_validator_group`)\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Record:** No `approval.template` is currently assigned to the plan
  (`approval_template_id` is empty) — for example when the plan got stuck in **Waiting
  for Approval** because no template matched when it was confirmed.
- **Config:** An active `policy.template` for `strategy_plan` grants
  `restart_approval_ok` for state `confirm` to the actor's group, under the condition
  above.
- **Config:** An active `approval.template` for `strategy_plan` exists to be matched.
- **Access:** User is in group `Validator` (`strategy_plan_validator_group`).

## Flow

1. Open the **Strategic Management > Strategy > Plans** menu.
2. Open the plan whose approval process needs to be (re)prepared.
3. Click the **Restart Approval Process** button in the header.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Any existing approval records for this plan are removed.
- A matching `approval.template` is (re-)assigned to `approval_template_id`, and new
  approval records are created for each approver level defined by that template —
  without changing the plan's status.
