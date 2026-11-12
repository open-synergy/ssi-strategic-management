# Create Perspective

> **Module:** `ssi_strategic_management`\
> **Model:** `strategy_perspective`\
> **Menu:** Strategic Management > Configuration > Perspectives\
> **Actor:** user in group `Strategy Perspective`\
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Config:** An active `sequence.template` exists for `strategy_perspective` (only
  needed for **Generate Code**).
- **Access:** User is in group `Strategy Perspective`.

## Flow

1. Open the **Strategic Management > Configuration > Perspectives** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter the name of the Balanced Scorecard perspective (e.g.
     "Financial", "Customer").
   - **Code** _(required)_: Enter a unique code identifying this record, or enter **/**
     to assign it later using **Generate Code**.
   - **Sequence**: Automatically defaulted to **10**. Change it to control the display
     order among perspectives — lower values appear first.
   - **Color Index**: Optional color index used to tint the perspective on dashboards.
4. Click **Generate Code** in the header to automatically assign a code from the
   `sequence.template` configured for `strategy_perspective`. This requires an active
   `sequence.template` for this model — without one, the action fails with an error. You
   may also leave the Code field as **/** or type a code manually instead.
5. Click **Save**.

## Post-Condition

- A new Perspective record is created and active.
- The new Perspective becomes selectable on strategic objectives.
