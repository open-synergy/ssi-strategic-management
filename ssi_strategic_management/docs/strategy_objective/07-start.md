# Start Strategy Objective

> **Module:** `ssi_strategic_management`\
> **Model:** `strategy_objective`\
> **Menu:** Strategic Management > Strategy > Objectives\
> **Actor:** user in group `User` (`strategy_objective_user_group`)\
> **State:** `draft` → `open`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Record:** The plan of the objective is **On Progress**.
- **Record:** When the objective has child objectives that contribute to it, their
  **Contribution Weight (%)** add up to exactly 100.
- **Config:** An active `policy.template` for `strategy_objective` grants `open_ok` for
  state `draft` to the actor's group.
- **Config:** An active `sequence.template` exists for `strategy_objective` — the
  document number is generated at this transition.
- **Access:** User is in group `User` (`strategy_objective_user_group`) or `Validator`.

## Flow

1. Open the **Strategic Management > Strategy > Objectives** menu.
2. Open the objective to start.
3. Click the **Start** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **On Progress**.
- The document number (**Name**) is assigned from the `sequence.template` configured for
  this model, replacing the placeholder **/**, with the prefix **SO/**.
