# Finish Strategy Initiative

> **Module:** `ssi_strategic_management`\
> **Model:** `strategy_initiative`\
> **Menu:** Strategic Management > Strategy > Initiatives\
> **Actor:** user in group `User` (`strategy_initiative_user_group`)\
> **State:** `open` → `done`\
> **Requires:** `07-start`

## Pre-Condition

- **Record:** Status is **On Progress**.
- **Config:** An active `policy.template` for `strategy_initiative` grants `done_ok` for
  state `open` to the actor's group.
- **Access:** User is in group `User` (`strategy_initiative_user_group`) or `Validator`.

## Flow

1. Open the **Strategic Management > Strategy > Initiatives** menu.
2. Open the initiative to finish.
3. Click the **Done** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Done**.
