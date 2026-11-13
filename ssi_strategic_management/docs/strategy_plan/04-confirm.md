# Confirm Strategy Plan

> **Module:** `ssi_strategic_management`\
> **Model:** `strategy_plan`\
> **Menu:** Strategic Management > Strategy > Plans\
> **Actor:** user in group `User` (`strategy_plan_user_group`)\
> **State:** `draft` → `confirm`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Config:** An active `policy.template` for `strategy_plan` grants `confirm_ok` for
  state `draft` to the actor's group.
- **Config:** An active `approval.template` for `strategy_plan` matches this record and
  has at least one approver level (the standard template routes approval to group
  `Validator`).
- **Access:** User is in group `User` (`strategy_plan_user_group`) or `Validator`.

## Flow

1. Open the **Strategic Management > Strategy > Plans** menu.
2. Open the plan to confirm.
3. Click the **Confirm** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**.
- Approval records are created for each approver level defined by the matched
  `approval.template`.
