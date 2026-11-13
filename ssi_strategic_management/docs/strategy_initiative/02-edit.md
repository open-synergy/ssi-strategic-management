# Edit Strategy Initiative

> **Module:** `ssi_strategic_management`\
> **Model:** `strategy_initiative`\
> **Menu:** Strategic Management > Strategy > Initiatives\
> **Actor:** user in group `User` (`strategy_initiative_user_group`)\
> **Requires:** `01-create`\
> **Inline Actions:** `action_compute_progress` (Compute Progress)

## Pre-Condition

- **Record:** The initiative exists. Its main fields (Plan, Owner, Department, Dates,
  Progress Method, Scope) can be changed only while the status is **Draft**; the
  **Progress** tab stays editable while the status is **On Progress**, so that progress
  can be reported during the initiative.
- **Data:** For the Compute Progress step, the **Progress Method** is **Python Code**
  and the progress code is filled in.
- **Access:** User is in group `User` (`strategy_initiative_user_group`) or `Validator`.

## Flow

1. Open the **Strategic Management > Strategy > Initiatives** menu.
2. Open the initiative to edit.
3. Click the **Edit** button.
4. Open the **Progress** tab and report the progress:
   - **Milestones**: tick **Done** on the milestones that are completed (the **Date
     Done** is filled in automatically and can be adjusted), and add **Evidence**.
   - **Manual**: type the new **Manual Progress (%)**.
   - **Python Code**: click **Compute Progress** to run the progress code and store the
     figure as the progress. It is the only way to refresh the figure — the code does
     not run by itself.
5. Click **Save**.

## Post-Condition

- The **Progress (%)** shown in the header reflects the weight of the completed
  milestones, the manual figure or the computed figure.
- While the initiative is **On Progress**, the **Health** is recalculated at once and
  again every day.
