# Confirm Strategy Review

> **Module:** `ssi_strategic_management`\
> **Model:** `strategy_review`\
> **Menu:** Strategic Management > Monitoring > Reviews\
> **Actor:** user in group `User` (`strategy_review_user_group`)\
> **State:** `draft` → `confirm`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Record:** The snapshot is taken: the **Snapshot** tab has at least one line.
- **Config:** An active `policy.template` for `strategy_review` grants `confirm_ok` for
  state `draft` to the actor's group.
- **Config:** An active `approval.template` for `strategy_review` matches this record
  and has at least one approver level (the standard template routes approval to group
  `Validator`).
- **Access:** User is in group `User` (`strategy_review_user_group`) or `Validator`.

## Flow

1. Open the **Strategic Management > Monitoring > Reviews** menu.
2. Open the review to confirm.
3. Click the **Confirm** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**.
- Approval records are created for each approver level defined by the matched
  `approval.template`.
- A review without a snapshot line is not confirmed: the error _"Take a snapshot before
  confirming the review."_ is shown instead.
