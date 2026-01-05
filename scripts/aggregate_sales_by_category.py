#!/usr/bin/env python3
"""Aggregate sales by Category from data/raw/superstore.csv
Writes CSV to visuals/sales_by_category.csv and a short summary to visuals/summary.txt
"""
from pathlib import Path
import sys
import csv

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "raw" / "superstore.csv"
OUT_CSV = ROOT / "visuals" / "sales_by_category.csv"
OUT_SUM = ROOT / "visuals" / "summary.txt"

def run_pandas():
    import pandas as pd
    df = pd.read_csv(INPUT)
    if 'Category' not in df.columns or 'Sales' not in df.columns:
        raise SystemExit("Input CSV missing required 'Category' or 'Sales' columns")
    # ensure Sales numeric
    df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce').fillna(0.0)
    agg = df.groupby('Category', dropna=False)['Sales'].sum().reset_index()
    agg = agg.sort_values('Sales', ascending=False)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    agg.to_csv(OUT_CSV, index=False)
    lines = [f"{row['Category']}: {row['Sales']:.2f}" for _, row in agg.iterrows()]
    return '\n'.join(lines)

def run_csv():
    totals = {}
    with open(INPUT, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            cat = (r.get('Category') or '').strip()
            sales_raw = (r.get('Sales') or '0').replace('$','').replace(',','')
            try:
                s = float(sales_raw)
            except Exception:
                s = 0.0
            totals[cat] = totals.get(cat, 0.0) + s
    rows = sorted(totals.items(), key=lambda x: -x[1])
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, 'w', newline='', encoding='utf-8') as out:
        w = csv.writer(out)
        w.writerow(['Category', 'Sales'])
        for cat, s in rows:
            w.writerow([cat, f"{s:.2f}"])
    return '\n'.join(f"{cat}: {s:.2f}" for cat, s in rows)

def main():
    if not INPUT.exists():
        print(f"Input file not found: {INPUT}", file=sys.stderr)
        raise SystemExit(1)
    try:
        out = run_pandas()
    except Exception:
        out = run_csv()
    with open(OUT_SUM, 'w', encoding='utf-8') as f:
        f.write('Sales by Category (aggregated)\n')
        f.write(out)
        f.write('\n')
    print(out)

if __name__ == '__main__':
    main()
