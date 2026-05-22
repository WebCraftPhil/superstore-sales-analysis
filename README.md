# Superstore Sales Analysis

Retail sales analysis project built to answer practical business questions on revenue, profitability, seasonality, and customer segments using Python, Excel-style analysis outputs, and Tableau-ready data.

## Executive Summary

This project analyzes Superstore order data to identify where sales come from, when performance peaks, and which areas need margin improvement. The analysis highlights category and segment performance, recurring monthly patterns, and shipping service behavior to support decisions on pricing, inventory, and operations.

## Business Problem

Retail leaders need a clear view of:
- Which categories and segments drive revenue
- Where profit leakage is happening
- How seasonality affects demand
- How shipping performance may impact customer experience

## Dataset Overview

| Item | Details |
|---|---|
| Dataset | Superstore sales data (portfolio dataset) |
| Scope | Multi-year U.S. retail orders |
| Core fields | Order Date, Ship Date, Category, Sub-Category, Segment, Region, Sales, Profit |
| Outputs | Processed CSV summaries and notebook-based analysis |

## Tools & Technologies

- Python (pandas, matplotlib, seaborn)
- Jupyter Notebooks
- Excel-friendly CSV outputs in `data/processed/`
- Tableau Public (dashboard-ready placeholders included)

## Project Workflow

1. Load and profile raw sales data
2. Clean date and numeric fields
3. Aggregate by category, segment, and month
4. Analyze trends, profitability, and shipping behavior
5. Summarize findings and recommendations for business stakeholders

## Key Business Questions

- Which product categories and sub-categories generate the most revenue?
- What monthly and yearly sales patterns are visible?
- Which customer segments contribute most to total sales?
- Which regions or product areas show lower profitability?
- How do shipping delays vary by shipping mode?

## Key Insights

- Consumer is the top revenue segment, with Corporate and Home Office trailing.
- Sales show recurring seasonal peaks, and rolling monthly trends clarify demand direction.
- Technology and Office Supplies are major contributors to revenue.
- Profitability is uneven across products, suggesting pricing and mix optimization opportunities.
- Shipping delay patterns differ by ship mode, indicating service-level consistency gaps.

## Recommendations

- Prioritize inventory and campaigns for high-performing categories during peak periods.
- Review pricing or discount strategy for low-margin product groups.
- Use segment-specific messaging, with strong focus on Consumer and tailored B2B offers for Corporate.
- Investigate shipping outliers and improve delivery consistency for slower modes.

## Business Impact

This analysis helps stakeholders make faster, evidence-based decisions by connecting sales trends to practical actions. The outputs support better demand planning, stronger margin management, and clearer prioritization of marketing and operations efforts.

## Dashboard Preview

> Add dashboard screenshots in the `visuals/` folder and replace these placeholders.

- `[Placeholder] visuals/dashboard_sales_overview.png`
- `[Placeholder] visuals/dashboard_profitability_overview.png`

## Tableau/Public Dashboard Links

- Tableau Public: [Add link here](https://public.tableau.com/)
- Interactive dashboard notes: [Add link or short summary here](#)

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

## Skills Demonstrated

- Data cleaning and transformation with pandas
- Exploratory and business-focused data analysis
- Trend and category performance analysis
- Profitability and segment-level interpretation
- Clear stakeholder communication through summaries and visuals

## Future Improvements

- Add deeper state and regional profitability drill-downs
- Expand product-level margin analysis
- Publish a complete Tableau dashboard with filters and KPI cards
- Add a short slide-style business presentation for hiring reviews

## About Me

I am an entry-level data analyst focused on turning raw business data into clear insights and practical recommendations.

## Contact

- LinkedIn: [Add LinkedIn URL](https://www.linkedin.com/)
- GitHub: [@WebCraftPhil](https://github.com/WebCraftPhil)
- Portfolio: [Add portfolio URL](https://example.com)
