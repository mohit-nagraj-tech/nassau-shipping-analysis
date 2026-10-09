import pandas as pd
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "outputs" / "shipping_data_with_factories.csv"
OUTPUT_DIR = PROJECT_DIR / "outputs"

df = pd.read_csv(DATA_FILE)

# Summarize shipments by customer state and region
geographic_summary = (
    df.groupby(["State/Province", "Region"], dropna=False)
    .agg(
        Shipment_Records=("Order ID", "size"),
        Unique_Orders=("Order ID", "nunique"),
        Total_Sales=("Sales", "sum"),
        Average_Reported_Lead_Time=("Shipping Lead Time", "mean"),
    )
    .reset_index()
)

geographic_summary["Total_Sales"] = (
    geographic_summary["Total_Sales"].round(2)
)
geographic_summary["Average_Reported_Lead_Time"] = (
    geographic_summary["Average_Reported_Lead_Time"].round(2)
)

geographic_summary = geographic_summary.sort_values(
    "Shipment_Records", ascending=False
)

geographic_summary.to_csv(
    OUTPUT_DIR / "geographic_bottleneck_analysis.csv",
    index=False
)

print("TOP 10 STATES BY SHIPMENT VOLUME")
print(
    geographic_summary.head(10).to_string(index=False)
)

print("\nSHIPMENT VOLUME BY REGION")
print(
    df.groupby("Region")
    .agg(
        Shipment_Records=("Order ID", "size"),
        Total_Sales=("Sales", "sum")
    )
    .sort_values("Shipment_Records", ascending=False)
    .round(2)
    .to_string()
)

print("\nSaved geographic_bottleneck_analysis.csv")
print(
    "Warning: Reported lead times are suspicious; "
    "do not interpret them as verified delivery performance."
)