import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Nassau Shipping Analysis",
    page_icon="📦",
    layout="wide"
)

PROJECT_DIR = Path(__file__).resolve().parent
DATA_FILE = PROJECT_DIR / "data" / "Nassau Candy Distributor.csv.xls"

st.title("📦 Factory-to-Customer Shipping Route Analysis")
st.caption("Nassau Candy Distributor | Data Analytics Project")

st.warning(
    "Data-quality warning: reported shipping lead times range from "
    "904 to 1,642 days. Verify the source dates before interpreting "
    "delivery speed or ranking routes by efficiency."
)


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)

    for col in ["Sales", "Gross Profit", "Units", "Cost"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


df = load_data()

# Product-to-factory mapping from the project brief
factory_products = {
    "Lot's O' Nuts": [
        "Wonka Bar - Nutty Crunch Surprise",
        "Wonka Bar - Fudge Mallows",
        "Wonka Bar -Scrumdiddlyumptious",
    ],
    "Wicked Choccy's": [
        "Wonka Bar - Milk Chocolate",
        "Wonka Bar - Triple Dazzle Caramel",
    ],
    "Sugar Shack": [
        "Laffy Taffy",
        "SweeTARTS",
        "Nerds",
        "Fun Dip",
        "Fizzy Lifting Drinks",
    ],
    "Secret Factory": [
        "Everlasting Gobstopper",
        "Lickable Wallpaper",
        "Wonka Gum",
    ],
    "The Other Factory": [
        "Hair Toffee",
        "Kazookles",
    ],
}

product_to_factory = {
    product: factory
    for factory, products in factory_products.items()
    for product in products
}

df["Factory"] = df["Product Name"].map(product_to_factory)

# Sidebar filters
st.sidebar.header("Dashboard Filters")

regions = sorted(df["Region"].dropna().unique())
selected_regions = st.sidebar.multiselect(
    "Region", regions, default=regions
)

states = sorted(df["State/Province"].dropna().unique())
selected_states = st.sidebar.multiselect(
    "State / Province", states, default=states
)

ship_modes = sorted(df["Ship Mode"].dropna().unique())
selected_modes = st.sidebar.multiselect(
    "Shipping Mode", ship_modes, default=ship_modes
)

factories = sorted(df["Factory"].dropna().unique())
selected_factories = st.sidebar.multiselect(
    "Factory", factories, default=factories
)

filtered = df[
    df["Region"].isin(selected_regions)
    & df["State/Province"].isin(selected_states)
    & df["Ship Mode"].isin(selected_modes)
    & df["Factory"].isin(selected_factories)
].copy()

# KPI cards
st.header("📊 Business Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Shipment Records", f"{len(filtered):,}")
c2.metric("Unique Orders", f"{filtered['Order ID'].nunique():,}")
c3.metric("Total Sales", f"${filtered['Sales'].sum():,.2f}")
c4.metric("Gross Profit", f"${filtered['Gross Profit'].sum():,.2f}")

st.caption(
    f"Factory mapping available for "
    f"{filtered['Factory'].notna().sum():,} of {len(filtered):,} "
    "filtered shipment records."
)

st.divider()

# Sales by region and shipping mode
left, right = st.columns(2)

with left:
    st.subheader("Sales by Region")

    region_sales = (
        filtered.groupby("Region")["Sales"]
        .sum()
        .sort_values(ascending=True)
    )

    fig, ax = plt.subplots(figsize=(7, 4))
    region_sales.plot(kind="barh", ax=ax)
    ax.set_xlabel("Sales ($)")
    ax.set_ylabel("Region")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with right:
    st.subheader("Shipment Records by Shipping Mode")

    mode_counts = filtered["Ship Mode"].value_counts()

    fig, ax = plt.subplots(figsize=(7, 4))
    mode_counts.plot(kind="bar", ax=ax)
    ax.set_ylabel("Shipment Records")
    ax.set_xlabel("Shipping Mode")
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

st.divider()

# Factory analysis
st.header("🏭 Factory Analysis")

factory_summary = (
    filtered.groupby("Factory", dropna=False)
    .agg(
        Shipment_Records=("Order ID", "size"),
        Unique_Orders=("Order ID", "nunique"),
        Total_Sales=("Sales", "sum"),
        Gross_Profit=("Gross Profit", "sum"),
    )
    .reset_index()
    .sort_values("Shipment_Records", ascending=False)
)

st.subheader("Shipment Volume by Factory")
st.dataframe(factory_summary, use_container_width=True)

st.divider()

# Geographic analysis
st.header("🗺️ Geographic Bottleneck Analysis")

state_summary = (
    filtered.groupby(["State/Province", "Region"])
    .agg(
        Shipment_Records=("Order ID", "size"),
        Unique_Orders=("Order ID", "nunique"),
        Total_Sales=("Sales", "sum"),
    )
    .reset_index()
    .sort_values("Shipment_Records", ascending=False)
)

st.subheader("Top 10 States by Shipment Volume")
st.dataframe(state_summary.head(10), use_container_width=True)

st.subheader("Shipment Volume by State")

fig, ax = plt.subplots(figsize=(10, 5))

state_summary.head(10).sort_values(
    "Shipment_Records"
).plot(
    x="State/Province",
    y="Shipment_Records",
    kind="barh",
    legend=False,
    ax=ax,
)

ax.set_xlabel("Shipment Records")
ax.set_ylabel("State / Province")
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.divider()

# Factory-to-destination route analysis
st.header("🚚 Factory-to-Destination Route Analysis")

route_summary = (
    filtered.groupby(
        ["Factory", "State/Province", "Region"],
        dropna=False
    )
    .agg(
        Shipment_Records=("Order ID", "size"),
        Unique_Orders=("Order ID", "nunique"),
        Total_Sales=("Sales", "sum"),
        Gross_Profit=("Gross Profit", "sum"),
    )
    .reset_index()
    .sort_values("Shipment_Records", ascending=False)
)

st.caption(
    "Routes are inferred from the project's product-to-factory mapping "
    "and recorded customer destinations. Shipment volume does not "
    "represent verified road routes or delivery-time efficiency."
)

st.subheader("Top 10 Routes by Shipment Volume")
st.dataframe(route_summary.head(10), use_container_width=True)

st.subheader("Bottom 10 Routes by Shipment Volume")
st.dataframe(
    route_summary.sort_values("Shipment_Records").head(10),
    use_container_width=True,
)

st.download_button(
    "Download Route Summary CSV",
    data=route_summary.to_csv(index=False).encode("utf-8"),
    file_name="route_summary_dashboard.csv",
    mime="text/csv",
)

st.divider()

# Shipment data explorer
st.header("🔎 Shipment Data Explorer")
st.write(f"Showing {len(filtered):,} records based on your filters.")
st.dataframe(filtered, use_container_width=True)

st.download_button(
    "Download Filtered Shipment Data CSV",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="filtered_shipping_data.csv",
    mime="text/csv",
)

st.divider()

# Interactive factory map
st.header("🗺️ Factory and Customer Destination Map")
st.subheader("Factory Locations")

factory_coordinates = {
    "Lot's O' Nuts": (32.881893, -111.768036),
    "Wicked Choccy's": (32.076176, -81.088371),
    "Sugar Shack": (48.119140, -96.181150),
    "Secret Factory": (41.446333, -90.565487),
    "The Other Factory": (35.117500, -89.971107),
}

factory_df = pd.DataFrame([
    {
        "Factory": name,
        "Latitude": coordinates[0],
        "Longitude": coordinates[1],
    }
    for name, coordinates in factory_coordinates.items()
])

factory_fig = px.scatter_geo(
    factory_df,
    lat="Latitude",
    lon="Longitude",
    hover_name="Factory",
    scope="north america",
    title="Locations of the Five Factories",
)

factory_fig.update_traces(
    marker=dict(size=12, color="red")
)

factory_fig.update_geos(
    showcountries=True,
    showland=True,
    landcolor="rgb(235, 235, 235)",
    fitbounds="locations",
)

st.plotly_chart(
    factory_fig,
    use_container_width=True,
    key="factory_locations_map",
)

st.caption(
    "Factory locations are based on the project brief. "
    "The map does not show actual roads or verified shipment paths."
)

# Completion message
st.success(
    "Dashboard loaded. Use the sidebar filters to explore factories, "
    "regions, states, and shipping modes."
)