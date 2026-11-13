# Restart Strategy Initiative

> **Module:** `ssi_strategic_management`\
> **Model:** `strategy_initiative`\
> **Menu:** Strategic Management > Strategy > Initiatives\
> **Actor:** user in group `Validator` (`strategy_initiative_validator_group`)\
> **State:** `cancel` | `reject` | `terminate` → `draft`\
> **Requires:** `10-cancel`

## Pre-Condition

- **Record:** Status is **Cancelled**, **Rejected** or **Terminated**.
- **Config:** An active `policy.template` for `strategy_initiative` grants `restart_ok`
  for that state to the actor's group.
- **Access:** User is in group `Validator` (`strategy_initiative_validator_group`).

## Flow

1. Open the **Strategic Management > Strategy > Initiatives** menu.
2. Open the initiative to restart.
3. Click the **Restart** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status returns to **Draft**.
- All approval records are removed and `approval_template_id` is cleared. A later
  Confirm starts the approval process from the beginning.
