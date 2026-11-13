# Restart Approval Process — Strategy Review

> **Module:** `ssi_strategic_management`\
> **Model:** `strategy_review`\
> **Menu:** Strategic Management > Monitoring > Reviews\
> **Actor:** user in group `Validator` (`strategy_review_validator_group`)\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Record:** No `approval.template` is currently assigned to the review
  (`approval_template_id` is empty) — for example when the review got stuck in **Waiting
  for Approval** because no template matched when it was confirmed.
- **Config:** An active `policy.template` for `strategy_review` grants
  `restart_approval_ok` for state `confirm` to the actor's group, under the condition
  above.
- **Config:** An active `approval.template` for `strategy_review` exists to be matched.
- **Access:** User is in group `Validator` (`strategy_review_validator_group`).

## Flow

1. Open the **Strategic Management > Monitoring > Reviews** menu.
2. Open the review whose approval process needs to be (re)prepared.
3. Click the **Restart Approval Process** button in the header.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Any existing approval records for this review are removed.
- A matching `approval.template` is (re-)assigned to `approval_template_id`, and new
  approval records are created for each approver level defined by that template —
  without changing the review's status.
