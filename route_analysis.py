import pandas as pd
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "outputs" / "cleaned_shipping_data.csv"
OUTPUT_DIR = PROJECT_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

# Product-to-factory mapping from the project instructions
PRODUCT_FACTORY = {
    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious": "Lot's O' Nuts",
    "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",
    "Laffy Taffy": "Sugar Shack",
    "SweeTARTS": "Sugar Shack",
    "Nerds": "Sugar Shack",
    "Fun Dip": "Sugar Shack",
    "Fizzy Lifting Drinks": "Sugar Shack",
    "Everlasting Gobstopper": "Secret Factory",
    "Lickable Wallpaper": "Secret Factory",
    "Wonka Gum": "Secret Factory",
    "Hair Toffee": "The Other Factory",
    "Kazookles": "The Other Factory",
}

def main():
    df = pd.read_csv(DATA_FILE)

    # Assign a factory to each product
    df["Factory"] = df["Product Name"].map(PRODUCT_FACTORY)

    # Check for product names that did not match the mapping
    unmatched = df[df["Factory"].isna()]["Product Name"].drop_duplicates()

    print("Total shipment records:", len(df))
    print("Records without factory mapping:", len(df[df["Factory"].isna()]))

    if not unmatched.empty:
        print("Unmatched product names:")
        print(unmatched.to_string(index=False))

    # Save the shipment data with factory assignments
    df.to_csv(OUTPUT_DIR / "shipping_data_with_factories.csv", index=False)

    # Build route summaries only for records with known factories
    route_df = df.dropna(subset=["Factory"]).copy()

    route_summary = (
        route_df.groupby(
            ["Factory", "State/Province", "Region"],
            dropna=False
        )
        .agg(
            Shipment_Records=("Order ID", "size"),
            Unique_Orders=("Order ID", "nunique"),
            Average_Lead_Time=("Shipping Lead Time", "mean"),
            Lead_Time_Std=("Shipping Lead Time", "std"),
            Total_Sales=("Sales", "sum"),
        )
        .reset_index()
    )

    route_summary["Average_Lead_Time"] = (
        route_summary["Average_Lead_Time"].round(2)
    )
    route_summary["Lead_Time_Std"] = (
        route_summary["Lead_Time_Std"].round(2)
    )
    route_summary["Total_Sales"] = route_summary["Total_Sales"].round(2)

    route_summary.to_csv(
        OUTPUT_DIR / "route_summary.csv",
        index=False
    )

    print("\nRoute summary created.")
    print("Number of factory-to-region/state routes:", len(route_summary))
    print("\nTop routes by shipment volume:")
    print(
        route_summary.sort_values(
            "Shipment_Records", ascending=False
        ).head(10).to_string(index=False)
    )

    print("\nSaved:")
    print(OUTPUT_DIR / "shipping_data_with_factories.csv")
    print(OUTPUT_DIR / "route_summary.csv")

    print(
        "\nDATA QUALITY WARNING: Lead-time values are currently "
        "suspicious and must be verified before ranking routes "
        "by shipping speed or efficiency."
    )

if __name__ == "__main__":
    main()