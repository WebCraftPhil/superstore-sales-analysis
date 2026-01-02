"""
Superstore Sales Analysis Script
A portfolio-style data analysis script for retail sales data.

This script performs comprehensive analysis of superstore sales data,
answering key business questions about sales trends, product performance,
regional analysis, customer segments, and profitability.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# Configuration
warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette('husl')

# Constants
DATA_PATH = 'data/superstore_sales.csv'


def load_and_prepare_data(filepath):
    """Load and prepare the sales data."""
    print("Loading data...")
    df = pd.read_csv(filepath)
    
    # Convert dates
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    
    # Extract date components
    df['Year'] = df['Order Date'].dt.year
    df['Month'] = df['Order Date'].dt.month
    df['Quarter'] = df['Order Date'].dt.quarter
    
    # Calculate shipping time
    df['Shipping Days'] = (df['Ship Date'] - df['Order Date']).dt.days
    
    print(f"✓ Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"✓ Date range: {df['Order Date'].min()} to {df['Order Date'].max()}")
    
    return df


def analyze_sales_trends(df):
    """Analyze sales trends over time."""
    print("\n" + "="*50)
    print("SALES TRENDS ANALYSIS")
    print("="*50)
    
    # Yearly sales
    yearly_sales = df.groupby('Year')['Sales'].sum().round(2)
    print("\nTotal Sales by Year:")
    for year, sales in yearly_sales.items():
        print(f"  {year}: ${sales:,.2f}")
    
    # Calculate growth
    growth = yearly_sales.pct_change() * 100
    print("\nYear-over-Year Growth:")
    for year, pct in growth.dropna().items():
        print(f"  {year}: {pct:+.1f}%")
    
    return yearly_sales


def analyze_product_performance(df):
    """Analyze product category performance."""
    print("\n" + "="*50)
    print("PRODUCT PERFORMANCE ANALYSIS")
    print("="*50)
    
    # Category sales
    category_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=False).round(2)
    total_sales = category_sales.sum()
    
    print("\nSales by Category:")
    for category, sales in category_sales.items():
        pct = (sales / total_sales) * 100
        print(f"  {category}: ${sales:,.2f} ({pct:.1f}%)")
    
    # Top sub-categories
    subcategory_sales = df.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False).head(5).round(2)
    print("\nTop 5 Sub-Categories:")
    for i, (subcat, sales) in enumerate(subcategory_sales.items(), 1):
        print(f"  {i}. {subcat}: ${sales:,.2f}")
    
    return category_sales


def analyze_regional_performance(df):
    """Analyze sales by region."""
    print("\n" + "="*50)
    print("REGIONAL PERFORMANCE ANALYSIS")
    print("="*50)
    
    # Regional sales
    regional_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False).round(2)
    total_sales = regional_sales.sum()
    
    print("\nSales by Region:")
    for region, sales in regional_sales.items():
        pct = (sales / total_sales) * 100
        print(f"  {region}: ${sales:,.2f} ({pct:.1f}%)")
    
    # Top states
    state_sales = df.groupby('State')['Sales'].sum().sort_values(ascending=False).head(5).round(2)
    print("\nTop 5 States:")
    for i, (state, sales) in enumerate(state_sales.items(), 1):
        print(f"  {i}. {state}: ${sales:,.2f}")
    
    return regional_sales


def analyze_customer_segments(df):
    """Analyze customer segment performance."""
    print("\n" + "="*50)
    print("CUSTOMER SEGMENT ANALYSIS")
    print("="*50)
    
    # Segment sales
    segment_sales = df.groupby('Segment')['Sales'].sum().sort_values(ascending=False).round(2)
    total_sales = segment_sales.sum()
    
    print("\nSales by Customer Segment:")
    for segment, sales in segment_sales.items():
        pct = (sales / total_sales) * 100
        print(f"  {segment}: ${sales:,.2f} ({pct:.1f}%)")
    
    # Average order value
    segment_avg = df.groupby('Segment')['Sales'].mean().sort_values(ascending=False).round(2)
    print("\nAverage Order Value by Segment:")
    for segment, avg in segment_avg.items():
        print(f"  {segment}: ${avg:,.2f}")
    
    return segment_sales


def analyze_profitability(df):
    """Analyze profitability across categories."""
    print("\n" + "="*50)
    print("PROFITABILITY ANALYSIS")
    print("="*50)
    
    # Category profit and margin
    category_metrics = df.groupby('Category').agg({
        'Sales': 'sum',
        'Profit': 'sum'
    })
    category_metrics['Profit Margin %'] = (
        category_metrics['Profit'] / category_metrics['Sales'] * 100
    ).round(2)
    category_metrics = category_metrics.sort_values('Profit', ascending=False)
    
    print("\nProfitability by Category:")
    for category in category_metrics.index:
        profit = category_metrics.loc[category, 'Profit']
        margin = category_metrics.loc[category, 'Profit Margin %']
        print(f"  {category}: ${profit:,.2f} (margin: {margin:.1f}%)")
    
    # Top profitable sub-categories
    subcat_profit = df.groupby('Sub-Category').agg({
        'Sales': 'sum',
        'Profit': 'sum'
    })
    subcat_profit['Profit Margin %'] = (
        subcat_profit['Profit'] / subcat_profit['Sales'] * 100
    ).round(2)
    top_profitable = subcat_profit.sort_values('Profit', ascending=False).head(5)
    
    print("\nTop 5 Most Profitable Sub-Categories:")
    for i, subcat in enumerate(top_profitable.index, 1):
        profit = top_profitable.loc[subcat, 'Profit']
        margin = top_profitable.loc[subcat, 'Profit Margin %']
        print(f"  {i}. {subcat}: ${profit:,.2f} (margin: {margin:.1f}%)")
    
    return category_metrics


def generate_summary_report(df):
    """Generate overall summary report."""
    print("\n" + "="*50)
    print("EXECUTIVE SUMMARY")
    print("="*50)
    
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    overall_margin = (total_profit / total_sales * 100)
    num_orders = df['Order ID'].nunique()
    num_customers = df['Customer ID'].nunique()
    avg_order_value = df.groupby('Order ID')['Sales'].sum().mean()
    
    print(f"\nKey Metrics:")
    print(f"  Total Sales: ${total_sales:,.2f}")
    print(f"  Total Profit: ${total_profit:,.2f}")
    print(f"  Overall Profit Margin: {overall_margin:.2f}%")
    print(f"  Number of Orders: {num_orders:,}")
    print(f"  Number of Customers: {num_customers:,}")
    print(f"  Average Order Value: ${avg_order_value:,.2f}")
    
    print("\nKey Insights:")
    print("  ✓ Analysis covers retail sales data across multiple years")
    print("  ✓ Multiple product categories with varying profitability")
    print("  ✓ Geographic distribution across different regions")
    print("  ✓ Three customer segments with distinct purchasing patterns")
    
    print("\nRecommendations:")
    print("  1. Focus on high-margin products for better profitability")
    print("  2. Optimize inventory based on seasonal trends")
    print("  3. Develop region-specific marketing strategies")
    print("  4. Review pricing for low or negative profit items")
    print("  5. Enhance customer segment-specific offerings")


def main():
    """Main execution function."""
    print("="*50)
    print("SUPERSTORE SALES ANALYSIS")
    print("Portfolio Project - Data Analysis")
    print("="*50)
    
    # Load data
    df = load_and_prepare_data(DATA_PATH)
    
    # Perform analyses
    analyze_sales_trends(df)
    analyze_product_performance(df)
    analyze_regional_performance(df)
    analyze_customer_segments(df)
    analyze_profitability(df)
    generate_summary_report(df)
    
    print("\n" + "="*50)
    print("Analysis Complete!")
    print("="*50)
    print("\nFor detailed visualizations, please run the Jupyter notebook:")
    print("  jupyter notebook notebooks/superstore_analysis.ipynb")


if __name__ == "__main__":
    main()
