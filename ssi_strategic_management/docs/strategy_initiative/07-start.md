# Start Strategy Initiative

> **Module:** `ssi_strategic_management`\
> **Model:** `strategy_initiative`\
> **Menu:** Strategic Management > Strategy > Initiatives\
> **Actor:** user in group `User` (`strategy_initiative_user_group`)\
> **State:** `confirm` → `open`\
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **Waiting for Approval** and every approval level is approved.
- **Record:** The **Plan** of the initiative is **On Progress**.
- **Record:** When the **Progress Method** is **Milestones**, the weights of the
  milestones add up to 100.
- **Config:** An active `policy.template` for `strategy_initiative` grants `open_ok` for
  state `confirm` to the actor's group once the initiative is approved.
- **Config:** An active `sequence.template` exists for `strategy_initiative` — the
  document number is generated at this transition.
- **Access:** User is in group `User` (`strategy_initiative_user_group`) or `Validator`.

## Flow

1. Open the **Strategic Management > Strategy > Initiatives** menu.
2. Open the initiative to start.
3. Click the **Start** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **On Progress**.
- The document number (**Name**) is assigned from the `sequence.template` configured for
  this model, replacing the placeholder **/**, with the prefix **SI/**.
- The **Health** is calculated: **On Track**, **At Risk** or **Off Track**, from the gap
  between the share of the period that has elapsed and the progress, compared with the
  thresholds of the plan type.
