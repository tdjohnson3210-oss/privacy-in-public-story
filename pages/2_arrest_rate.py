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

volume_df = df_privacy.groupby("primary_type").size().reset_index(name="total_cases")

rate_df["percent"] = rate_df["count"] / rate_df.groupby("primary_type")["count"].transform("sum") * 100
arrest_rates = rate_df[rate_df["arrest"]].merge(volume_df, on="primary_type")

# Sort by arrest rate
arrest_rates = arrest_rates.sort_values("percent", ascending=True)

# Horizontal bar chart (updated)
fig = px.bar(
    arrest_rates,
    y="primary_type",
    x="percent",
    color="total_cases",
    orientation="h",
    color_continuous_scale=["#c6dbef", "#6baed6", "#2171b5", "#084594"],
    labels={
        "primary_type": "",
        "percent": "Arrest Rate (%)",
        "total_cases": "Total Case Volume"
    },
    title="Arrest Rate by Case Type (Colored by Total Case Volume)"
)

fig.update_layout(
    xaxis_title="Arrest Rate (%)",
    yaxis_title="",
    paper_bgcolor="#0e1117",
    plot_bgcolor="#0e1117",
    font_color="#e0e0e0",
    margin={"r":20,"t":50,"l":20,"b":20}
)

ct = arrest_rates[arrest_rates["primary_type"] == "CRIMINAL TRESPASS"].iloc[0]
fig.add_annotation(
    y=ct["primary_type"],
    x=ct["percent"],
    text=f"<b>High volume, low arrest rate</b><br>({ct['percent']:.1f}%)",
    showarrow=True,
    arrowhead=2,
    ax=60,
    ay=0,
    font=dict(color="#f4d35e", size=12),
    bgcolor="rgba(20,20,20,0.75)",
    bordercolor="#f4d35e",
    borderwidth=1,
    align="left"
)

# Legend note
fig.add_annotation(
    x=0.98,
    y=0.95,
    xref="paper",
    yref="paper",
    text="",
    showarrow=False,
    font=dict(color="#e0e0e0", size=12),
    align="right"
)

st.plotly_chart(fig, use_container_width=True)
