# Finish Strategy Plan

> **Module:** `ssi_strategic_management`\
> **Model:** `strategy_plan`\
> **Menu:** Strategic Management > Strategy > Plans\
> **Actor:** user in group `User` (`strategy_plan_user_group`)\
> **State:** `open` → `done`\
> **Requires:** `07-start`

## Pre-Condition

- **Record:** Status is **On Progress**.
- **Config:** An active `policy.template` for `strategy_plan` grants `done_ok` for state
  `open` to the actor's group.
- **Access:** User is in group `User` (`strategy_plan_user_group`) or `Validator`.

## Flow

1. Open the **Strategic Management > Strategy > Plans** menu.
2. Open the plan to finish.
3. Click the **Done** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Done**.
