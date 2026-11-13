# Finish Strategy Review

> **Module:** `ssi_strategic_management`\
> **Model:** `strategy_review`\
> **Menu:** Strategic Management > Monitoring > Reviews\
> **Actor:** user in group `User` (`strategy_review_user_group`)\
> **State:** `confirm` → `done`\
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **Waiting for Approval** and every approval level is approved.
- **Config:** An active `policy.template` for `strategy_review` grants `done_ok` for
  state `confirm` to the actor's group, under the condition that the review is fully
  approved.
- **Access:** User is in group `User` (`strategy_review_user_group`) or `Validator`.

## Flow

1. Open the **Strategic Management > Monitoring > Reviews** menu.
2. Open the review to finish.
3. Click the **Done** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Done**.
- The document number (**Name**) is assigned (prefix `SR/`).
- The measurements of the plan that are dated inside the review period are locked: they
  cannot be created, changed or deleted, for every objective of the plan, or only for
  the objectives of the **Department** when the review has one. Measurements dated
  outside the period are not affected.
