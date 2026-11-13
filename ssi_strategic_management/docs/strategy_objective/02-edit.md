# Edit Strategy Objective

> **Module:** `ssi_strategic_management`\
> **Model:** `strategy_objective`\
> **Menu:** Strategic Management > Strategy > Objectives\
> **Actor:** user in group `User` (`strategy_objective_user_group`)\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The objective exists. Its main fields (Plan, Department, Perspective and
  so on) can be changed only while the status is **Draft**; the **KPIs** tab stays
  editable in every status, so that realizations can be recorded while the objective is
  **On Progress**.
- **Data:** A **Measure** exists in the measure library (see `strategy_measure`).
- **Data:** The plan of the objective has a start and end date. The period of every
  target must lie within them.
- **Access:** User is in group `User` (`strategy_objective_user_group`) or `Validator`.

## Flow

1. Open the **Strategic Management > Strategy > Objectives** menu.
2. Open the objective to edit.
3. Click the **Edit** button.
4. Open the **KPIs** tab.
5. Click **Add a line** and fill in the KPI:
   - **Measure** _(required)_: Select the measure of the library. The unit, polarity,
     aggregation, score limits and score ranges are copied from it and can be changed.
   - **Name** _(required)_: Type the name of the KPI.
   - **Weight (%)**: Type the share of this KPI in the objective. The weights of all
     KPIs of an objective must add up to 100 before the objective can be started.
   - **Default Target**: Type the target proposed for every new period.
   - **Key Result**: Check it to mark the KPI as a key result of an OKR objective, then
     select the **Key Result Type**.
6. Open the **Targets** tab of the KPI.
7. Click **Add a line** and fill in the target:
   - **Period**: Optionally select a date range to fill the dates.
   - **Date Start** _(required)_: Type the first day of the target period.
   - **Date End** _(required)_: Type the last day of the target period.
   - **Target**: Type the value to reach in the period.
8. In the **Measurements** list of the target, click **Add a line** and fill in the
   measurement:
   - **Date** _(required)_: Type the date of the realization. It must lie within the
     target period.
   - **Value**: Type the realized value.
   - **Note**: Optionally type a remark.
9. Click **Save & Close** on the target dialog, then **Save & Close** on the KPI dialog.
10. Click **Save**.

## Post-Condition

- The KPI is listed on the **KPIs** tab of the objective, and on the **Strategy > KPIs**
  menu.
- The target holds the **Realization** (the measurements rolled up with the aggregation
  of the KPI), its **Score** and its **Final Score** (the score multiplied by the weight
  of the KPI).
- The KPI shows the score of its latest measured target.
- The measurement is listed on the **Monitoring > Measurements** menu.
