import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="Slide 4 — What Time of Day Affects Arrest Rates",
    layout="wide",
    initial_sidebar_state="collapsed"
)

hide_sidebar = """
    <style>
        [data-testid="stSidebar"] {display: none;}
        [data-testid="stSidebarNav"] {display: none;}
        [data-testid="collapsedControl"] {display: none;}
    </style>
"""
st.markdown(hide_sidebar, unsafe_allow_html=True)

if st.button("Previous"):
    st.switch_page("pages/2_arrest_rate.py")
if st.button("Next"):
    st.switch_page("pages/4_layered.py")

st.markdown("<h1 style='text-align:center;'>Arrest Rate by Hour</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#3182bd;'>How Enforcement Shifts Across the Day in Public vs Private Spaces (across all case types)</h3>", unsafe_allow_html=True)

df = st.session_state.df_privacy.copy()

df["space_type"] = df["privacy_location"].apply(
    lambda x: "Private" if x == "Residential" else "Public"
)

df["hour"] = df["date"].dt.hour

total_df = df.groupby(["hour", "space_type"]).size().reset_index(name="total_incidents")
arrest_df = df[df["arrest"]].groupby(["hour", "space_type"]).size().reset_index(name="arrests")

merged = pd.merge(total_df, arrest_df, on=["hour", "space_type"], how="left")
merged["arrests"] = merged["arrests"].fillna(0)
merged["percent"] = merged["arrests"] / merged["total_incidents"] * 100

fig = px.area(
    merged,
    x="hour",
    y="percent",
    color="space_type",
    labels={"percent": "Arrest Rate (%)", "hour": "Hour of Day"},
    title="Arrest Rate Across the Day: Public vs Private Spaces",
    color_discrete_map={
        "Public": "#08519c",
        "Private": "#6baed6"
    }
)

for i, trace in enumerate(fig.data):
    trace.stackgroup = str(i)

fig.update_traces(mode="lines")
fig.update_layout(
    margin={"r":0,"t":50,"l":0,"b":0},
    legend_title_text="Space Type",
    yaxis=dict(range=[0, 100])
)

private_peak = merged[merged["space_type"] == "Private"].sort_values("percent", ascending=False).iloc[0]
fig.add_annotation(
    x=private_peak["hour"],
    y=private_peak["percent"],
    text=f"Private Peak: {private_peak['percent']:.1f}%",
    showarrow=True,
    arrowhead=2,
    ax=-40,
    ay=-40,
    font=dict(color="red", size=12),
    arrowcolor="red"
)

st.plotly_chart(fig, use_container_width=True)
