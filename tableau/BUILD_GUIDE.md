# Tableau Dashboard — Build Guide

The workbook is built in **Tableau Public, entirely in the browser — no install
needed** — from one tidy file: **`superstore_tableau.csv`** — 9,800 order lines,
Jan 2015–Dec 2018, with ISO dates, `Year`, `Month`, `shipping_delay_days`
already computed. No joins or reshaping needed.

## Connect (Tableau Public web authoring)

1. Create a free account at public.tableau.com and sign in.
2. Click **Create a Viz** — this opens web authoring in your browser.
3. In the Connect to Data pane, go to the **Files** tab and upload
   `tableau/superstore_tableau.csv` (drag-and-drop works; CSV uploads up to 1 GB).
4. Confirm `Order Date` and `Month` read as dates, `Sales` as a number.
5. No extracts or calculations are required to start; the two calculated fields
   below are optional polish.

Note: Tableau Public publishes to your public profile by design — fine here,
since the Superstore data is a public sample dataset, not private company data.

## Sheets to build (about 20 minutes)

| Sheet | Type | Rows / Columns | Notes |
|---|---|---|---|
| KPI cards | Text | `SUM(Sales)`, `COUNTD(Order ID)`, `AVG` order value | Headline values: **$2.26M** total sales, **4,922** orders, **$459** avg order value |
| Sales by Category | Bar | Category → `SUM(Sales)` | Technology $827K, Furniture $729K, Office Supplies $705K |
| Monthly Sales Trend | Line | `Month` (continuous) → `SUM(Sales)` | Add a 3-month moving average; peak is Nov 2018 ($117.9K) |
| Sales by Segment | Bar or donut | Segment → `SUM(Sales)` | Consumer 50.8%, Corporate 30.4%, Home Office 18.8% |
| Sales by Region / State | Map or bar | State → `SUM(Sales)` | Filterable by Region |
| Shipping Delay by Mode | Box plot or bar | Ship Mode → `AVG(shipping_delay_days)` | Same Day 0, First Class 2, Second Class 3, Standard Class 5 days (median) |

## Dashboard

- Put the KPI cards across the top, the monthly trend full-width below them,
  category + segment side by side, shipping at the bottom.
- Add filters: `Year`, `Category`, `Segment`. Apply to all sheets.
- Title: "Superstore Sales, 2015–2018 — what drives revenue, and when it peaks."

## Optional calculated fields

- `Sales Share` = `SUM([Sales]) / TOTAL(SUM([Sales]))` (for category/segment labels)
- `YoY Growth` = `(SUM([Sales]) - LOOKUP(SUM([Sales]), -12)) / ABS(LOOKUP(SUM([Sales]), -12))`
  on the monthly trend (table calculation, 12 months back).

## Publishing (Tableau Public)

File → Save to Tableau Public. The CSV travels with the workbook, so the
published dashboard stays live without a separate data source.
