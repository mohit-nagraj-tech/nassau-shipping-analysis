import pandas as pd
from pathlib import Path

# Locate the project and dataset
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "Nassau Candy Distributor.csv.xls"

def load_and_clean_data():
    df = pd.read_csv(DATA_FILE)

    # Remove exact duplicate rows
    df = df.drop_duplicates().copy()

    # Convert date columns using the dataset's DD-MM-YYYY format
    df["Order Date"] = pd.to_datetime(
        df["Order Date"], format="%d-%m-%Y", errors="coerce"
    )
    df["Ship Date"] = pd.to_datetime(
        df["Ship Date"], format="%d-%m-%Y", errors="coerce"
    )

    # Convert numeric columns safely
    numeric_columns = ["Sales", "Units", "Gross Profit", "Cost"]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Calculate lead time, but flag suspicious dates for review
    df["Shipping Lead Time"] = (
        df["Ship Date"] - df["Order Date"]
    ).dt.days

    df["Date Issue"] = (
        df["Order Date"].isna()
        | df["Ship Date"].isna()
        | (df["Shipping Lead Time"] < 0)
        | (df["Shipping Lead Time"] > 60)
    )

    # Save cleaned data for further analysis
    output_dir = PROJECT_DIR / "outputs"
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "cleaned_shipping_data.csv"
    df.to_csv(output_file, index=False)

    print(f"Cleaned data saved to: {output_file}")

    return df


if __name__ == "__main__":
    cleaned_df = load_and_clean_data()

    print("Rows after cleaning:", len(cleaned_df))
    print("Columns:", len(cleaned_df.columns))
    print("Records flagged for date review:", cleaned_df["Date Issue"].sum())
    print("\nShipping lead time summary:")
    print(cleaned_df["Shipping Lead Time"].describe())
    print("\nSample cleaned records:")
    print(cleaned_df.head())
    print("\n--- ORDER ID AND DATE CHECK ---")
    print(
        cleaned_df[
            ["Order ID", "Order Date", "Ship Date", "Ship Mode"]
        ].head(15).to_string(index=False)
    )

    print("\n--- LEAD TIME BY SHIP MODE ---")
    print(
        cleaned_df.groupby("Ship Mode")["Shipping Lead Time"]
        .agg(["count", "min", "max", "mean"])
        .round(2)
    )
