import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from folium.features import GeoJsonTooltip
from streamlit_folium import st_folium
import duckdb

# -------------------------
# Load your data
# -------------------------
# Equivalent of: source("data/shapefiles.R")
# You should replace this with your actual loading logic
@st.cache_data
def load_data():
    con = duckdb.connect()

    con.execute("""
        INSTALL httpfs;
        LOAD httpfs;

        SET s3_endpoint='minio:9000';
        SET s3_access_key_id='minioadmin';
        SET s3_secret_access_key='minioadmin';
        SET s3_url_style='path';
        SET s3_use_ssl=false;
    """)

    metrics = con.execute("""
        SELECT *
        FROM read_parquet(
            's3://real-estate-by-census/analytics/realtor_county_metrics.parquet'
        )
    """).df()

    counties = gpd.read_parquet("/app/data/reference/counties.parquet")

    main_df = counties.merge(metrics, on="county_fips", how="inner")

    return gpd.GeoDataFrame(main_df, geometry="geometry", crs="EPSG:4326")

main_df = load_data()

# Ensure it's GeoDataFrame
if not isinstance(main_df, gpd.GeoDataFrame):
    main_df = gpd.GeoDataFrame(main_df, geometry="geometry")

# -------------------------
# App Title
# -------------------------
st.title("Realtor Data at the County Level")

# -------------------------
# Sidebar (filters)
# -------------------------
st.sidebar.header("Filters")

# State picker
states = sorted(main_df["state"].dropna().unique())
selected_states = st.sidebar.multiselect("State", options=states, default=states)

# Median listing price slider
price_min, price_max = 10000, 1_000_000
selected_price = st.sidebar.slider(
    "Median Listing Price",
    min_value=price_min,
    max_value=price_max,
    value=(price_min, price_max),
    step=50000,
)

# Median square feet slider
sqft_min = int(main_df["median_square_feet"].min())
sqft_max = 3000
selected_sqft = st.sidebar.slider(
    "Median Square Feet",
    min_value=sqft_min,
    max_value=sqft_max,
    value=(0, int(main_df["median_square_feet"].max())),
)

# Active listings slider
selected_listings = st.sidebar.slider(
    "Number of Active Listings", min_value=0, max_value=3000, value=(0, 3000)
)

# County population size checkbox
pop_sizes = main_df["county_pop_size"].dropna().unique().tolist()
selected_pop_sizes = st.sidebar.multiselect(
    "County Size by Population", options=pop_sizes, default=pop_sizes
)

# -------------------------
# Filtering (reactive equivalent)
# -------------------------
filtered_df = main_df[
    (main_df["state"].isin(selected_states))
    & (main_df["median_listing_price"].between(*selected_price))
    & (main_df["median_square_feet"].between(*selected_sqft))
    & (main_df["active_listing_count"].between(*selected_listings))
    & (main_df["county_pop_size"].isin(selected_pop_sizes))
]

# -------------------------
# Map (Leaflet equivalent)
# -------------------------
m = folium.Map(location=[37.8, -96], zoom_start=4)

# Color mapping (similar to colorFactor)
import branca.colormap as cm

unique_vals = filtered_df["county_pop_size"].dropna().unique()
colormap = cm.linear.Set1_09.scale(0, len(unique_vals))
val_to_color = {val: colormap(i) for i, val in enumerate(unique_vals)}


def style_function(feature):
    val = feature["properties"]["county_pop_size"]
    return {
        "fillColor": val_to_color.get(val, "#cccccc"),
        "color": "white",
        "weight": 1,
        "fillOpacity": 0.6,
    }


# Tooltip (equivalent to label)
tooltip = GeoJsonTooltip(
    fields=[
        "NAME",
        "state",
        "median_listing_price",
        "median_square_feet",
        "active_listing_count",
        "total_pop",
        "county_pop_size",
        "hispanic_pct",
    ],
    aliases=[
        "County:",
        "State:",
        "Median Listing Price:",
        "Median Sq Ft:",
        "Active Listings:",
        "Population:",
        "County Size:",
        "Hispanic %:",
    ],
    localize=True,
)

# Add polygons
folium.GeoJson(
    filtered_df,
    style_function=style_function,
    tooltip=tooltip,
    highlight_function=lambda x: {"weight": 3, "color": "#666", "fillOpacity": 0.8},
).add_to(m)

# Add legend
colormap.caption = "County Size"
colormap.add_to(m)

# -------------------------
# Render map
# -------------------------
st_data = st_folium(m, width=1000, height=600)
