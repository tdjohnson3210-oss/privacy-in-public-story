import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

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
    st.switch_page("pages/1_map.py")
if st.button("Next"):
    st.switch_page("pages/3_slope.py")

# Titles
st.markdown("<h1 style='text-align:center; color:#f2f2f2;'>Arrest Rate Across Privacy‑Related Case Types</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#7db3ff;'>Which Privacy‑Linked Incidents Most Often Lead to Arrest?</h3>", unsafe_allow_html=True)

df_privacy = st.session_state.df_privacy.copy()

# Narrative
st.markdown("""
<div style="max-width: 750px; margin-left:auto; margin-right:auto; font-size:1.05rem; line-height:1.6; color:#e0e0e0;">
Arrest rate shows how often a privacy‑related case results in someone being taken into custody. 
But arrest rate alone doesn’t tell the full story — some case types are rare but heavily enforced, 
while others are extremely common but rarely lead to arrest. This chart shows both the <strong>arrest rate</strong> 
and the <strong>total number of cases</strong> to give a fuller picture of enforcement patterns.
</div>
""", unsafe_allow_html=True)

# Compute arrest rate + volume
rate_df = (
    df_privacy.groupby(["primary_type", "arrest"])
    .size()
    .reset_index(name="count")
)

# Total volume per type
volume_df = df_privacy.groupby("primary_type").size().reset_index(name="total_cases")

# Merge
rate_df["percent"] = rate_df["count"] / rate_df.groupby("primary_type")["count"].transform("sum") * 100
arrest_rates = rate_df[rate_df["arrest"]].merge(volume_df, on="primary_type")

# Sort by arrest rate
arrest_rates = arrest_rates.sort_values("percent", ascending=False)

# Advanced bar chart
fig = px.bar(
    arrest_rates,
    x="primary_type",
    y="percent",
    color="total_cases",
    color_continuous_scale=["#c6dbef", "#6baed6", "#2171b5", "#084594"],
    labels={
        "primary_type": "",
        "percent": "Arrest Rate (%)",
        "total_cases": "Total Case Volume"
    },
    title="Arrest Rate by Case Type (Colored by Total Case Volume)"
)

fig.update_layout(
    coloraxis_colorbar=dict(
        title="Case Volume",
        tickfont=dict(color="#e0e0e0"),
        titlefont=dict(color="#e0e0e0")
    ),
    xaxis_tickangle=-45,
    margin={"r":0,"t":50,"l":0,"b":0},
    paper_bgcolor="#0e1117",
    plot_bgcolor="#0e1117",
    font_color="#e0e0e0"
)

# Annotation: highlight Criminal Trespass
ct = arrest_rates[arrest_rates["primary_type"] == "CRIMINAL TRESPASS"].iloc[0]
fig.add_annotation(
    x=ct["primary_type"],
    y=ct["percent"],
    text=f"High volume,\nlow arrest rate\n({ct['percent']:.1f}%)",
    showarrow=True,
    arrowhead=2,
    ax=20,
    ay=-40,
    font=dict(color="#ff6b6b", size=12),
)

st.plotly_chart(fig, use_container_width=True)
