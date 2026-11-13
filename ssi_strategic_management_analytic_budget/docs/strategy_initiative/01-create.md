# Create Strategy Initiative

> **Module:** `ssi_strategic_management_analytic_budget`
>
> **Extends:** ssi_strategic_management — model `strategy_initiative`, action
> `01-create`

## Additional Fields

When this module is installed, the create form gains one optional field:

- **Analytic Account**: Select the analytic account whose budgets fund the initiative.
  It is on the left side of the form header, below **Department**. It can be changed
  only while the initiative is in **Draft** status. The budgets of the child accounts of
  the selected account are counted as well.

The required **Title** field of the base module must also be filled in before the
initiative can be saved.

## Additional Post-Condition

- Once an analytic account is selected, the **Budget** tab shows the planned cost, the
  cost realization and the budget absorption of the analytic budgets of that account
  that are open or done and whose period overlaps the period of the initiative. The tab
  is visible to users of the analytic budget viewer group, and all its figures are
  read-only.
- While the initiative is in progress, a budget absorption that is ahead of the progress
  lowers the **Health** of the initiative by the same rules as a schedule that is
  behind.
