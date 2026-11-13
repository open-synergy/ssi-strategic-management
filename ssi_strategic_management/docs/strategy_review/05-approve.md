# Approve Strategy Review

> **Module:** `ssi_strategic_management`\
> **Model:** `strategy_review`\
> **Menu:** Strategic Management > Monitoring > Reviews\
> **Actor:** active approver on the pending approval level\
> **State:** `confirm` → `confirm` (approved, waiting to be finished)\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** An active `policy.template` for `strategy_review` grants `approve_ok` —
  the standard template does not restrict this to a fixed group; it is granted per
  record.
- **Access:** User's id is listed in the record's active approvers
  (`active_approver_user_ids`) for the currently pending approval level. When the
  `approval.template` uses sequential approval, only the first unapproved level is
  pending.

## Flow

1. Open the **Strategic Management > Monitoring > Reviews** menu.
2. Open the review to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- If there are still pending approval levels, status remains **Waiting for Approval**
  and the next level becomes pending.
- If all approval levels are fulfilled, status still shows **Waiting for Approval**, the
  **Approve** and **Reject** buttons disappear and the **Done** button becomes available
  (see `09-finish`). The review is not finished automatically.
