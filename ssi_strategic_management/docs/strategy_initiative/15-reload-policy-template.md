# Reload Template Policy — Strategy Initiative

> **Module:** `ssi_strategic_management`\
> **Model:** `strategy_initiative`\
> **Menu:** Strategic Management > Strategy > Initiatives\
> **Actor:** administrator in group _Settings / Technical Settings_\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** None — usable regardless of status.
- **Config:** At least one active `policy.template` exists for `strategy_initiative`, so
  a matching template can be found.
- **Access:** User is in group _Settings / Technical Settings_ (`base.group_system`).
  The **Policies** tab that contains this button is only visible to this group.

## Flow

1. Open the **Strategic Management > Strategy > Initiatives** menu.
2. Open the initiative whose assigned policy template should be re-evaluated.
3. On the **Policies** tab, click **Reload Template Policy**.

## Post-Condition

- **Policy Template** is recomputed and re-assigned to the highest-sequence
  `policy.template` for this model whose condition currently matches the initiative.
  This may change which action buttons and policy fields (`confirm_ok`,
  `restart_approval_ok`, etc.) are granted, without changing the initiative's status.
