# Create Strategy Initiative

> **Module:** `ssi_strategic_management`\
> **Model:** `strategy_initiative`\
> **Menu:** Strategic Management > Strategy > Initiatives\
> **Actor:** user in group `User` (`strategy_initiative_user_group`)\
> **State:** `—` → `draft`\
> **Inline Actions:** `action_compute_progress` (Compute Progress)

## Pre-Condition

- **Data:** A **Plan** exists (see `strategy_plan`). To link objectives and KPIs, they
  exist in that plan.
- **Data:** For the Compute Progress step, the **Progress Method** is **Python Code**
  and the progress code is filled in.
- **Access:** User is in group `User` (`strategy_initiative_user_group`) or the higher
  `Validator` group, which includes it.

## Flow

1. Open the **Strategic Management > Strategy > Initiatives** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Plan** _(required)_: Select the plan that owns the initiative.
   - **Date Start** _(required)_: Enter the first day of the initiative.
   - **Date End** _(required)_: Enter the last day of the initiative.
   - **Responsible**: automatically filled with the current user. Change if needed.
   - **Progress Method** _(required)_: automatically defaulted to **Milestones**. Choose
     **Manual** or **Python Code** instead if progress is not measured by milestones.
4. Optionally fill in the other fields:
   - **Owner** and **Department**: Select the employee and the department that carry out
     the initiative.
   - On the **Scope** tab, select the **Objectives** of the plan and the **KPIs** of
     those objectives that the initiative is meant to move.
5. On the **Progress** tab, prepare how progress is measured:
   - **Milestones**: click **Add a line** for each milestone and fill in **Name**,
     **Weight (%)** and **Deadline**. The weights must add up to 100 before the
     initiative can be started (see `07-start`).
   - **Manual**: type the **Manual Progress (%)**.
   - **Python Code**: type the progress code, which assigns the figure to `result`, then
     click **Compute Progress** to store the figure as the progress. You may also leave
     the code for later — the progress stays 0 until the button is clicked, and every
     change to the code needs another click.
6. Click **Save**.

## Post-Condition

- A new Strategy Initiative record is created in **Draft** status.
- The document number (**Name**) still shows **/** — it is only assigned when the
  initiative is started (see `07-start`).
- The initiative is listed on the **Initiatives** tab of its plan.
- The **Health** stays empty until the initiative is started.
