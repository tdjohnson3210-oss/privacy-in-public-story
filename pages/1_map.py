import streamlit as st
import plotly.express as px
import pandas as pd

# Remove sidebar
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
    st.switch_page("overview.py")
if st.button("Next"):
    st.switch_page("pages/2_arrest_rate.py")

# Retrieve survey responses
q1 = st.session_state.get("q1", "")
q2 = st.session_state.get("q2", "")

# Title/subtitle
st.markdown("<h1 style='text-align:center;'>Arrest Outcomes in Privacy‑Related Incidents</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#3182bd;'>Chicago Crime Data • 2001–Present • Privacy‑Linked Case Subset (~3%)</h3>", unsafe_allow_html=True)

# Survey responses highlighted
st.markdown(f"""
<div style="max-width: 750px; margin-left:auto; margin-right:auto; font-size:1.05rem; line-height:1.6;">
    <p>Your survey responses indicate:</p>
    <ul style="list-style-type:none; padding-left:0;">
        <li><strong style="color:#3182bd;">• Time spent in public spaces: {q1}</strong></li>
        <li><strong style="color:#3182bd;">• Experiences of discomfort or feeling watched: {q2}</strong></li>
        <li><strong style="color:#3182bd;">• Where privacy intrusions are most likely to occur: {st.session_state.get("q3", "")}</strong></li>
        <li><strong style="color:#3182bd;">• When privacy intrusions are most common: {st.session_state.get("q4", "")}</strong></li>
    </ul>
   <p>To connect these perceptions to real‑world patterns, we turn to our pilot site: Chicago. Privacy‑related cases make up only about <strong>3%</strong> 
   of all reported crimes since 2001, yet they highlight how differently people experience and enforce boundaries in shared public spaces. And even at such 
   a small share of the overall caseload, the map shows these grouped privacy offenses scattered across the entire Chicago area, a reminder that boundary‑intrusion 
   incidents aren’t isolated to one neighborhood or demographic, but happen wherever people move through and share space.</p>
</div>
""", unsafe_allow_html=True)

# Load data
df_privacy = pd.read_parquet("chicago_crime_snapshot_08242026.parquet")

# Dropdown filter for primary case type
primary_types = sorted(df_privacy["primary_type"].unique())
selected_type = st.selectbox("Filter by Case Type", ["All"] + primary_types)

# Apply filter
df_filtered = (
    df_privacy if selected_type == "All"
    else df_privacy[df_privacy["primary_type"] == selected_type]
)

# Map viz: Arrest vs. Non Arrest
fig = px.scatter_mapbox(
    df_filtered,
    lat="latitude",
    lon="longitude",
    hover_name="primary_type",
    hover_data={
        "Location Type": df_filtered["privacy_location"],
        "Time of Day": df_filtered["time_of_day"],
        "Arrest Made": df_filtered["arrest"]
    },
    color="arrest",
    color_discrete_map={
        True: "#084594",
        False: "#c6dbef"
    },
    zoom=10,
    height=600
)

fig.update_traces(
    marker=dict(
        size=df_filtered["arrest"].map({True: 11, False: 6}),
        opacity=df_filtered["arrest"].map({True: 0.95, False: 0.28}),
        symbol="circle"
    )
)

fig.update_layout(
    mapbox_style="open-street-map",
    margin={"r":0,"t":0,"l":0,"b":0},
    legend_title_text="Arrest Status"
)
st.plotly_chart(fig)