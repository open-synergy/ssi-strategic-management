# Create Measure

> **Module:** `ssi_strategic_management`\
> **Model:** `strategy_measure`\
> **Menu:** Strategic Management > Configuration > Measure Library\
> **Actor:** user in group `Strategy Measure`\
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Config:** An active `sequence.template` exists for `strategy_measure` (only needed
  for **Generate Code**).
- **Access:** User is in group `Strategy Measure`.

## Flow

1. Open the **Strategic Management > Configuration > Measure Library** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter the name of the measure (e.g. "Net Profit Margin").
   - **Code** _(required)_: Enter a unique code identifying this record, or enter **/**
     to assign it later using **Generate Code**.
   - On the **Indicator** tab, **Polarity**, **Frequency**, **Indicator Type** and
     **Aggregation** are automatically defaulted. Change them if the measure needs a
     different behaviour.
   - On the **Scoring** tab, **Minimum Score** and **Maximum Score** are automatically
     defaulted to **0** and **120**. The score range lines of the measure are optional
     and can be completed later.
4. Click **Generate Code** in the header to automatically assign a code from the
   `sequence.template` configured for `strategy_measure`. This requires an active
   `sequence.template` for this model — without one, the action fails with an error. You
   may also leave the Code field as **/** or type a code manually instead.
5. Click **Save**.

## Post-Condition

- A new Measure record is created and active.
- The new Measure is available in the measure library for key results and KPIs.
