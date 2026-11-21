
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# =====================================================
# 1. PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="RetailIQ | Customer Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "processed"

CUSTOMER_FILE = DATA_DIR / "final_customer_segments.csv"
ANOMALY_FILE = DATA_DIR / "customer_anomalies.csv"

# =====================================================
# 2. DARK THEME CSS
# =====================================================

st.markdown("""
<style>

/* Main application */
.stApp {
    background: #0b1120;
    color: #e2e8f0;
}

[data-testid="stHeader"] {
    background: rgba(11,17,32,0.95);
}

.block-container {
    max-width: 1600px;
    padding: 1.5rem 2.5rem 3rem 2.5rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid #263449;
}

[data-testid="stSidebar"] * {
    color: #e2e8f0;
}

/* Typography */
h1, h2, h3, h4, p, label {
    color: #e2e8f0 !important;
}

h1 {
    font-weight: 750 !important;
}

small {
    color: #94a3b8;
}

/* Header */
.hero {
    background: linear-gradient(120deg, #172554, #1e40af 65%, #2563eb);
    padding: 32px;
    border-radius: 18px;
    margin-bottom: 25px;
    border: 1px solid #334f91;
}

.hero-title {
    font-size: 30px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 8px;
}

.hero-subtitle {
    color: #dbeafe;
    font-size: 14px;
}

/* KPI cards */
.kpi-card {
    background: linear-gradient(145deg, #172033, #111c30);
    border: 1px solid #29364d;
    padding: 22px;
    border-radius: 15px;
    min-height: 125px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.15);
}

.kpi-label {
    color: #94a3b8;
    font-size: 13px;
    font-weight: 600;
}

.kpi-value {
    color: #ffffff;
    font-size: 27px;
    font-weight: 800;
    margin-top: 10px;
}

.kpi-caption {
    color: #60a5fa;
    font-size: 12px;
    margin-top: 5px;
}

/* Dashboard panels */
.panel {
    background: #141f32;
    border: 1px solid #29364d;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 18px;
}

.panel-title {
    color: #f8fafc;
    font-size: 17px;
    font-weight: 700;
    margin-bottom: 5px;
}

.panel-subtitle {
    color: #94a3b8;
    font-size: 12px;
    margin-bottom: 15px;
}

/* Insights */
.insight {
    background: #1b2a41;
    border: 1px solid #30435e;
    border-left: 4px solid #3b82f6;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 12px;
}

.insight-heading {
    color: #93c5fd;
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 5px;
}

.insight-body {
    color: #cbd5e1;
    font-size: 12px;
}

/* Inputs */
[data-baseweb="select"] > div {
    background-color: #172033;
    border-color: #334155;
    color: white;
}

[data-baseweb="input"] input {
    background-color: #172033;
    color: white;
}

.stTextInput input {
    background: #172033;
    color: white;
}

.stButton button, .stDownloadButton button {
    background: #2563eb;
    color: white;
    border: none;
    border-radius: 9px;
    font-weight: 600;
}

.stButton button:hover, .stDownloadButton button:hover {
    background: #1d4ed8;
    color: white;
}

/* Tabs and expanders */
.stTabs [data-baseweb="tab"] {
    color: #cbd5e1;
}

[data-testid="stExpander"] {
    background: #141f32;
    border: 1px solid #334155;
    border-radius: 12px;
}

[data-testid="stDataFrame"] {
    border: 1px solid #334155;
    border-radius: 10px;
}

hr {
    border-color: #29364d;
}

.footer {
    text-align: center;
    color: #64748b;
    font-size: 12px;
    padding: 20px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. HELPER FUNCTIONS
# =====================================================

def money(value):
    return f"£{value:,.0f}"


def chart_layout(fig, height=350):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#141f32",
        plot_bgcolor="#141f32",
        font=dict(
            color="#e2e8f0",
            family="Arial"
        ),
        height=height,
        margin=dict(l=20, r=20, t=55, b=35),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#cbd5e1")
        )
    )
    return fig


def assign_segment(score):
    if score >= 13:
        return "Champions"
    elif score >= 10:
        return "Loyal Buyers"
    elif score >= 8:
        return "Growing Buyers"
    elif score >= 6:
        return "Needs Attention"
    return "Inactive"


# =====================================================
# 4. LOAD DATA
# =====================================================

@st.cache_data
def load_data():

    if not CUSTOMER_FILE.exists():
        raise FileNotFoundError(
            f"Customer file not found: {CUSTOMER_FILE}"
        )

    customers = pd.read_csv(CUSTOMER_FILE)

    anomalies = None

    if ANOMALY_FILE.exists():
        anomalies = pd.read_csv(ANOMALY_FILE)

    return customers, anomalies


try:
    df, anomaly_df = load_data()

except Exception as error:
    st.error(f"Unable to load data: {error}")
    st.stop()


# =====================================================
# 5. DATA VALIDATION
# =====================================================

required_columns = [
    "CustomerID",
    "Recency",
    "Frequency",
    "Monetary"
]

missing = [
    column for column in required_columns
    if column not in df.columns
]

if missing:
    st.error(f"Missing required columns: {missing}")
    st.stop()

for column in ["Recency", "Frequency", "Monetary"]:
    df[column] = pd.to_numeric(
        df[column], errors="coerce"
    )

df = df.dropna(
    subset=required_columns
).copy()

df["CustomerID"] = df["CustomerID"].astype(str)

if df.empty:
    st.error("No valid customer records available.")
    st.stop()

# Use existing Cluster column if available, but keep
# the business RFM segmentation separate.
df["R_Score"] = np.ceil(
    (1 - df["Recency"].rank(pct=True)) * 5
).clip(1, 5).astype(int)

df["F_Score"] = np.ceil(
    df["Frequency"].rank(pct=True) * 5
).clip(1, 5).astype(int)

df["M_Score"] = np.ceil(
    df["Monetary"].rank(pct=True) * 5
).clip(1, 5).astype(int)

df["RFM_Score"] = (
    df["R_Score"] +
    df["F_Score"] +
    df["M_Score"]
)

df["Segment"] = df["RFM_Score"].apply(assign_segment)

segment_order = [
    "Champions",
    "Loyal Buyers",
    "Growing Buyers",
    "Needs Attention",
    "Inactive"
]

segment_colors = {
    "Champions": "#22c55e",
    "Loyal Buyers": "#3b82f6",
    "Growing Buyers": "#a78bfa",
    "Needs Attention": "#f59e0b",
    "Inactive": "#ef4444"
}


# =====================================================
# 6. SIDEBAR
# =====================================================

st.sidebar.markdown("## 📊 RetailIQ")
st.sidebar.caption("Customer Intelligence Platform")

st.sidebar.markdown("---")

st.sidebar.markdown("### 🎯 Dashboard Filters")

selected_segments = st.sidebar.multiselect(
    "Customer Segments",
    segment_order,
    default=segment_order
)

min_recency = int(df["Recency"].min())
max_recency = int(df["Recency"].max())

if min_recency < max_recency:
    recency_range = st.sidebar.slider(
        "Recency Range (Days)",
        min_value=min_recency,
        max_value=max_recency,
        value=(min_recency, max_recency)
    )
else:
    recency_range = (min_recency, max_recency)

search_customer = st.sidebar.text_input(
    "Search Customer ID",
    placeholder="Enter customer ID..."
)

st.sidebar.markdown("---")

st.sidebar.markdown("### 📌 Project Information")
st.sidebar.caption("Project: Online Retail Analytics")
st.sidebar.caption("Method: RFM Customer Segmentation")
st.sidebar.caption("Analysis: Customer Behaviour")


# =====================================================
# 7. APPLY FILTERS
# =====================================================

filtered_data = df[
    df["Segment"].isin(selected_segments)
].copy()

filtered_data = filtered_data[
    filtered_data["Recency"].between(
        recency_range[0],
        recency_range[1]
    )
]

if search_customer.strip():
    filtered_data = filtered_data[
        filtered_data["CustomerID"].str.contains(
            search_customer.strip(),
            case=False,
            na=False
        )
    ]

if filtered_data.empty:
    st.warning("No customers match the selected filters.")
    st.stop()


# =====================================================
# 8. HEADER
# =====================================================

st.markdown("""
<div class="hero">
    <div class="hero-title">
        📊 RetailIQ — Customer Intelligence
    </div>
    <div class="hero-subtitle">
        Transform retail transactions into customer insights,
        understand buying behaviour and discover growth opportunities.
    </div>
</div>
""", unsafe_allow_html=True)

st.caption(
    f"Showing insights for {len(filtered_data):,} customer records"
)


# =====================================================
# 9. KPI METRICS
# =====================================================

total_customers = filtered_data["CustomerID"].nunique()
total_revenue = filtered_data["Monetary"].sum()
avg_recency = filtered_data["Recency"].mean()
avg_frequency = filtered_data["Frequency"].mean()
avg_monetary = filtered_data["Monetary"].mean()

k1, k2, k3, k4 = st.columns(4)

kpis = [
    (
        k1,
        "TOTAL CUSTOMERS",
        f"{total_customers:,}",
        "Unique customers"
    ),
    (
        k2,
        "TOTAL REVENUE",
        money(total_revenue),
        "Total customer spending"
    ),
    (
        k3,
        "AVG. RECENCY",
        f"{avg_recency:.1f} days",
        "Days since last purchase"
    ),
    (
        k4,
        "AVG. FREQUENCY",
        f"{avg_frequency:.1f}",
        "Average unique orders"
    )
]

for col, title, value, caption in kpis:
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{title}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-caption">{caption}</div>
        </div>
        """, unsafe_allow_html=True)


st.markdown("<br>", unsafe_allow_html=True)


# =====================================================
# 10. SEGMENTATION ANALYSIS
# =====================================================

st.markdown("## 📈 Customer Segmentation")
st.caption(
    "Understand how customers are distributed across business segments."
)

left, right = st.columns([1.1, 1])

segment_counts = (
    filtered_data["Segment"]
    .value_counts()
    .reindex(segment_order, fill_value=0)
    .reset_index()
)

segment_counts.columns = ["Segment", "Customers"]

with left:

    st.markdown("""
    <div class="panel">
        <div class="panel-title">Customer Distribution</div>
        <div class="panel-subtitle">
            Number of customers in each segment
        </div>
    </div>
    """, unsafe_allow_html=True)

    fig = px.bar(
        segment_counts,
        x="Segment",
        y="Customers",
        color="Segment",
        color_discrete_map=segment_colors,
        text="Customers"
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False
    )

    fig.update_layout(
        showlegend=False,
        xaxis_title="Customer Segment",
        yaxis_title="Number of Customers"
    )

    st.plotly_chart(
        chart_layout(fig, 370),
        use_container_width=True
    )

with right:

    st.markdown("""
    <div class="panel">
        <div class="panel-title">Segment Composition</div>
        <div class="panel-subtitle">
            Percentage share of each customer segment
        </div>
    </div>
    """, unsafe_allow_html=True)

    fig = px.pie(
        segment_counts,
        names="Segment",
        values="Customers",
        hole=0.62,
        color="Segment",
        color_discrete_map=segment_colors
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    st.plotly_chart(
        chart_layout(fig, 370),
        use_container_width=True
    )


# =====================================================
# 11. REVENUE ANALYSIS
# =====================================================

st.markdown("---")
st.markdown("## 💰 Revenue Intelligence")
st.caption(
    "Identify which customer segments contribute most to revenue."
)

revenue_summary = (
    filtered_data.groupby("Segment")
    .agg(
        Revenue=("Monetary", "sum"),
        Customers=("CustomerID", "nunique"),
        Average_Spending=("Monetary", "mean")
    )
    .reindex(segment_order)
    .dropna(how="all")
    .reset_index()
)

rev1, rev2 = st.columns([1.2, 1])

with rev1:

    fig = px.bar(
        revenue_summary,
        x="Segment",
        y="Revenue",
        color="Segment",
        color_discrete_map=segment_colors,
        text_auto=".2s"
    )

    fig.update_layout(
        showlegend=False,
        xaxis_title="Customer Segment",
        yaxis_title="Revenue (£)"
    )

    st.plotly_chart(
        chart_layout(fig, 360),
        use_container_width=True
    )

with rev2:

    fig = px.bar(
        revenue_summary,
        x="Segment",
        y="Average_Spending",
        color="Segment",
        color_discrete_map=segment_colors,
        text_auto=".2s"
    )

    fig.update_layout(
        showlegend=False,
        xaxis_title="Customer Segment",
        yaxis_title="Average Spending (£)"
    )

    st.plotly_chart(
        chart_layout(fig, 360),
        use_container_width=True
    )


# =====================================================
# 12. RFM HEATMAP
# =====================================================

st.markdown("---")
st.markdown("## 🔥 RFM Behaviour Analysis")

heatmap_data = filtered_data.pivot_table(
    index="R_Score",
    columns="F_Score",
    values="Monetary",
    aggfunc="mean"
).reindex(
    index=[1, 2, 3, 4, 5],
    columns=[1, 2, 3, 4, 5]
)

fig = go.Figure(
    data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale="Blues",
        colorbar=dict(title="Avg Spending"),
        hovertemplate=(
            "Frequency Score: %{x}<br>"
            "Recency Score: %{y}<br>"
            "Average Spending: %{z:.2f}"
            "<extra></extra>"
        )
    )
)

fig.update_layout(
    title="Average Monetary Value by Recency and Frequency",
    xaxis_title="Frequency Score",
    yaxis_title="Recency Score"
)

st.plotly_chart(
    chart_layout(fig, 430),
    use_container_width=True
)


# =====================================================
# 13. CUSTOMER BEHAVIOUR
# =====================================================

st.markdown("---")
st.markdown("## 👥 Customer Behaviour Analysis")

fig = px.scatter(
    filtered_data,
    x="Recency",
    y="Monetary",
    size="Frequency",
    color="Segment",
    color_discrete_map=segment_colors,
    hover_data=[
        "CustomerID",
        "RFM_Score",
        "Frequency"
    ],
    size_max=25,
    title="Recency vs Monetary Value"
)

fig.update_layout(
    xaxis_title="Recency (Days)",
    yaxis_title="Monetary Value (£)"
)

st.plotly_chart(
    chart_layout(fig, 450),
    use_container_width=True
)


# =====================================================
# 14. BUSINESS INSIGHTS
# =====================================================

st.markdown("---")
st.markdown("## 💡 Business Insights & Recommendations")

summary = (
    filtered_data.groupby("Segment")
    .agg(
        Revenue=("Monetary", "sum"),
        Customers=("CustomerID", "nunique")
    )
)

if not summary.empty:

    best_segment = summary["Revenue"].idxmax()
    best_revenue = summary.loc[best_segment, "Revenue"]
    best_customers = summary.loc[best_segment, "Customers"]

    revenue_share = (
        best_revenue / total_revenue * 100
        if total_revenue > 0 else 0
    )

else:
    best_segment = "N/A"
    best_revenue = 0
    best_customers = 0
    revenue_share = 0

needs_attention = filtered_data[
    filtered_data["Segment"] == "Needs Attention"
]["CustomerID"].nunique()

inactive_customers = filtered_data[
    filtered_data["Segment"] == "Inactive"
]["CustomerID"].nunique()

champions = filtered_data[
    filtered_data["Segment"] == "Champions"
]["CustomerID"].nunique()

i1, i2, i3 = st.columns(3)

with i1:
    st.markdown(f"""
    <div class="insight">
        <div class="insight-heading">🏆 Highest Revenue Segment</div>
        <div class="insight-body">
            <h3>{best_segment}</h3>
            Revenue: {money(best_revenue)}<br>
            Customers: {best_customers:,}<br>
            Revenue contribution: {revenue_share:.1f}%
        </div>
    </div>
    """, unsafe_allow_html=True)

with i2:
    st.markdown(f"""
    <div class="insight">
        <div class="insight-heading">⚠️ Retention Opportunity</div>
        <div class="insight-body">
            <h3>{needs_attention:,} customers</h3>
            Customers need attention. Use personalized
            discounts and re-engagement campaigns.
        </div>
    </div>
    """, unsafe_allow_html=True)

with i3:
    st.markdown(f"""
    <div class="insight">
        <div class="insight-heading">🚀 Growth Opportunity</div>
        <div class="insight-body">
            <h3>{champions:,} Champions</h3>
            Reward high-value customers with loyalty
            benefits and exclusive offers.
            <br><br>
            Inactive customers: {inactive_customers:,}
        </div>
    </div>
    """, unsafe_allow_html=True)


# =====================================================
# 15. CUSTOMER TABLE
# =====================================================

st.markdown("---")
st.markdown("## 📋 Customer Explorer")
st.caption(
    "Search, review and download customer-level RFM information."
)

display_columns = [
    "CustomerID",
    "Recency",
    "Frequency",
    "Monetary",
    "R_Score",
    "F_Score",
    "M_Score",
    "RFM_Score",
    "Segment"
]

customer_table = filtered_data[
    display_columns
].sort_values(
    "Monetary",
    ascending=False
)

st.dataframe(
    customer_table,
    use_container_width=True,
    hide_index=True,
    height=400
)

csv_data = customer_table.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "⬇️ Download Customer Report",
    data=csv_data,
    file_name="retail_customer_report.csv",
    mime="text/csv"
)


# =====================================================
# 16. ANOMALY DETECTION
# =====================================================

st.markdown("---")
st.markdown("## 🚨 Anomaly Detection")

if anomaly_df is not None and not anomaly_df.empty:

    st.caption(
        "Records from the saved anomaly detection output."
    )

    a1, a2 = st.columns(2)

    with a1:
        st.metric(
            "Detected Anomaly Records",
            f"{len(anomaly_df):,}"
        )

    with a2:
        st.metric(
            "Anomaly Dataset Columns",
            f"{len(anomaly_df.columns)}"
        )

    st.dataframe(
        anomaly_df,
        use_container_width=True,
        hide_index=True,
        height=350
    )

    anomaly_csv = anomaly_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "⬇️ Download Anomaly Report",
        data=anomaly_csv,
        file_name="customer_anomalies.csv",
        mime="text/csv"
    )

else:

    st.info(
        "Anomaly dataset not found or contains no records. "
        "Check customer_anomalies.csv in data/processed."
    )


# =====================================================
# 17. FOOTER
# =====================================================

st.markdown("---")

st.markdown("""
<div class="footer">
    <b>RetailIQ | Customer Intelligence Dashboard</b><br>
    Machine Learning Project • Customer Segmentation • RFM Analytics
    <br><br>
    Built with Python, Pandas, Plotly and Streamlit
</div>
""", unsafe_allow_html=True)
