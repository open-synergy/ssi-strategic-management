# Cancel Strategy Plan

> **Module:** `ssi_strategic_management`\
> **Model:** `strategy_plan`\
> **Menu:** Strategic Management > Strategy > Plans\
> **Actor:** user in group `Validator` (`strategy_plan_validator_group`)\
> **State:** `draft` | `confirm` | `open` → `cancel`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**, **Waiting for Approval** or **On Progress**.
- **Config:** An active `policy.template` for `strategy_plan` grants `cancel_ok` for
  that state to the actor's group.
- **Data:** At least one cancellation reason is available to the model.
- **Access:** User is in group `Validator` (`strategy_plan_validator_group`).

## Flow

1. Open the **Strategic Management > Strategy > Plans** menu.
2. Open the plan to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Cancellation Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
