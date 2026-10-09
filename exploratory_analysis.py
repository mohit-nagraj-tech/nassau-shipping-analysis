import pandas as pd
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "Nassau Candy Distributor.csv.xls"
OUTPUT_DIR = PROJECT_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

# Load the dataset
df = pd.read_csv(DATA_FILE)

# Convert business metrics to numeric values
for col in ["Sales", "Units", "Gross Profit", "Cost"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

print("========== BUSINESS DATA ANALYSIS ==========")
print("Total records:", len(df))
print("Unique orders:", df["Order ID"].nunique())
print("Unique customers:", df["Customer ID"].nunique())
print("Unique products:", df["Product Name"].nunique())

# 1. Sales and profit summary
print("\n--- SALES AND PROFIT ---")
print("Total sales:", round(df["Sales"].sum(), 2))
print("Total gross profit:", round(df["Gross Profit"].sum(), 2))
print("Total units:", df["Units"].sum())

# 2. Performance by region
region_summary = df.groupby("Region").agg(
    Shipment_Records=("Order ID", "count"),
    Unique_Orders=("Order ID", "nunique"),
    Sales=("Sales", "sum"),
    Gross_Profit=("Gross Profit", "sum")
).sort_values("Sales", ascending=False)

print("\n--- REGION SUMMARY ---")
print(region_summary.round(2).to_string())

# 3. Performance by shipping mode
ship_summary = df.groupby("Ship Mode").agg(
    Shipment_Records=("Order ID", "count"),
    Unique_Orders=("Order ID", "nunique"),
    Sales=("Sales", "sum"),
    Gross_Profit=("Gross Profit", "sum")
).sort_values("Shipment_Records", ascending=False)

print("\n--- SHIPPING MODE SUMMARY ---")
print(ship_summary.round(2).to_string())

# 4. Top 10 products by sales
product_summary = df.groupby("Product Name").agg(
    Units=("Units", "sum"),
    Sales=("Sales", "sum"),
    Gross_Profit=("Gross Profit", "sum")
).sort_values("Sales", ascending=False).head(10)

print("\n--- TOP 10 PRODUCTS BY SALES ---")
print(product_summary.round(2).to_string())

# Save results for later charts and dashboard
region_summary.to_csv(OUTPUT_DIR / "region_summary.csv")
ship_summary.to_csv(OUTPUT_DIR / "shipping_mode_summary.csv")
product_summary.to_csv(OUTPUT_DIR / "top_products.csv")

print("\nAnalysis complete.")
print("Summary files saved in the outputs folder.")