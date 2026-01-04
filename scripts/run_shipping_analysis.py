#!/usr/bin/env python3
"""Run shipping KPI analysis and save charts + concise summary.

Outputs:
- visuals/shipping_delay_hist.png
- visuals/shipping_delay_boxplot.png
- visuals/sales_vs_delay.png
- visuals/summary.txt
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dateutil import parser
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'raw' / 'superstore.csv'
OUT = ROOT / 'visuals'
OUT.mkdir(parents=True, exist_ok=True)


def safe_parse_dates(series: pd.Series) -> pd.Series:
    s = pd.to_datetime(series, errors='coerce', infer_datetime_format=True)
    mask = s.isna()
    if mask.any():
        def _try_parse(x):
            try:
                return parser.parse(str(x))
            except Exception:
                return pd.NaT
        s.loc[mask] = series[mask].apply(_try_parse)
    return pd.to_datetime(s, errors='coerce')


def main():
    sns.set(style='whitegrid')
    df = pd.read_csv(DATA)

    # robust parsing
    df['Order Date Parsed'] = safe_parse_dates(df['Order Date'])
    df['Ship Date Parsed'] = safe_parse_dates(df['Ship Date'])
    df['Order Date Invalid'] = df['Order Date Parsed'].isna()
    df['Ship Date Invalid'] = df['Ship Date Parsed'].isna()
    df['Shipping Delay (Days)'] = (df['Ship Date Parsed'] - df['Order Date Parsed']).dt.days

    # overall stats
    delay = df['Shipping Delay (Days)']
    desc = delay.describe(percentiles=[0.25, 0.5, 0.75])
    iqr = desc['75%'] - desc['25%'] if '75%' in desc else None

    overall_stats = dict(
        count=int(desc['count']) if not pd.isna(desc['count']) else 0,
        mean=float(desc['mean']) if not pd.isna(desc['mean']) else None,
        median=float(desc['50%']) if not pd.isna(desc['50%']) else None,
        std=float(desc['std']) if not pd.isna(desc['std']) else None,
        min=float(desc['min']) if not pd.isna(desc['min']) else None,
        max=float(desc['max']) if not pd.isna(desc['max']) else None,
        iqr_days=float(iqr) if iqr is not None else None,
    )

    # ship mode stats
    valid = df[~df['Shipping Delay (Days)'].isna()]
    group = valid.groupby('Ship Mode')['Shipping Delay (Days)']
    ship_stats = group.agg(['count', 'median', 'mean', 'std', 'min', 'max'])
    q1 = group.quantile(0.25)
    q3 = group.quantile(0.75)
    ship_stats['IQR'] = (q3 - q1)
    ship_stats['neg_rate'] = df.groupby('Ship Mode').apply(lambda g: (g['Shipping Delay (Days)'] < 0).sum() / max(g.shape[0], 1))
    ship_stats['long_rate_gt7d'] = df.groupby('Ship Mode').apply(lambda g: (g['Shipping Delay (Days)'] > 7).sum() / max(g.shape[0], 1))

    # suspicious records
    med = df['Shipping Delay (Days)'].median()
    stdv = df['Shipping Delay (Days)'].std()
    threshold = med + 3 * stdv if pd.notna(stdv) else (med + 30 if pd.notna(med) else 30)
    suspicious = df[(df['Shipping Delay (Days)'] < 0) | (df['Shipping Delay (Days)'] > threshold)]

    # correlation sales vs delay
    mask = df['Shipping Delay (Days)'].notna() & df['Sales'].notna()
    if mask.sum() > 0:
        corr, pval = spearmanr(df.loc[mask, 'Sales'], df.loc[mask, 'Shipping Delay (Days)'])
    else:
        corr, pval = None, None

    # charts
    plt.figure(figsize=(8, 4))
    sns.histplot(df['Shipping Delay (Days)'].dropna().clip(lower=-5, upper=30), bins=35, kde=False)
    plt.title('Histogram: Shipping Delay (Days) (clipped -5 to 30)')
    plt.xlabel('Shipping Delay (Days)')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig(OUT / 'shipping_delay_hist.png')
    plt.close()

    plt.figure(figsize=(8, 5))
    order = df.groupby('Ship Mode')['Shipping Delay (Days)'].median().sort_values().index
    sns.boxplot(x='Ship Mode', y='Shipping Delay (Days)', data=df, order=order)
    plt.title('Shipping Delay by Ship Mode')
    plt.ylabel('Delay (Days)')
    plt.tight_layout()
    plt.savefig(OUT / 'shipping_delay_boxplot.png')
    plt.close()

    plt.figure(figsize=(7, 5))
    m = mask
    sns.scatterplot(x=df.loc[m, 'Shipping Delay (Days)'], y=df.loc[m, 'Sales'])
    plt.yscale('log')
    plt.xlabel('Shipping Delay (Days)')
    plt.ylabel('Sales (log scale)')
    plt.title('Sales vs Shipping Delay')
    plt.tight_layout()
    plt.savefig(OUT / 'sales_vs_delay.png')
    plt.close()

    # concise summary
    lines = []
    lines.append('Concise Shipping Analysis Summary')
    lines.append('--------------------------------')
    lines.append(f"Total records: {len(df)}")
    lines.append(f"Order date invalid: {int(df['Order Date Invalid'].sum())}")
    lines.append(f"Ship date invalid: {int(df['Ship Date Invalid'].sum())}")
    lines.append('')
    lines.append('Overall shipping delay (days):')
    for k, v in overall_stats.items():
        lines.append(f"- {k}: {v}")
    lines.append('')
    lines.append('Ship Mode summary (median, IQR, neg_rate, long_rate_gt7d):')
    for idx, row in ship_stats.sort_values('median').iterrows():
        lines.append(f"- {idx}: median={row['median']:.1f}, IQR={row.get('IQR', float('nan')):.1f}, neg_rate={row.get('neg_rate',0):.3f}, long_rate_gt7d={row.get('long_rate_gt7d',0):.3f}")
    lines.append('')
    lines.append(f"Suspicious records flagged: {len(suspicious)} (threshold > {threshold:.1f} days)")
    lines.append('')
    lines.append('Spearman correlation (Sales vs Delay):')
    lines.append(f"- correlation: {corr}, p-value: {pval}")
    lines.append('')
    lines.append('Recommended next steps:')
    lines.append('- Investigate negative-delay records and fix date-entry or ETL issues')
    lines.append('- Review high-variability ship modes and long-tail delays (>7 days)')
    lines.append('- Consider prioritizing high-sales orders for faster fulfillment if correlation shows longer delays for larger orders')

    (OUT / 'summary.txt').write_text('\n'.join(lines))


if __name__ == '__main__':
    main()
