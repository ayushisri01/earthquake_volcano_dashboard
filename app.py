import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

from data_fetch import fetch_earthquakes, fetch_volcanoes
from geo_utils import haversine
from report_generator import generate_pdf_bytes

st.set_page_config(layout="wide")
st.title("🌋 Earthquake + Volcano Risk Intelligence Dashboard")

# Date range filter
st.sidebar.header("📆 Date & Filters")
start_date = st.sidebar.date_input("Start Date", datetime.now() - timedelta(days=1))
end_date = st.sidebar.date_input("End Date", datetime.now())
min_mag = st.sidebar.slider("Min Magnitude", 2.5, 10.0, 4.5, 0.1)
depth_range = st.sidebar.slider("Depth (km)", 0.0, 700.0, (0.0, 300.0))

# Load data
@st.cache_data(ttl=900)
def load_data():
    eqs = fetch_earthquakes(start_date, end_date)
    vols = fetch_volcanoes()
    return eqs, vols

eqs, vols = load_data()

# Apply filters
filtered_eqs = eqs[
    (eqs["mag"] >= min_mag) &
    (eqs["depth"] >= depth_range[0]) &
    (eqs["depth"] <= depth_range[1])
]

# KPIs
st.subheader("📊 Earthquake KPIs")
col1, col2, col3 = st.columns(3)
if not filtered_eqs.empty:
    col1.metric("Total Quakes", len(filtered_eqs))
    col2.metric("Avg Magnitude", round(filtered_eqs["mag"].mean(), 2))
    top_quake = filtered_eqs.loc[filtered_eqs["mag"].idxmax()]
    col3.metric("Strongest Quake", f"{top_quake['mag']} at {top_quake['place']}")
else:
    st.info("No earthquakes in this time range.")

# Heatmap
st.subheader("🗺️ Earthquake Map with Heat Intensity")
if not filtered_eqs.empty:
    fig = px.density_map(
        filtered_eqs,
        lat='lat',
        lon='lon',
        z='mag',
        radius=20,
        center=dict(lat=0, lon=0),
        zoom=1,
        title="Heatmap of Earthquake Magnitudes"
    )
    st.plotly_chart(fig, use_container_width=True)

# Volcano map
st.subheader("🌋 Volcano Locations")
fig_volcanoes = px.scatter_map(
    vols,
    lat="latitude",
    lon="longitude",
    hover_name="volcano_name",
    color_discrete_sequence=["red"],
    zoom=1,
    title="Global Volcanoes",
    center=dict(lat=0, lon=0)
)
st.plotly_chart(fig_volcanoes, use_container_width=True)

# Risk Alerts
st.subheader("🚨 Volcano Risk Alerts")
alerts = []
for _, eq in filtered_eqs.iterrows():
    for _, vol in vols.iterrows():
        dist = haversine(eq["lon"], eq["lat"], vol["longitude"], vol["latitude"])
        if dist < 100 and eq["mag"] >= 5.0:
            alerts.append({
                "quake_place": eq["place"],
                "mag": eq["mag"],
                "volcano_name": vol["volcano_name"],
                "distance_km": round(dist, 2)
            })

if alerts:
    st.warning(f"{len(alerts)} alert(s) triggered!")
    st.dataframe(pd.DataFrame(alerts))
else:
    st.success("No critical alerts.")

# PDF Report Download
st.subheader("🧾 Download Risk Summary Report")
if st.button("Generate PDF Report"):
    kpi_data = {
        "Total Quakes": len(filtered_eqs),
        "Average Magnitude": round(filtered_eqs["mag"].mean(), 2),
        "Max Magnitude": round(top_quake["mag"], 2)
    }
    pdf_bytes = generate_pdf_bytes(kpi_data, alerts)
    st.download_button(
        label="Download PDF Report",
        data=pdf_bytes,
        file_name="earthquake_volcano_report.pdf",
        mime="application/pdf"
    )

# Optional: Telegram Alert Setup
st.sidebar.markdown("🔔 Want real-time alerts? Set up a Telegram bot using BotFather and your chat ID.")
