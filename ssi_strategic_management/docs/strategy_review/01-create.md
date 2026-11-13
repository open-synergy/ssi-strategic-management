# Create Strategy Review

> **Module:** `ssi_strategic_management`\
> **Model:** `strategy_review`\
> **Menu:** Strategic Management > Monitoring > Reviews\
> **Actor:** user in group `User` (`strategy_review_user_group`)\
> **State:** `—` → `draft`\
> **Inline Actions:** `action_take_snapshot` (Take Snapshot)

## Pre-Condition

- **Data:** A **Plan** exists (see `strategy_plan`) with the objectives, the KPI targets
  and the initiatives to review.
- **Data:** For the Take Snapshot step, the plan has at least one objective, KPI target
  or initiative that falls inside the review period (and inside the department, when one
  is chosen).
- **Access:** User is in group `User` (`strategy_review_user_group`) or the higher
  `Validator` group, which includes it.

## Flow

1. Open the **Strategic Management > Monitoring > Reviews** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Title** _(required)_: Enter a short title that identifies the review. It is shown
     next to the document number in the document name.
   - **Plan** _(required)_: Select the plan to review.
   - **Date Start** _(required)_: Enter the first day of the reviewed period.
   - **Date End** _(required)_: Enter the last day of the reviewed period.
   - **Responsible**: automatically filled with the current user. Change if needed.
4. Optionally fill in the other fields:
   - **Department**: Select a department to review only its objectives and initiatives.
     Leave it empty to review the whole plan.
   - On the **Summary** tab, type the conclusion of the review.
5. Click **Save**.
6. On the **Snapshot** tab, click the **Take Snapshot** button. The tab lists one line
   for every objective of the plan, one line for every KPI of those objectives that has
   a target overlapping the review period, and one line for every initiative. Click the
   button again to refresh the snapshot — the existing lines are replaced.
7. Optionally, type a **Comment** and a **Corrective Action** on any line.
8. Click **Save**.

## Post-Condition

- The record is listed under its title, and the title is searchable. Once a number is
  assigned, the name shows **number - title**.
- A new Strategy Review record is created in **Draft** status.
- The document number (**Name**) still shows **/** — it is only assigned when the review
  is finished (see `09-finish`).
- **Plan Score** shows the score of the plan at the time of the snapshot, and the lines
  hold the scores, targets, realizations, progress and health as they were at that time.
  They do not change when the figures of the plan change afterwards.
