import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="Slide 3 — Public vs Private Patterns",
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
cols = st.columns([1,1,8])
if cols[0].button("← Previous"):
    st.switch_page("pages/2_arrest_rate.py")
if cols[1].button("Next →"):
    st.switch_page("pages/4_layered.py")

# Title
st.markdown("<h1 style='text-align:center;'>Public vs Private Patterns Across Privacy Offense Categories</h1>", unsafe_allow_html=True)

# Brief explanation
st.markdown("""
<div style='text-align:center; font-size:18px; color:#cfcfcf; max-width:900px; margin:auto;'>
Privacy-related offenses fall into three natural behavioral patterns.  
<strong style='color:#ff6b6b;'>Public-heavy offenses</strong> (e.g., Public Indecency, Obscenity) occur overwhelmingly in public spaces.  
<strong style='color:#4da6ff;'>Private-heavy offenses</strong> (e.g., Stalking, Intimidation) cluster in private environments.  
<strong style='color:#f4d35e;'>Mixed offenses</strong> (Criminal Trespass) appear in both settings.  
This slope shows how each category shifts from private → public.
</div>
""", unsafe_allow_html=True)

# Load data
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
        return None

df["category"] = df["primary_type"].apply(categorize)
df = df.dropna(subset=["category"])

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

# Pivot
pivot = summary.pivot(index="category", columns="space_type", values="share").reset_index()
pivot = pivot.fillna(0)

# Colors mapped to meaning
color_map = {
    "Public-Heavy Offenses": "#ff6b6b",   # red
    "Private-Heavy Offenses": "#4da6ff",  # blue
    "Mixed Offense": "#f4d35e"            # gold
}

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
        line=dict(width=4, color=color_map[row["category"]]),
        marker=dict(size=12, color=color_map[row["category"]]),
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
    margin={"r":20,"t":50,"l":20,"b":20},
    showlegend=False  # REMOVE LEGEND
)

st.plotly_chart(fig, use_container_width=True)
