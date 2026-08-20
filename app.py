import os
import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Logistics Intelligence",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_PATH = "data/APL_Logistics.csv"

REQUIRED_COLUMNS = [
    "Days for shipping (real)",
    "Days for shipment (scheduled)",
    "Late_delivery_risk",
    "Market",
    "Order Region",
    "Shipping Mode",
    "Customer Segment",
]

# ============================================================
# SESSION STATE
# ============================================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "theme" not in st.session_state:
    st.session_state.theme = "day"

# ============================================================
# THEME
# ============================================================
DAY_CSS = """
<style>
.stApp, .main { background-color: #f5f7fb; color: #172033; }
[data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e4e7ec; }
[data-testid="stSidebar"] * { color: #172033 !important; }
h1, h2, h3, h4, h5 { color: #172033 !important; }
p, label { color: #475467 !important; }
div[data-baseweb="select"] > div { background-color: #ffffff !important; border-color: #d0d5dd !important; }
div[data-baseweb="select"] * { color: #172033 !important; }
.stButton > button, .stDownloadButton > button {
    background-color: #ffffff; color: #172033; border: 1px solid #d0d5dd; border-radius: 10px;
}
.stButton > button:hover { background-color: #f2f4f7; border-color: #98a2b3; }
.metric-card {
    background-color: #ffffff; border: 1px solid #e4e7ec; border-radius: 18px;
    padding: 20px; min-height: 120px; box-shadow: 0 5px 20px rgba(0,0,0,0.05);
}
.metric-title { color: #667085 !important; font-size: 14px; margin-bottom: 8px; }
.metric-value { color: #172033 !important; font-size: 28px; font-weight: 800; }
[data-testid="stDataFrame"], [data-testid="stExpander"] { border: 1px solid #e4e7ec; background-color:#ffffff; }
button[data-baseweb="tab"] { color: #667085 !important; }
button[data-baseweb="tab"][aria-selected="true"] { color: #172033 !important; }
.login-wrapper { background-color: #ffffff; border: 1px solid #e4e7ec; box-shadow: 0 20px 60px rgba(0,0,0,0.10); }
.login-title { color: #172033 !important; }
.login-subtitle { color: #667085 !important; }
</style>
"""

NIGHT_CSS = """
<style>
.stApp, .main { background-color: #080d1a; color: #f8fafc; }
[data-testid="stSidebar"] { background-color: #0f172a; border-right: 1px solid #1e293b; }
[data-testid="stSidebar"] * { color: #e5e7eb !important; }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3, [data-testid="stSidebar"] h4 { color: #f8fafc !important; }
h1, h2, h3, h4, h5 { color: #f8fafc !important; }
p, label { color: #cbd5e1 !important; }
div[data-baseweb="select"] > div { background-color: #111827 !important; border-color: #334155 !important; color: #f8fafc !important; }
div[data-baseweb="select"] * { color: #f8fafc !important; }
.stButton > button, .stDownloadButton > button {
    background-color: #111827; color: #f8fafc; border: 1px solid #334155; border-radius: 10px;
}
.stButton > button:hover { background-color: #1e293b; border-color: #64748b; }
.metric-card {
    background-color: #111827; border: 1px solid #263247; border-radius: 18px;
    padding: 20px; min-height: 120px; box-shadow: 0 8px 25px rgba(0,0,0,0.30);
}
.metric-title { color: #94a3b8 !important; font-size: 14px; margin-bottom: 8px; }
.metric-value { color: #f8fafc !important; font-size: 28px; font-weight: 800; }
button[data-baseweb="tab"] { color: #94a3b8 !important; }
button[data-baseweb="tab"][aria-selected="true"] { color: #f8fafc !important; }
[data-testid="stDataFrame"], [data-testid="stExpander"] { border: 1px solid #263247; background-color:#111827; }
.login-wrapper { background-color: #111827; border: 1px solid #263247; box-shadow: 0 20px 60px rgba(0,0,0,0.40); }
.login-title { color: #f8fafc !important; }
.login-subtitle { color: #94a3b8 !important; }
</style>
"""


def apply_theme():
    st.markdown(DAY_CSS if st.session_state.theme == "day" else NIGHT_CSS, unsafe_allow_html=True)


apply_theme()

# ============================================================
# LOGIN SCREEN
# ============================================================
def login_screen():
    st.markdown(
        """
        <style>
        .login-container { max-width: 500px; margin: 70px auto 20px auto; }
        .login-wrapper { padding: 40px; border-radius: 25px; text-align: center; }
        .login-logo { font-size: 65px; }
        .login-title { font-size: 32px; font-weight: 800; margin-top: 10px; }
        .login-subtitle { margin-top: 8px; margin-bottom: 25px; }
        </style>
        <div class="login-container">
            <div class="login-wrapper">
                <div class="login-logo">🚚</div>
                <div class="login-title">Logistics Intelligence</div>
                <div class="login-subtitle">Secure Supply Chain Analytics Portal</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    username = st.text_input("👤 Username", placeholder="Enter username")
    password = st.text_input("🔑 Password", type="password", placeholder="Enter password")
    login = st.button("🔓 Login", use_container_width=True)

    if login:
        if username == "admin" and password == "admin123":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("❌ Invalid username or password")

    with st.expander("ℹ️ Demo Credentials"):
        st.write("Username: `admin`")
        st.write("Password: `admin123`")


if not st.session_state.authenticated:
    login_screen()
    st.stop()

# ============================================================
# LOAD DATA (with guards)
# ============================================================
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Data file not found at '{path}'.")
    return pd.read_csv(path, encoding="latin1")


try:
    df = load_data(DATA_PATH)
except FileNotFoundError as e:
    st.error(
        f"🚫 {e}\n\n"
        f"Make sure the CSV exists relative to the folder you run "
        f"`streamlit run` from, e.g. `{os.path.abspath(DATA_PATH)}`."
    )
    st.stop()
except Exception as e:
    st.error(f"🚫 Failed to load data: {e}")
    st.stop()

missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
if missing_cols:
    st.error(
        "🚫 The CSV is missing required column(s): "
        + ", ".join(f"`{c}`" for c in missing_cols)
        + "\n\nAvailable columns: " + ", ".join(f"`{c}`" for c in df.columns)
    )
    st.stop()

# ============================================================
# DATA CLEANING
# ============================================================
numeric_columns = [
    "Days for shipping (real)",
    "Days for shipment (scheduled)",
    "Late_delivery_risk",
]
for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

df["Delay_Gap"] = df["Days for shipping (real)"] - df["Days for shipment (scheduled)"]

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("## 🚚 Logistics Intelligence")
    st.caption("Global Supply Chain Analytics")
    st.divider()

    st.markdown("### 🎨 Appearance")
    button_text = "🌙 Night Mode" if st.session_state.theme == "day" else "☀️ Day Mode"
    if st.button(button_text, use_container_width=True):
        st.session_state.theme = "night" if st.session_state.theme == "day" else "day"
        st.rerun()

    st.divider()
    st.markdown("### 🔎 Filters")

    def options_for(col):
        return ["All"] + sorted(df[col].dropna().unique().tolist())

    selected_market = st.selectbox("🌎 Market", options_for("Market"))
    selected_region = st.selectbox("📍 Region", options_for("Order Region"))
    selected_shipping = st.selectbox("🚚 Shipping Mode", options_for("Shipping Mode"))
    selected_segment = st.selectbox("👥 Customer Segment", options_for("Customer Segment"))

    st.divider()
    if st.button("🔒  Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# ============================================================
# FILTER DATA
# ============================================================
filtered_df = df.copy()
filters = {
    "Market": selected_market,
    "Order Region": selected_region,
    "Shipping Mode": selected_shipping,
    "Customer Segment": selected_segment,
}
for col, value in filters.items():
    if value != "All":
        filtered_df = filtered_df[filtered_df[col] == value]

plotly_template = "plotly_dark" if st.session_state.theme == "night" else "plotly_white"

# ============================================================
# HEADER
# ============================================================
st.markdown(
    """
    <div style="font-size:40px; font-weight:800; margin-bottom:5px;">
        🚚 Logistics Intelligence Dashboard
    </div>
    <div style="font-size:17px; margin-bottom:20px;">
        Delivery Performance • Delay Risk • Logistics Efficiency
    </div>
    """,
    unsafe_allow_html=True
)

if filtered_df.empty:
    st.warning("⚠️ No records match the selected filters. Try adjusting them in the sidebar.")
    st.stop()

# ============================================================
# KPI CALCULATIONS
# ============================================================
total_orders = len(filtered_df)
average_delay = filtered_df["Delay_Gap"].mean()
late_risk = filtered_df["Late_delivery_risk"].mean() * 100
on_time = (filtered_df["Late_delivery_risk"] == 0).mean() * 100
max_delay = filtered_df["Delay_Gap"].max()


def metric_card(title, value, icon):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">{icon} {title}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    metric_card("Total Orders", f"{total_orders:,}", "📦")
with c2:
    metric_card("Average Delay", f"{average_delay:.2f} Days", "⏱️")
with c3:
    metric_card("Late Risk", f"{late_risk:.2f}%", "⚠️")
with c4:
    metric_card("On-Time / Low Risk", f"{on_time:.2f}%", "✅")
with c5:
    metric_card("Maximum Delay", f"{max_delay:.2f} Days", "🔴")

st.divider()

# ============================================================
# TABS
# ============================================================
overview, regional, logistics, data_tab = st.tabs(
    ["📊 Overview", "🌎 Regional Analysis", "🚚 Logistics Analysis", "📋 Data Explorer"]
)

# ---------------- OVERVIEW ----------------
with overview:
    st.subheader("📊 Delivery Performance Overview")
    col1, col2 = st.columns(2)

    with col1:
        risk = filtered_df["Late_delivery_risk"].value_counts().reset_index()
        risk.columns = ["Risk", "Orders"]
        risk["Risk"] = risk["Risk"].map({0: "Low Risk", 1: "Late Risk"})
        fig = px.pie(
            risk, names="Risk", values="Orders", hole=0.55,
            title="Delivery Risk Distribution", template=plotly_template
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.histogram(
            filtered_df, x="Delay_Gap", nbins=25,
            title="Delay Distribution", template=plotly_template
        )
        fig.update_layout(xaxis_title="Delay Gap (Days)", yaxis_title="Orders")
        st.plotly_chart(fig, use_container_width=True)

# ---------------- REGIONAL ----------------
with regional:
    st.subheader("🌎 Regional Performance")

    region_analysis = (
        filtered_df.groupby("Order Region")
        .agg(
            Orders=("Order Region", "size"),
            Avg_Delay_Gap=("Delay_Gap", "mean"),
            Late_Risk_Rate=("Late_delivery_risk", "mean"),
        )
        .reset_index()
    )
    region_analysis["Avg_Delay_Gap"] = region_analysis["Avg_Delay_Gap"].round(2)
    region_analysis["Late_Risk_Rate"] = (region_analysis["Late_Risk_Rate"] * 100).round(2)

    top_regions = region_analysis.sort_values("Avg_Delay_Gap", ascending=False).head(15)
    fig = px.bar(
        top_regions, x="Avg_Delay_Gap", y="Order Region", orientation="h",
        title="Top Delayed Regions", template=plotly_template
    )
    fig.update_layout(xaxis_title="Average Delay Gap (Days)", yaxis_title="Order Region")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📋 Regional Performance Table")
    st.dataframe(
        region_analysis.sort_values("Late_Risk_Rate", ascending=False),
        use_container_width=True
    )

# ---------------- LOGISTICS ----------------
with logistics:
    st.subheader("🚚 Logistics Performance")
    col1, col2 = st.columns(2)

    with col1:
        shipping = (
            filtered_df.groupby("Shipping Mode")
            .agg(
                Orders=("Shipping Mode", "size"),
                Avg_Delay=("Delay_Gap", "mean"),
                Late_Risk=("Late_delivery_risk", "mean"),
            )
            .reset_index()
        )
        shipping["Late_Risk"] = (shipping["Late_Risk"] * 100).round(2)
        shipping["Avg_Delay"] = shipping["Avg_Delay"].round(2)

        fig = px.bar(
            shipping, x="Shipping Mode", y="Late_Risk",
            title="Late Risk by Shipping Mode", template=plotly_template
        )
        fig.update_layout(yaxis_title="Late Risk (%)")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        customer = (
            filtered_df.groupby("Customer Segment")
            .agg(
                Orders=("Customer Segment", "size"),
                Late_Risk=("Late_delivery_risk", "mean"),
            )
            .reset_index()
        )
        customer["Late_Risk"] = (customer["Late_Risk"] * 100).round(2)

        fig = px.bar(
            customer, x="Customer Segment", y="Late_Risk",
            title="Late Risk by Customer Segment", template=plotly_template
        )
        fig.update_layout(yaxis_title="Late Risk (%)")
        st.plotly_chart(fig, use_container_width=True)

# ---------------- DATA EXPLORER ----------------
with data_tab:
    st.subheader("📋 Filtered Logistics Data")
    st.info(f"Showing {len(filtered_df):,} records based on the selected filters.")
    st.dataframe(filtered_df, use_container_width=True, height=500)

    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download Filtered CSV", csv, "filtered_logistics_data.csv",
        "text/csv", use_container_width=True
    )

# ============================================================
# FOOTER
# ============================================================
st.divider()
st.markdown(
    """
    <div style="text-align:center; padding:25px; border-radius:16px; margin-top:20px;">
        <h4>🚚 Logistics Intelligence</h4>
        <p>Delivery Performance • Delay Risk • Supply Chain Analytics</p>
        <p>Built with Python • Pandas • Plotly • Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)