
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------

st.set_page_config(
    page_title="Online Retail Analytics",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 Online Retail Customer Segmentation")
st.write("Unsupervised Machine Learning Dashboard")

# -------------------------------
# LOAD DATA
# -------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "processed"

@st.cache_data
def load_data():
    segments = pd.read_csv(
        DATA_DIR / "final_customer_segments.csv"
    )

    anomalies = pd.read_csv(
        DATA_DIR / "customer_anomalies.csv"
    )

    return segments, anomalies

try:
    segments, anomalies = load_data()

except FileNotFoundError as e:
    st.error(f"Dataset file not found: {e}")
    st.stop()

# -------------------------------
# SIDEBAR FILTER
# -------------------------------

st.sidebar.header("Dashboard Filters")

available_clusters = sorted(
    segments["Cluster"].dropna().unique()
)

selected_clusters = st.sidebar.multiselect(
    "Select Customer Clusters",
    available_clusters,
    default=available_clusters
)

filtered_data = segments[
    segments["Cluster"].isin(selected_clusters)
]

# -------------------------------
# KEY METRICS
# -------------------------------

st.subheader("Business Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Customers",
    f"{segments['CustomerID'].nunique():,}"
)

col2.metric(
    "Total Clusters",
    segments["Cluster"].nunique()
)

col3.metric(
    "Total Revenue",
    f"£{segments['Monetary'].sum():,.2f}"
)

col4.metric(
    "Average Spending",
    f"£{segments['Monetary'].mean():,.2f}"
)

st.divider()

# -------------------------------
# CUSTOMER DISTRIBUTION
# -------------------------------

st.subheader("Customer Cluster Distribution")

cluster_counts = (
    filtered_data["Cluster"]
    .value_counts()
    .sort_index()
    .reset_index()
)

cluster_counts.columns = ["Cluster", "Customers"]

fig1 = px.bar(
    cluster_counts,
    x="Cluster",
    y="Customers",
    color="Cluster",
    title="Customers in Each Cluster"
)

st.plotly_chart(fig1, use_container_width=True)

# -------------------------------
# CLUSTER SPENDING
# -------------------------------

st.subheader("Customer Spending Analysis")

cluster_spending = (
    filtered_data.groupby("Cluster")
    .agg(
        Average_Spending=("Monetary", "mean"),
        Total_Revenue=("Monetary", "sum")
    )
    .reset_index()
)

fig2 = px.bar(
    cluster_spending,
    x="Cluster",
    y="Average_Spending",
    color="Cluster",
    title="Average Spending by Cluster"
)

st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# RECENCY VS FREQUENCY
# -------------------------------

fig3 = px.scatter(
    filtered_data,
    x="Recency",
    y="Frequency",
    size="Monetary",
    color="Cluster",
    hover_data=["CustomerID"],
    title="Customer Behavior Analysis"
)

st.plotly_chart(fig3, use_container_width=True)

# -------------------------------
# CUSTOMER DATA TABLE
# -------------------------------

st.subheader("Customer Details")

st.dataframe(
    filtered_data[
        [
            "CustomerID",
            "Recency",
            "Frequency",
            "Monetary",
            "Cluster"
        ]
    ],
    use_container_width=True
)

# -------------------------------
# ANOMALY DETECTION
# -------------------------------

st.divider()
st.subheader("Anomaly Detection")

anomaly_count = (
    anomalies["Anomaly"] == -1
).sum()

normal_count = (
    anomalies["Anomaly"] == 1
).sum()

col1, col2 = st.columns(2)

col1.metric("Normal Customers", f"{normal_count:,}")
col2.metric("Anomaly Customers", f"{anomaly_count:,}")

anomaly_customers = anomalies[
    anomalies["Anomaly"] == -1
]

st.write("Unusual Customer Behavior")

st.dataframe(
    anomaly_customers,
    use_container_width=True
)

st.success("Dashboard loaded successfully!")
