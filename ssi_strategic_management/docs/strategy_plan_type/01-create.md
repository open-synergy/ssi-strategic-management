# Create Plan Type

> **Module:** `ssi_strategic_management`\
> **Model:** `strategy_plan_type`\
> **Menu:** Strategic Management > Configuration > Plan Types\
> **Actor:** user in group `Strategy Plan Type`\
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Config:** An active `sequence.template` exists for `strategy_plan_type` (only needed
  for **Generate Code**).
- **Access:** User is in group `Strategy Plan Type`.

## Flow

1. Open the **Strategic Management > Configuration > Plan Types** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter the name of the plan type (e.g. "Corporate Balanced
     Scorecard").
   - **Code** _(required)_: Enter a unique code identifying this record, or enter **/**
     to assign it later using **Generate Code**.
   - On the **Configuration** tab, **Methodology**, **Cascade Level** and **Score
     Scale** are automatically defaulted to **Balanced Scorecard**, **Department** and
     **Percentage (0-100+)**. An OKR plan type must use the **OKR (0.0-1.0)** score
     scale.
4. Click **Generate Code** in the header to automatically assign a code from the
   `sequence.template` configured for `strategy_plan_type`. This requires an active
   `sequence.template` for this model — without one, the action fails with an error. You
   may also leave the Code field as **/** or type a code manually instead.
5. Click **Save**.

## Post-Condition

- A new Plan Type record is created and active.
- The new Plan Type becomes selectable on strategic plans.
