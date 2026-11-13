# Restart Strategy Objective

> **Module:** `ssi_strategic_management`\
> **Model:** `strategy_objective`\
> **Menu:** Strategic Management > Strategy > Objectives\
> **Actor:** user in group `Validator` (`strategy_objective_validator_group`)\
> **State:** `cancel` → `draft`\
> **Requires:** `10-cancel`

## Pre-Condition

- **Record:** Status is **Cancelled**.
- **Config:** An active `policy.template` for `strategy_objective` grants `restart_ok`
  for that state to the actor's group.
- **Access:** User is in group `Validator` (`strategy_objective_validator_group`).

## Flow

1. Open the **Strategic Management > Strategy > Objectives** menu.
2. Open the objective to restart.
3. Click the **Restart** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status returns to **Draft**.
