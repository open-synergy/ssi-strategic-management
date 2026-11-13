# Reload Template Policy — Strategy Review

> **Module:** `ssi_strategic_management`\
> **Model:** `strategy_review`\
> **Menu:** Strategic Management > Monitoring > Reviews\
> **Actor:** administrator in group _Settings / Technical Settings_\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** None — usable regardless of status.
- **Config:** At least one active `policy.template` exists for `strategy_review`, so a
  matching template can be found.
- **Access:** User is in group _Settings / Technical Settings_ (`base.group_system`).
  The **Policies** tab that contains this button is only visible to this group.

## Flow

1. Open the **Strategic Management > Monitoring > Reviews** menu.
2. Open the review whose assigned policy template should be re-evaluated.
3. On the **Policies** tab, click **Reload Template Policy**.

## Post-Condition

- **Policy Template** is recomputed and re-assigned to the highest-sequence
  `policy.template` for this model whose condition currently matches the review. This
  may change which action buttons and policy fields (`confirm_ok`,
  `restart_approval_ok`, etc.) are granted, without changing the review's status.
