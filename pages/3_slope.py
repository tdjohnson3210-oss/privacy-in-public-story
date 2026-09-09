import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="Slide 3 — Slope: Public vs Private Incident Volume",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide sidebar
hide_sidebar = """
    <style>
        [data-testid="stSidebar"] {display: none;}
        [data-testid="stSidebarNav"] {display: none;}
        [data-testid="collapsedControl"] {display: none;}
    </style>
"""
st.markdown(hide_sidebar, unsafe_allow_html=True)

# Navigation
if st.button("Previous"):
    st.switch_page("pages/2_arrest_rate.py")
if st.button("Next"):
    st.switch_page("pages/4_layered.py")

# Titles
st.markdown("<h1 style='text-align:center;'>How Privacy-Related Incidents Shift from Private to Public Spaces</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#3182bd;'>Slope Graph: Incident Volume Differences Across Case Types</h3>", unsafe_allow_html=True)

# Load from session_state
if "df_privacy" not in st.session_state:
    st.error("df_privacy is not loaded in session_state. Load it on the first page.")
    st.stop()

df = st.session_state.df_privacy.copy()

# Public vs Private
df["space_type"] = df["privacy_location"].apply(
    lambda x: "Private" if x == "Residential" else "Public"
)

# Compute incident counts
summary = (
    df.groupby(["primary_type", "space_type"])
    .size()
    .reset_index(name="count")
)

# Pivot for slope graph
pivot = summary.pivot(index="primary_type", columns="space_type", values="count").reset_index()

# Fill missing values with 0
pivot = pivot.fillna(0)

# Sort by public incident volume
pivot = pivot.sort_values("Public", ascending=False)

# Build slope graph
fig = go.Figure()

for _, row in pivot.iterrows():
    fig.add_trace(go.Scatter(
        x=[0, 1],
        y=[row["Private"], row["Public"]],
        mode="lines+markers+text",
        text=[
            f"{row['primary_type']} ({row['Private']})",
            f"{row['primary_type']} ({row['Public']})"
        ],
        textposition="middle right",
        line=dict(width=2, color="#6baed6"),
        marker=dict(size=8, color="#08519c"),
        hovertemplate=f"{row['primary_type']}<br>Private: {row['Private']} incidents<br>Public: {row['Public']} incidents"
    ))

fig.update_layout(
    title="Incident Volume Change by Case Type (Private → Public)",
    xaxis=dict(
        tickvals=[0, 1],
        ticktext=["Private", "Public"],
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(title="Incident Count"),
    paper_bgcolor="#0e1117",
    plot_bgcolor="#0e1117",
    font_color="#e0e0e0",
    margin={"r":20,"t":50,"l":20,"b":20}
)

st.plotly_chart(fig, use_container_width=True)
