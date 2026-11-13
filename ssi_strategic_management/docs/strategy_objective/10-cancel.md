# Cancel Strategy Objective

> **Module:** `ssi_strategic_management`\
> **Model:** `strategy_objective`\
> **Menu:** Strategic Management > Strategy > Objectives\
> **Actor:** user in group `Validator` (`strategy_objective_validator_group`)\
> **State:** `draft` | `open` → `cancel`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft** or **On Progress**.
- **Config:** An active `policy.template` for `strategy_objective` grants `cancel_ok`
  for that state to the actor's group.
- **Data:** At least one cancellation reason is available to the model.
- **Access:** User is in group `Validator` (`strategy_objective_validator_group`).

## Flow

1. Open the **Strategic Management > Strategy > Objectives** menu.
2. Open the objective to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Cancellation Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
