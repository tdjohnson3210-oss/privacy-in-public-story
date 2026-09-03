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

if st.button("Previous"):
    st.switch_page("pages/1_map.py")
if st.button("Next"):
    st.switch_page("pages/3_slope.py")

st.markdown("<h1 style='text-align:center;'>Arrest Rate Across Privacy‑Related Case Types</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#3182bd;'>Which Privacy‑Linked Incidents Most Often Lead to Arrest?</h3>", unsafe_allow_html=True)

df_privacy = st.session_state.df_privacy.copy()

st.markdown("""
<div style="max-width: 750px; margin-left:auto; margin-right:auto; font-size:1.05rem; line-height:1.6;">
Arrest rate gives us a sense of how often a privacy‑related case actually leads to someone being taken into custody, and the differences across case types are hard to miss. 
Public Indecency shows the strongest enforcement response, while <strong>Criminal Trespass</strong>, even though it makes up the majority of privacy‑related cases, is far less likely to result in arrest. 
Seeing those contrasts makes it easier to imagine how these incidents play out in everyday life. Most people spend their days moving through shared public spaces, and even though 
privacy‑related incidents make up a minority share of Chicago’s overall caseload, they still show up everywhere. The map makes that clear: these grouped offenses aren’t clustered 
in one hotspot or tied to a single neighborhood. They’re spread across the entire city, reminding us that boundary‑intrusion moments can happen anywhere people live, commute, or simply coexist.
</div>
""", unsafe_allow_html=True)

rate_df = df_privacy.groupby(["primary_type", "arrest"]).size().reset_index(name="count")
rate_df["percent"] = rate_df["count"] / rate_df.groupby("primary_type")["count"].transform("sum") * 100
arrest_rates = rate_df[rate_df["arrest"]].sort_values("percent", ascending=False)

fig = px.bar(
    arrest_rates,
    x="primary_type",
    y="percent",
    color="percent",
    color_continuous_scale=["#c6dbef", "#6baed6", "#2171b5", "#084594"],
    labels={"primary_type": "", "percent": "Arrest Rate (%)"},
    title="Arrest Rate by Privacy‑Related Case Type"
)

fig.update_layout(
    coloraxis_showscale=False,
    xaxis_tickangle=-45,
    margin={"r":0,"t":50,"l":0,"b":0}
)

ct = arrest_rates[arrest_rates["primary_type"] == "CRIMINAL TRESPASS"].iloc[0]
fig.add_annotation(
    x=ct["primary_type"],
    y=ct["percent"],
    text=f"Criminal Trespass Arrest Rate\n({ct['percent']:.1f}%)",
    showarrow=True,
    arrowhead=2,
    ax=20,
    ay=-40,
    font=dict(color="red", size=12),
)

st.plotly_chart(fig, use_container_width=True)
