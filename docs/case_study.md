# Case Study: Superstore Sales Analysis

## Executive Summary

Problem: The Superstore dataset contains four years of retail orders. The goal
is to identify revenue drivers, monthly trends, and customer segments that
generate the most sales so business stakeholders can prioritize inventory,
marketing, and pricing decisions.

Approach: I cleaned and aggregated the data, analyzed sales by `Category` and
`Segment`, examined monthly trends (rolling averages and percent changes), and
checked shipping performance by mode. Key charts live in
`notebooks/02_aggregate_sales_by_category.ipynb`,
`notebooks/03_monthly_sales_trends.ipynb`, and
`notebooks/04_shipping_performance_analysis.ipynb`.

## Key Findings

- Total sales: **$2.26M** across 4,922 orders (9,800 order lines, 793 customers, Jan 2015 – Dec 2018).
- Top customer segment by total sales: **Consumer** ($1.15M, 50.8%).
  Corporate ($688K) and Home Office ($425K) follow.
- Category contribution: Technology $827K (36.6%), Furniture $729K (32.2%),
  Office Supplies $705K (31.2%) — balanced enough that no single category
  carries the business.
- **September to December bring in 52% of annual sales**; January and February
  bring in just 7%.
- **Consumer is the slowest-growing segment:** +25% from 2015 to 2018, against
  +85% for Corporate and +77% for Home Office.
- Monthly analysis reveals clear seasonality: the peak month is **Nov 2018
  ($117.9K)** and the lowest is **Feb 2015 ($4.5K)**; yearly totals grow from
  $480K (2015) to $722K (2018). A 3-month rolling average highlights the
  underlying trend beyond month-to-month noise.
- Shipping is clean: delays run 0–7 days (mean 4.0, median 4), with Standard
  Class slowest (median 5 days) and carrying 60% of orders. No link between
  order size and delay.

## Data Quality Note

The source dates are DD/MM/YYYY. An earlier version of this project parsed
them month-first, which silently scrambled monthly trends and produced
impossible shipping delays. The October 2026 cleanup fixed parsing to
`dayfirst=True` in every script and notebook, regenerated all processed files
and charts, and re-executed every notebook — so every number here matches
`data/processed/`.

This export has no `Profit` column, so no profitability claims are made here.
Adding margin analysis is the top follow-up (see below).

## Business Impact

- Focus marketing and inventory investments on high-revenue categories
  during peak months (notably Q4) to maximize ROI.
- Keep `Consumer` messaging for reach, but build a B2B offer for `Corporate`
  and `Home Office`, the two fastest-growing segments.
- Shipping needs no rescue plan — but Standard Class is the mode to watch
  if fulfillment speed becomes a goal.

## Recommended Next Steps

1. Bring in the full Superstore export (with `Profit`) for margin analysis
   by sub-category and region.
2. Extend the live [Tableau dashboard](https://public.tableau.com/app/profile/phil.greene/viz/SuperstoreDataViz_17947709580860/Sheet6)
   with a segment-growth view (build spec in `tableau/BUILD_GUIDE.md`).
3. Drill into `State`/`Region` for targeted regional strategies.

## How to reproduce

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the full analysis and regenerate all outputs:

```bash
python analysis.py
python scripts/run_notebooks.py
python scripts/run_shipping_analysis.py
```

3. Open the notebooks and charts:

- `notebooks/02_aggregate_sales_by_category.ipynb`
- `notebooks/03_monthly_sales_trends.ipynb`
- `notebooks/04_shipping_performance_analysis.ipynb`
- `notebooks/05_full_analysis_walkthrough.ipynb`
- `visuals/` for charts, the slide deck, and the shipping summary

## Files

- `docs/case_study.md` — this file
- `data/raw/superstore.csv` — canonical dataset (9,800 rows)
- `data/processed/` — generated CSVs (monthly and aggregated outputs)
- `tableau/` — Tableau-ready dataset + dashboard build guide

---

_Authored by Phillip Greene — project-ready summary for portfolio presentation._
