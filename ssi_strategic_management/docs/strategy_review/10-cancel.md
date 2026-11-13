# Cancel Strategy Review

> **Module:** `ssi_strategic_management`\
> **Model:** `strategy_review`\
> **Menu:** Strategic Management > Monitoring > Reviews\
> **Actor:** user in group `Validator` (`strategy_review_validator_group`)\
> **State:** `draft` | `confirm` | `done` → `cancel`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**, **Waiting for Approval** or **Done**.
- **Config:** An active `policy.template` for `strategy_review` grants `cancel_ok` for
  that state to the actor's group.
- **Data:** At least one cancellation reason is available to the model.
- **Access:** User is in group `Validator` (`strategy_review_validator_group`).

## Flow

1. Open the **Strategic Management > Monitoring > Reviews** menu.
2. Open the review to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Cancellation Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
- When the review was **Done**, the measurements of its period are unlocked again.
