# Case Study: Superstore Sales Analysis

## Executive Summary

Problem: The Superstore dataset contains several years of retail orders. The goal is to identify revenue drivers, monthly trends, and customer segments that generate the most sales so business stakeholders can prioritize inventory, marketing, and pricing decisions.

Approach: I cleaned and aggregated the data, analyzed sales by `Category` and `Segment`, and examined monthly trends (rolling averages and percent changes). Key charts live in `notebooks/02_aggregate_sales_by_category.ipynb` and `notebooks/03_monthly_sales_trends.ipynb`.

## Key Findings

- Top customer segment by total sales: **Consumer** (~1.15M).  Corporate and Home Office follow.
- Monthly analysis reveals clear seasonality with recurring peaks in key months; a 3-month rolling average highlights the underlying trend beyond month-to-month noise.
- Category contribution: Technology and Office Supplies are large contributors to revenue (see stacked area chart in `03_monthly_sales_trends.ipynb`).

## Business Impact

- Focus marketing and inventory investments on high-revenue categories during peak months to maximize ROI.
- Investigate promotions or pricing adjustments for underperforming categories to improve margins.
- Use customer-segment-targeted campaigns: prioritize `Consumer` messaging for broad revenue impact, and design B2B offers for `Corporate` accounts.

## Recommended Next Steps

1. Drill into `State`/`Region` for targeted regional strategies.
2. Perform profitability analysis at the product level to balance revenue and margin.
3. Build a small dashboard (Streamlit or Tableau) to present these insights to non-technical stakeholders.

## How to reproduce

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the runner script to export processed CSVs:

```bash
python scripts/run_notebooks.py
```

3. Open the notebooks and charts:

- `notebooks/02_aggregate_sales_by_category.ipynb`
- `notebooks/03_monthly_sales_trends.ipynb`

## Files added

- `docs/case_study.md` — this file (executive summary + reproductions)
- `data/processed/` — generated CSVs (monthly and aggregated outputs)

---

_Authored by Phillip Greene — project-ready summary for portfolio presentation._
