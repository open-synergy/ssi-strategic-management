# Create Strategy Objective

> **Module:** `ssi_strategic_management`\
> **Model:** `strategy_objective`\
> **Menu:** Strategic Management > Strategy > Objectives\
> **Actor:** user in group `User` (`strategy_objective_user_group`)\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** A **Plan** exists (see `strategy_plan`).
- **Data:** At least one **Department** exists. When the objective is cascaded to an
  employee, that employee works in the selected department.
- **Data:** When the plan follows the Balanced Scorecard methodology, at least one
  **Perspective** exists.
- **Data:** When the objective is a child objective, its parent objective already exists
  in the same plan or in an ancestor plan.
- **Access:** User is in group `User` (`strategy_objective_user_group`) or the higher
  `Validator` group, which includes it.

## Flow

1. Open the **Strategic Management > Strategy > Objectives** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Plan** _(required)_: Select the plan that owns the objective.
   - **Department** _(required)_: Select the department that the objective is cascaded
     to.
   - **Cascade Method** _(required)_: Keep **Contributive** or select **Direct**.
   - **Perspective** _(required for Balanced Scorecard plans)_: Select the perspective
     of the objective.
   - **Responsible**: automatically filled with the current user. Change if needed.
4. Optionally fill in the other fields:
   - **Employee**: Select the employee that the objective is cascaded to. Only plans
     whose plan type cascades down to employees accept it, and the employee must belong
     to the selected department.
   - **Owner**: Select the employee who is accountable for the objective.
   - **Parent Objective**: Select the objective that this objective is cascaded from.
   - **Contribute to Parent** and **Contribution Weight (%)**: Adjust how this objective
     contributes to its parent.
   - On the **Influences** tab, add the objectives that this objective influences.
5. Click **Save**.

## Post-Condition

- A new Strategy Objective record is created in **Draft** status.
- The document number (**Name**) still shows **/** — it is only assigned when the
  objective is started (see `07-start`).
- The objective is listed on the **Objectives** tab of its plan.
- When a **Parent Objective** is selected, the objective is listed on the **Child
  Objectives** tab of the parent objective.
