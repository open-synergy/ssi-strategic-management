# Create Strategy Plan

> **Module:** `ssi_strategic_management`\
> **Model:** `strategy_plan`\
> **Menu:** Strategic Management > Strategy > Plans\
> **Actor:** user in group `User` (`strategy_plan_user_group`)\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** At least one **Plan Type** exists (see `strategy_plan_type`).
- **Data:** When the plan is a sub-plan, its parent plan already exists and its period
  covers the sub-plan period.
- **Access:** User is in group `User` (`strategy_plan_user_group`) or the higher
  `Validator` group, which includes it.

## Flow

1. Open the **Strategic Management > Strategy > Plans** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Title** _(required)_: Enter a short title that identifies the plan. It is shown
     next to the document number in the document name.
   - **Plan Type** _(required)_: Select the plan type that fixes the methodology of the
     plan.
   - **Date Start** _(required)_: Enter the first day covered by the plan.
   - **Date End** _(required)_: Enter the last day covered by the plan.
   - **Responsible**: automatically filled with the current user. Change if needed.
4. Optionally fill in the other fields:
   - **Parent Plan**: Select the plan that contains this plan (for example the yearly
     plan of a quarterly plan). The period of this plan must stay within the period of
     the parent plan.
   - On the **Direction** tab, enter the **Vision** and the **Mission** of the plan.
5. Click **Save**.

## Post-Condition

- The record is listed under its title, and the title is searchable. Once a number is
  assigned, the name shows **number - title**.
- A new Strategy Plan record is created in **Draft** status.
- The document number (**Name**) still shows **/** — it is only assigned when the plan
  is started (see `07-start`).
- When a **Parent Plan** is selected, the plan is listed on the **Sub-Plans** tab of the
  parent plan.
