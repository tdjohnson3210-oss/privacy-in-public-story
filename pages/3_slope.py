import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="Slide 3 — Slope: Public vs Private Categories",
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
st.markdown("<h1 style='text-align:center;'>Public vs Private Patterns Across Privacy Offense Categories</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#3182bd;'>Slope Graph: How Offense Categories Shift Between Private and Public Spaces</h3>", unsafe_allow_html=True)

# Load from session_state
if "df_privacy" not in st.session_state:
    st.error("df_privacy is not loaded in session_state. Load it on the first page.")
    st.stop()

df = st.session_state.df_privacy.copy()

# Public vs Private
df["space_type"] = df["privacy_location"].apply(
    lambda x: "Private" if x == "Residential" else "Public"
)

# Pattern 1 categories
def categorize(pt):
    if pt in ["PUBLIC PEACE VIOLATION", "PUBLIC INDECENCY", "OBSCENITY"]:
        return "Public-Heavy Offenses"
    elif pt in ["STALKING", "INTIMIDATION", "BOUNDARY VIOLATION"]:
        return "Private-Heavy Offenses"
    elif pt == "CRIMINAL TRESPASS":
        return "Mixed Offense"
    else:
        return "Other"

df["category"] = df["primary_type"].apply(categorize)

# Compute counts
summary = (
    df.groupby(["category", "space_type"])
    .size()
    .reset_index(name="count")
)

# Compute share
total_by_cat = summary.groupby("category")["count"].sum().reset_index(name="total")
summary = summary.merge(total_by_cat, on="category")
summary["share"] = summary["count"] / summary["total"]

# Pivot for slope graph
pivot = summary.pivot(index="category", columns="space_type", values="share").reset_index()
pivot = pivot.fillna(0)

# Sort by public share
pivot = pivot.sort_values("Public", ascending=False)

# Build slope graph
fig = go.Figure()

for _, row in pivot.iterrows():
    fig.add_trace(go.Scatter(
        x=[0, 1],
        y=[row["Private"], row["Public"]],
        mode="lines+markers+text",
        text=[
            f"{row['category']} ({row['Private']*100:.1f}%)",
            f"{row['category']} ({row['Public']*100:.1f}%)"
        ],
        textposition="middle right",
        line=dict(width=3, color="#6baed6"),
        marker=dict(size=10, color="#08519c"),
        hovertemplate=f"{row['category']}<br>Private: {row['Private']*100:.1f}%<br>Public: {row['Public']*100:.1f}%"
    ))

fig.update_layout(
    title="Distribution Shift by Offense Category (Private → Public)",
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
