# Terminate Strategy Initiative

> **Module:** `ssi_strategic_management`\
> **Model:** `strategy_initiative`\
> **Menu:** Strategic Management > Strategy > Initiatives\
> **Actor:** user in group `Validator` (`strategy_initiative_validator_group`)\
> **State:** `open` → `terminate`\
> **Requires:** `07-start`

## Pre-Condition

- **Record:** Status is **On Progress**.
- **Config:** An active `policy.template` for `strategy_initiative` grants
  `terminate_ok` for state `open` to the actor's group.
- **Data:** At least one termination reason is available to the model.
- **Access:** User is in group `Validator` (`strategy_initiative_validator_group`).

## Flow

1. Open the **Strategic Management > Strategy > Initiatives** menu.
2. Open the initiative to terminate.
3. Click the **Terminate** button.
4. In the wizard that appears, select the **Termination Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Terminated**.
- The **Health** is cleared.
- The initiative can be restarted to **Draft** (see `12-restart`).
