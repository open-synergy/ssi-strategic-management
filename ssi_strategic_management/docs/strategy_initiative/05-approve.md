# Approve Strategy Initiative

> **Module:** `ssi_strategic_management`\
> **Model:** `strategy_initiative`\
> **Menu:** Strategic Management > Strategy > Initiatives\
> **Actor:** active approver on the pending approval level\
> **State:** `confirm` → `confirm` (approved, waiting to be started)\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** An active `policy.template` for `strategy_initiative` grants `approve_ok`
  — the standard template does not restrict this to a fixed group; it is granted per
  record.
- **Access:** User's id is listed in the record's active approvers
  (`active_approver_user_ids`) for the currently pending approval level. When the
  `approval.template` uses sequential approval, only the first unapproved level is
  pending.

## Flow

1. Open the **Strategic Management > Strategy > Initiatives** menu.
2. Open the initiative to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- If there are still pending approval levels, status remains **Waiting for Approval**
  and the next level becomes pending.
- If all approval levels are fulfilled, status still shows **Waiting for Approval**, the
  **Approve** and **Reject** buttons disappear and the **Start** button becomes
  available (see `07-start`). The initiative is not started automatically.
