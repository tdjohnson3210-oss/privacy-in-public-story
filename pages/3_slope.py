import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="Slide 3 — Slope: Criminal Trespass vs All Others",
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
st.markdown("<h1 style='text-align:center;'>Criminal Trespass vs All Other Privacy Offenses</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#3182bd;'>How Incident Distribution Shifts Between Private and Public Spaces</h3>", unsafe_allow_html=True)

# Load from session_state
if "df_privacy" not in st.session_state:
    st.error("df_privacy is not loaded in session_state. Load it on the first page.")
    st.stop()

df = st.session_state.df_privacy.copy()

# Public vs Private
df["space_type"] = df["privacy_location"].apply(
    lambda x: "Private" if x == "Residential" else "Public"
)

# Criminal vs All Others
df["group"] = df["primary_type"].apply(
    lambda x: "Criminal Trespass" if x == "CRIMINAL TRESPASS" else "All Other Offenses"
)

# Compute counts
summary = (
    df.groupby(["group", "space_type"])
    .size()
    .reset_index(name="count")
)

# Compute share
total_by_group = summary.groupby("group")["count"].sum().reset_index(name="total")
summary = summary.merge(total_by_group, on="group")
summary["share"] = summary["count"] / summary["total"]

# Pivot for slope graph
pivot = summary.pivot(index="group", columns="space_type", values="share").reset_index()
pivot = pivot.fillna(0)

# Build slope graph
fig = go.Figure()

for _, row in pivot.iterrows():
    fig.add_trace(go.Scatter(
        x=[0, 1],
        y=[row["Private"], row["Public"]],
        mode="lines+markers+text",
        text=[
            f"{row['group']} ({row['Private']*100:.1f}%)",
            f"{row['group']} ({row['Public']*100:.1f}%)"
        ],
        textposition="middle right",
        line=dict(width=3, color="#6baed6"),
        marker=dict(size=10, color="#08519c"),
        hovertemplate=f"{row['group']}<br>Private: {row['Private']*100:.1f}%<br>Public: {row['Public']*100:.1f}%"
    ))

fig.update_layout(
    title="Distribution Shift: Criminal Trespass vs All Other Offenses (Private → Public)",
    xaxis=dict(
        tickvals=[0, 1],
        ticktext=["Private", "Public"],
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(title="Incident Share (%)", tickformat=".0%"),
    paper_bgcolor="#0e1117",
    plot_bgcolor="#0e1117",
    font_color="#e0e0e0",
    margin={"r":20,"t":50,"l":20,"b":20}
)

st.plotly_chart(fig, use_container_width=True)
