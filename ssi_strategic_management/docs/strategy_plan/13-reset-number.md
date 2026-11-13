# Reset Document Number — Strategy Plan

> **Module:** `ssi_strategic_management`\
> **Model:** `strategy_plan`\
> **Menu:** Strategic Management > Strategy > Plans\
> **Actor:** user in group `Validator` (`strategy_plan_validator_group`)\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Config:** An active `policy.template` for `strategy_plan` grants `manual_number_ok`
  for state `draft` to the actor's group.
- **Access:** User is in group `Validator` (`strategy_plan_validator_group`).

## Flow

1. Open the **Strategic Management > Strategy > Plans** menu.
2. Open the Draft plan whose document number will be reset.
3. Click the **Reset Document Number** button (or edit the **Name** field and change it
   to **/**).
4. Click **OK** on the confirmation dialog (only when the button was used).

## Post-Condition

- Document number returns to **/**.
- The plan receives an automatic number from the `sequence.template` when it is started
  (see `07-start`).
