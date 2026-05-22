# Superstore Sales Analysis

Practical retail sales analysis project focused on business decisions, not just charts.  
I used Python and notebook workflows to identify where revenue is concentrated, where demand changes across the year, and where teams could improve planning and pricing.

## Executive Summary

This project analyzes multi-year Superstore order data to answer common questions a business team would ask:

- What is driving total revenue?
- Which customer groups matter most?
- When does demand typically rise or slow down?
- Where should operations and marketing focus first?

The result is a set of clean, reusable outputs in `data/processed/` plus notebook-based analysis that can be used in Excel or Tableau.

## Business Problem

Retail teams often have data, but not a clear story.  
The goal here was to turn raw order-level records into actionable direction for inventory planning, segment strategy, and performance review.

## Dataset Overview

| Item | Details |
|---|---|
| Dataset | Superstore sales data (portfolio dataset) |
| Scope | Multi-year U.S. retail orders |
| Core fields | Order Date, Ship Date, Category, Sub-Category, Segment, Region, Sales, Profit |
| Main outputs | Aggregated CSVs by category, segment, and month |

## Key Business Questions

- Which categories and customer segments contribute most to sales?
- How does monthly demand shift over time?
- What periods should inventory and campaign planning prioritize?
- Where should deeper profitability analysis happen next?

## Key Metrics Analyzed

Based on processed outputs in `data/processed/`:

- **Total sales analyzed:** **$2.26M**
- **Sales mix by category:**
  - Technology: **$827K** (36.6%)
  - Furniture: **$729K** (32.2%)
  - Office Supplies: **$705K** (31.2%)
- **Sales mix by segment:**
  - Consumer: **$1.15M** (50.8%)
  - Corporate: **$688K** (30.4%)
  - Home Office: **$425K** (18.8%)
- **Monthly seasonality signal:**
  - Highest month in the dataset: **Feb 2017 ($42.97K)**
  - Lowest month in the dataset: **Mar 2015 ($6.72K)**

## Key Findings

1. **Consumer drives most revenue.**  
   Roughly half of all sales come from Consumer customers, which makes this segment the most direct lever for top-line impact.

2. **Revenue is fairly balanced across categories, with Technology leading.**  
   Technology is first, but Furniture and Office Supplies are close enough that planning cannot rely on one category alone.

3. **Sales are seasonal, not flat.**  
   Monthly results show clear swings, so inventory and campaign timing should follow demand cycles instead of fixed monthly assumptions.

4. **The dataset supports operational decision-making, not only reporting.**  
   Aggregated outputs make it easier to connect category and segment trends to practical actions in marketing, pricing, and supply planning.

## Business Impact

This analysis gives a junior-analyst-style decision pack that a manager can use quickly:

- **Planning:** prioritize inventory around historically stronger months instead of spreading stock evenly.
- **Commercial focus:** align promotions to the Consumer segment for broader reach while keeping targeted offers for Corporate accounts.
- **Performance tracking:** monitor category mix month over month to catch early shifts in demand.
- **Operational alignment:** use recurring trends to coordinate marketing, fulfillment, and purchasing decisions from one data view.

## Recommendations

- Build monthly planning targets by category and segment using the processed outputs as a baseline.
- Add profitability by sub-category and region to pair revenue growth with margin protection.
- Add a simple KPI dashboard in Tableau with filters for month, segment, and category.
- Document a recurring review cadence so analysis can support ongoing decisions, not one-time reporting.

## Tools Used

- Python (`pandas`, `matplotlib`, `seaborn`)
- Jupyter Notebooks
- CSV exports for Excel-friendly review
- Tableau-ready aggregated datasets

## Repository Structure

```text
superstore-sales-analysis/
├── analysis.py
├── README.md
├── requirements.txt
├── data/
│   ├── raw/
│   ├── processed/
│   └── superstore_sales.csv
├── notebooks/
│   ├── 01_exploratory_analysis.ipynb
│   ├── 02_aggregate_sales_by_category.ipynb
│   ├── 03_monthly_sales_trends.ipynb
│   ├── shipping_performance_analysis.ipynb
│   └── superstore_analysis.ipynb
├── scripts/
├── docs/
│   └── case_study.md
└── visuals/
```

## Future Improvements

- Expand profitability analysis to sub-category and state level
- Publish a finished Tableau dashboard with core KPI cards
- Add a short business presentation deck for stakeholder walkthroughs

## About Me

I am Phil Greene, an entry-level data analyst transitioning from operations, electrical, and customer-facing roles into analytics.

I am currently pursuing a BS in Data Analytics at SNHU, and I am building projects that show practical business thinking, clear communication, and reliable analysis workflows.

My background in independent e-commerce and operations work helps me frame analysis around real decisions, not just technical output.

## Connect

- LinkedIn: [Phil Greene](https://www.linkedin.com/in/philgreene89)
- X/Twitter: [@vtguy65](https://x.com/vtguy65)
- GitHub: [@WebCraftPhil](https://github.com/WebCraftPhil)

If you are hiring for a junior data analyst role, I would be glad to connect and share more of my work.
