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
if cols[0].button("Previous"):
    st.switch_page("pages/2_arrest_rate.py")
if cols[1].button("Next"):
    st.switch_page("pages/4_layered.py")

# Title
st.markdown("<h1 style='text-align:center;'>Public vs Private Patterns Across Privacy Offense Categories</h1>", unsafe_allow_html=True)

# Explanation
st.markdown("""
<div style='text-align:center; font-size:18px; color:#cfcfcf; max-width:900px; margin:auto;'>
Privacy-related offenses fall into three natural behavioral patterns.  
<strong style='color:#1B4F72;'>Public-heavy offenses</strong> occur overwhelmingly in public spaces.  
<strong style='color:#117A65;'>Private-heavy offenses</strong> cluster in private environments.  
<strong style='color:#E67E22;'>Mixed offenses</strong> appear in both settings.  
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

# Pattern categories
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

# Case types inside each category
case_types_map = {
    "Public-Heavy Offenses": [
        "PUBLIC PEACE VIOLATION",
        "PUBLIC INDECENCY",
        "OBSCENITY"
    ],
    "Private-Heavy Offenses": [
        "STALKING",
        "INTIMIDATION",
        "BOUNDARY VIOLATION"
    ],
    "Mixed Offense": [
        "CRIMINAL TRESPASS"
    ]
}

# Measure counts
summary = (
    df.groupby(["category", "space_type"])
    .size()
    .reset_index(name="count")
)

# Measure shares
total_by_cat = summary.groupby("category")["count"].sum().reset_index(name="total")
summary = summary.merge(total_by_cat, on="category")
summary["share"] = summary["count"] / summary["total"]

# Pivot
pivot = summary.pivot(index="category", columns="space_type", values="share").reset_index()
pivot = pivot.fillna(0)

color_map = {
    "Public-Heavy Offenses": "#1B4F72",
    "Private-Heavy Offenses": "#117A65",
    "Mixed Offense": "#E67E22"
}

# Build slope graph
fig = go.Figure()

for _, row in pivot.iterrows():
    category = row["category"]
    case_list = "<br>".join(case_types_map[category])

    fig.add_trace(go.Scatter(
        x=[0, 1],
        y=[row["Private"], row["Public"]],
        mode="lines+markers+text",
        text=[
            f"{category} ({row['Private']*100:.1f}%)",
            f"{category} ({row['Public']*100:.1f}%)"
        ],
        textposition="middle right",
        line=dict(width=4, color=color_map[category]),
        marker=dict(size=12, color=color_map[category]),
        hovertemplate=(
            f"<b>{category}</b><br>"
            f"<b>Case Types:</b><br>{case_list}<br><br>"
            f"Private Share: {row['Private']*100:.1f}%<br>"
            f"Public Share: {row['Public']*100:.1f}%<extra></extra>"
        )
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
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)
