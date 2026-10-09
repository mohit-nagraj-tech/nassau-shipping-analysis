import pandas as pd
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "outputs" / "route_summary.csv"
OUTPUT_DIR = PROJECT_DIR / "outputs"

df = pd.read_csv(DATA_FILE)

# Rank routes by shipment volume
df = df.sort_values(
    "Shipment_Records",
    ascending=False
).reset_index(drop=True)

df["Volume_Rank"] = df["Shipment_Records"].rank(
    method="dense",
    ascending=False
).astype(int)

# Highest-volume routes
top_10 = df.head(10).copy()

# Lowest-volume routes
bottom_10 = df.sort_values(
    ["Shipment_Records", "Factory", "State/Province"]
).head(10).copy()

# Save the results
top_10.to_csv(
    OUTPUT_DIR / "top_10_routes_by_volume.csv",
    index=False
)

bottom_10.to_csv(
    OUTPUT_DIR / "bottom_10_routes_by_volume.csv",
    index=False
)

print("TOP 10 ROUTES BY SHIPMENT VOLUME")
print(top_10[
    ["Factory", "State/Province", "Region",
     "Shipment_Records", "Unique_Orders", "Total_Sales"]
].to_string(index=False))

print("\nBOTTOM 10 ROUTES BY SHIPMENT VOLUME")
print(bottom_10[
    ["Factory", "State/Province", "Region",
     "Shipment_Records", "Unique_Orders", "Total_Sales"]
].to_string(index=False))

print("\nFiles saved in outputs folder.")
print("Note: These are volume rankings, not shipping-speed rankings.")