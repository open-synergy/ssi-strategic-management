# Reset Document Number — Strategy Review

> **Module:** `ssi_strategic_management`\
> **Model:** `strategy_review`\
> **Menu:** Strategic Management > Monitoring > Reviews\
> **Actor:** user in group `Validator` (`strategy_review_validator_group`)\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Config:** An active `policy.template` for `strategy_review` grants
  `manual_number_ok` for state `draft` to the actor's group.
- **Access:** User is in group `Validator` (`strategy_review_validator_group`).

## Flow

1. Open the **Strategic Management > Monitoring > Reviews** menu.
2. Open the Draft review whose document number will be reset.
3. Click the **Reset Document Number** button (or edit the **Name** field and change it
   to **/**).
4. Click **OK** on the confirmation dialog (only when the button was used).

## Post-Condition

- Document number returns to **/**.
- The review receives an automatic number from the `sequence.template` when it is
  finished (see `09-finish`).
