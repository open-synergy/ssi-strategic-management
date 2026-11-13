# Restart Strategy Review

> **Module:** `ssi_strategic_management`\
> **Model:** `strategy_review`\
> **Menu:** Strategic Management > Monitoring > Reviews\
> **Actor:** user in group `Validator` (`strategy_review_validator_group`)\
> **State:** `cancel` | `reject` → `draft`\
> **Requires:** `10-cancel`

## Pre-Condition

- **Record:** Status is **Cancelled** or **Rejected**.
- **Config:** An active `policy.template` for `strategy_review` grants `restart_ok` for
  that state to the actor's group.
- **Access:** User is in group `Validator` (`strategy_review_validator_group`).

## Flow

1. Open the **Strategic Management > Monitoring > Reviews** menu.
2. Open the review to restart.
3. Click the **Restart** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status returns to **Draft**.
- All approval records are removed and `approval_template_id` is cleared. A later
  Confirm starts the approval process from the beginning.
