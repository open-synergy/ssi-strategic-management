# Create Score Category

> **Module:** `ssi_strategic_management`\
> **Model:** `strategy_score_category`\
> **Menu:** Strategic Management > Configuration > Score Categories\
> **Actor:** user in group `Strategy Score Category`\
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Config:** An active `sequence.template` exists for `strategy_score_category` (only
  needed for **Generate Code**).
- **Access:** User is in group `Strategy Score Category`.

## Flow

1. Open the **Strategic Management > Configuration > Score Categories** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter the name of the score category (e.g. "Achievement
     Level").
   - **Code** _(required)_: Enter a unique code identifying this record, or enter **/**
     to assign it later using **Generate Code**.
   - The range lines on the **Ranges** tab are optional and can be completed later;
     ranges of one category must not overlap.
4. Click **Generate Code** in the header to automatically assign a code from the
   `sequence.template` configured for `strategy_score_category`. This requires an active
   `sequence.template` for this model — without one, the action fails with an error. You
   may also leave the Code field as **/** or type a code manually instead.
5. Click **Save**.

## Post-Condition

- A new Score Category record is created and active.
- The new Score Category becomes selectable on a Plan Type.
