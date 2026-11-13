# Start Strategy Plan

> **Module:** `ssi_strategic_management`\
> **Model:** `strategy_plan`\
> **Menu:** Strategic Management > Strategy > Plans\
> **Actor:** user in group `User` (`strategy_plan_user_group`)\
> **State:** `confirm` → `open`\
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **Waiting for Approval** and every approval level is approved.
- **Record:** When the plan has a **Parent Plan**, the parent plan is **On Progress**.
- **Config:** An active `policy.template` for `strategy_plan` grants `open_ok` for state
  `confirm` to the actor's group once the plan is approved.
- **Config:** An active `sequence.template` exists for `strategy_plan` — the document
  number is generated at this transition.
- **Access:** User is in group `User` (`strategy_plan_user_group`) or `Validator`.

## Flow

1. Open the **Strategic Management > Strategy > Plans** menu.
2. Open the plan to start.
3. Click the **Start** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **On Progress**.
- The document number (**Name**) is assigned from the `sequence.template` configured for
  this model, replacing the placeholder **/**, with the prefix **SP/**.
- Sub-plans of this plan can now be started.
