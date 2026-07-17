import streamlit as st
import pandas as pd

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Restaurant Channel Profitability Dashboard",
    page_icon="🍽️",
    layout="wide"
)

# -----------------------------
# Load Dataset
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/Restaurant_Channel_Profitability.csv")
    return df

df = load_data()

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("Dashboard Filters")

cuisine = st.sidebar.multiselect(
    "Cuisine",
    sorted(df["CuisineType"].unique()),
    default=sorted(df["CuisineType"].unique())
)

segment = st.sidebar.multiselect(
    "Segment",
    sorted(df["Segment"].unique()),
    default=sorted(df["Segment"].unique())
)

subregion = st.sidebar.multiselect(
    "Subregion",
    sorted(df["Subregion"].unique()),
    default=sorted(df["Subregion"].unique())
)

filtered_df = df[
    (df["CuisineType"].isin(cuisine)) &
    (df["Segment"].isin(segment)) &
    (df["Subregion"].isin(subregion))
]

# -----------------------------
# Title
# -----------------------------
st.title("🍽️ Restaurant Channel Profitability Dashboard")

st.markdown("""
Analyze profitability across

- In-Store
- Uber Eats
- DoorDash
- Self Delivery

Understand which channel generates the highest sustainable profit.
""")

# -----------------------------
# KPIs
# -----------------------------

filtered_df["TotalRevenue"] = (
    filtered_df["InStoreRevenue"] +
    filtered_df["UberEatsRevenue"] +
    filtered_df["DoorDashRevenue"] +
    filtered_df["SelfDeliveryRevenue"]
)

filtered_df["TotalProfit"] = (
    filtered_df["InStoreNetProfit"] +
    filtered_df["UberEatsNetProfit"].fillna(0) +
    filtered_df["DoorDashNetProfit"].fillna(0) +
    filtered_df["SelfDeliveryNetProfit"].fillna(0)
)

revenue = filtered_df["TotalRevenue"].sum()

profit = filtered_df["TotalProfit"].sum()

orders = filtered_df["MonthlyOrders"].sum()

restaurants = filtered_df["RestaurantID"].nunique()

margin = (profit/revenue)*100

avg_aov = filtered_df["AOV"].mean()

col1,col2,col3,col4,col5,col6 = st.columns(6)

col1.metric("Revenue",f"${revenue:,.0f}")
col2.metric("Net Profit",f"${profit:,.0f}")
col3.metric("Margin",f"{margin:.2f}%")
col4.metric("Orders",f"{orders:,}")
col5.metric("Restaurants",restaurants)
col6.metric("Average AOV",f"${avg_aov:.2f}")

st.divider()

st.subheader("Dataset Preview")

st.dataframe(filtered_df.head())

st.info("Use the left sidebar to filter cuisine, segment and region. Detailed analytics are available from the Pages menu.")