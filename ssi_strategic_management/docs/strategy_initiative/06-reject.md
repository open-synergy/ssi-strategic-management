# Reject Strategy Initiative

> **Module:** `ssi_strategic_management`\
> **Model:** `strategy_initiative`\
> **Menu:** Strategic Management > Strategy > Initiatives\
> **Actor:** active approver on the pending approval level\
> **State:** `confirm` → `reject`\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** An active `policy.template` for `strategy_initiative` grants `reject_ok` —
  the standard template does not restrict this to a fixed group; it is granted per
  record.
- **Access:** User's id is listed in the record's active approvers
  (`active_approver_user_ids`) for the currently pending approval level.

## Flow

1. Open the **Strategic Management > Strategy > Initiatives** menu.
2. Open the initiative to reject.
3. Click the **Reject** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Rejected**.
