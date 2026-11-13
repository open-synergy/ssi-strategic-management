# Restart Approval Process — Strategy Initiative

> **Module:** `ssi_strategic_management`\
> **Model:** `strategy_initiative`\
> **Menu:** Strategic Management > Strategy > Initiatives\
> **Actor:** user in group `Validator` (`strategy_initiative_validator_group`)\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Record:** No `approval.template` is currently assigned to the initiative
  (`approval_template_id` is empty) — for example when the initiative got stuck in
  **Waiting for Approval** because no template matched when it was confirmed.
- **Config:** An active `policy.template` for `strategy_initiative` grants
  `restart_approval_ok` for state `confirm` to the actor's group, under the condition
  above.
- **Config:** An active `approval.template` for `strategy_initiative` exists to be
  matched.
- **Access:** User is in group `Validator` (`strategy_initiative_validator_group`).

## Flow

1. Open the **Strategic Management > Strategy > Initiatives** menu.
2. Open the initiative whose approval process needs to be (re)prepared.
3. Click the **Restart Approval Process** button in the header.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Any existing approval records for this initiative are removed.
- A matching `approval.template` is (re-)assigned to `approval_template_id`, and new
  approval records are created for each approver level defined by that template —
  without changing the initiative's status.
