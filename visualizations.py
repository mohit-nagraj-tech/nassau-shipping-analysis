import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "Nassau Candy Distributor.csv.xls"
OUTPUT_DIR = PROJECT_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA_FILE)

# Convert numeric columns
for col in ["Sales", "Gross Profit", "Units"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Chart 1: Sales by region
region_sales = df.groupby("Region")["Sales"].sum().sort_values()

plt.figure(figsize=(9, 5))
region_sales.plot(kind="barh")
plt.title("Total Sales by Region")
plt.xlabel("Sales")
plt.ylabel("Region")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "sales_by_region.png", dpi=150)
plt.close()

# Chart 2: Shipment records by shipping mode
ship_counts = df["Ship Mode"].value_counts()

plt.figure(figsize=(9, 5))
ship_counts.plot(kind="bar")
plt.title("Shipment Records by Shipping Mode")
plt.xlabel("Shipping Mode")
plt.ylabel("Number of Records")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "shipments_by_mode.png", dpi=150)
plt.close()

# Chart 3: Top 10 products by sales
top_products = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values()
    .tail(10)
)

plt.figure(figsize=(10, 6))
top_products.plot(kind="barh")
plt.title("Top 10 Products by Sales")
plt.xlabel("Sales")
plt.ylabel("Product")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "top_products_by_sales.png", dpi=150)
plt.close()

print("All three charts created successfully!")
print("Check the outputs folder for the PNG files.")