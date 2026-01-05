#!/usr/bin/env python3
"""
Lightweight runner to export processed CSVs used by notebooks.
Produces:
 - data/processed/monthly_sales.csv
 - data/processed/sales_by_segment.csv
 - data/processed/sales_by_category.csv
 - data/processed/monthly_sales_by_category.csv

Run from repository root:
    python scripts/run_notebooks.py
"""
import os
import pandas as pd

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw_path = os.path.join(repo_root, 'data', 'raw', 'superstore.csv')
out_dir = os.path.join(repo_root, 'data', 'processed')

os.makedirs(out_dir, exist_ok=True)

print('Reading:', raw_path)
if not os.path.exists(raw_path):
    raise FileNotFoundError(f"Raw data not found at {raw_path}")

# Load with parsing if possible
try:
    df = pd.read_csv(raw_path, parse_dates=['Order Date'], low_memory=False)
except Exception:
    df = pd.read_csv(raw_path, low_memory=False)
    df['Order Date'] = pd.to_datetime(df.get('Order Date'), errors='coerce')

# Basic cleaning
df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
df = df.dropna(subset=['Order Date', 'Sales'])

# Monthly aggregation
df['Month'] = df['Order Date'].dt.to_period('M').dt.to_timestamp()
monthly = df.groupby('Month', dropna=False)['Sales'].sum().reset_index()
monthly.to_csv(os.path.join(out_dir, 'monthly_sales.csv'), index=False)
print('Wrote:', os.path.join(out_dir, 'monthly_sales.csv'))

# Sales by segment
if 'Segment' in df.columns:
    seg = df.groupby('Segment')['Sales'].sum().reset_index().sort_values('Sales', ascending=False)
    seg.to_csv(os.path.join(out_dir, 'sales_by_segment.csv'), index=False)
    print('Wrote:', os.path.join(out_dir, 'sales_by_segment.csv'))
else:
    print('Warning: no Segment column found')

# Sales by category
if 'Category' in df.columns:
    cat = df.groupby('Category')['Sales'].sum().reset_index().sort_values('Sales', ascending=False)
    cat.to_csv(os.path.join(out_dir, 'sales_by_category.csv'), index=False)
    print('Wrote:', os.path.join(out_dir, 'sales_by_category.csv'))

    # Monthly x Category pivot
    monthly_cat = (
        df.groupby([df['Order Date'].dt.to_period('M').dt.to_timestamp(), 'Category'])['Sales']
        .sum().reset_index().pivot(index=0, columns=1, values='Sales').fillna(0)
    )
    monthly_cat.index.name = 'Month'
    monthly_cat.to_csv(os.path.join(out_dir, 'monthly_sales_by_category.csv'))
    print('Wrote:', os.path.join(out_dir, 'monthly_sales_by_category.csv'))
else:
    print('Warning: no Category column found')

print('Done.')
