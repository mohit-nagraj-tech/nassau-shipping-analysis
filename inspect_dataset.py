import pandas as pd
from pathlib import Path

file_path = Path("data/Nassau Candy Distributor.csv.xls")

if not file_path.exists():
    print("Dataset not found. Check the file name.")
    raise SystemExit

df = pd.read_csv(file_path)
print("\n--- DATE CHECK BY SHIP MODE ---")

df["Order Date"] = pd.to_datetime(
    df["Order Date"], format="%d-%m-%Y", errors="coerce"
)
df["Ship Date"] = pd.to_datetime(
    df["Ship Date"], format="%d-%m-%Y", errors="coerce"
)

df["Lead Time"] = (df["Ship Date"] - df["Order Date"]).dt.days

print(
    df.groupby("Ship Mode")["Lead Time"]
    .agg(["count", "min", "max", "mean"])
    .round(2)
)
print("\n--- DATE RANGE IN ORIGINAL DATA ---")
print("Order Date examples:")
print(df["Order Date"].head(5).tolist())

print("\nShip Date examples:")
print(df["Ship Date"].head(5).tolist())

print("\n--- SHIP MODE COUNTS ---")
print(df["Ship Mode"].value_counts())
print("\n--- ORIGINAL DATE VALUES ---")
print(df[["Order Date", "Ship Date"]].head(15).to_string(index=False))
print("--- DATASET INFO ---")
print("Rows and columns:", df.shape)
print("\n--- MISSING VALUES ---")
print(df.isnull().sum())
print("\n--- DUPLICATE ROWS ---")
print(df.duplicated().sum())

# Convert dates using day-first interpretation
df["Order Date"] = pd.to_datetime(
    df["Order Date"], errors="coerce", dayfirst=True
)

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"], errors="coerce", dayfirst=True
)

print("\n--- DATE VALIDATION ---")
for col in ["Order Date", "Ship Date"]:
    print(f"\n{col}")
    print("Invalid dates:", df[col].isna().sum())
    print("Earliest date:", df[col].min())
    print("Latest date:", df[col].max())

# Calculate shipping lead time
df["Shipping Lead Time"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

print("\n--- LEAD TIME CHECK ---")
print(
    "Negative lead times:",
    (df["Shipping Lead Time"] < 0).sum()
)
print("Minimum lead time:", df["Shipping Lead Time"].min())
print("Maximum lead time:", df["Shipping Lead Time"].max())
print(
    "Average lead time:",
    round(df["Shipping Lead Time"].mean(), 2),
    "days"
)

print("\n--- SAMPLE DATE RECORDS ---")
print(df[["Order Date", "Ship Date", "Shipping Lead Time"]].head(10))

print("\n--- DATE RANGE CHECK ---")
print("Earliest order date:", pd.to_datetime(df["Order Date"], errors="coerce").min())
print("Latest order date:", pd.to_datetime(df["Order Date"], errors="coerce").max())
print("Earliest ship date:", pd.to_datetime(df["Ship Date"], errors="coerce").min())
print("Latest ship date:", pd.to_datetime(df["Ship Date"], errors="coerce").max())

print("\n--- ORDER ID SAMPLE ---")
print(df[["Order ID", "Order Date", "Ship Date"]].tail(10).to_string(index=False))