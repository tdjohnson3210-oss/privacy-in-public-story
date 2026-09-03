import streamlit as st
import plotly.express as px
import pandas as pd
import requests
from io import BytesIO

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
nav1, nav2 = st.columns([1,1])
with nav1:
    if st.button("Previous"):
        st.switch_page("overview.py")
with nav2:
    if st.button("Next"):
        st.switch_page("pages/2_arrest_rate.py")

# Retrieve survey responses
q1 = st.session_state.get("q1", "")
q2 = st.session_state.get("q2", "")

# Title/subtitle
st.markdown("<h1 style='text-align:center;'>Arrest Outcomes in Privacy‑Related Incidents</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#3182bd;'>Chicago Crime Data • 2001–Present • Privacy‑Linked Case Subset (~3%)</h3>", unsafe_allow_html=True)

# Clean narrative formatting
st.markdown(f"""
<div style="max-width: 780px; margin-left:auto; margin-right:auto; font-size:1.05rem; line-height:1.6; padding-top:10px;">

<p>Your survey responses indicate:</p>
<ul style="list-style-type:none; padding-left:0;">
    <li><strong style="color:#3182bd;">• Time spent in public spaces: {q1}</strong></li>
    <li><strong style="color:#3182bd;">• Experiences of discomfort or feeling watched: {q2}</strong></li>
    <li><strong style="color:#3182bd;">• Where privacy intrusions are most likely to occur: {st.session_state.get("q3", "")}</strong></li>
    <li><strong style="color:#3182bd;">• When privacy intrusions are most common: {st.session_state.get("q4", "")}</strong></li>
</ul>

<p>To keep the visualization lightweight and responsive, the chart below uses a simple latitude–longitude scatter instead of a full map. 
Even without basemap tiles, the spread of points makes the pattern clear: privacy‑related incidents occur across the entire city, not 
clustered in any single neighborhood. This “map‑like” view preserves the geographic story while avoiding the performance issues of 
tile‑based mapping.</p>

</div>
""", unsafe_allow_html=True)

# Load data
df_privacy = pd.read_parquet(
    BytesIO(
        requests.get(
            "https://mygcuedu6961-my.sharepoint.com/:u:/g/personal/tjohnson779_my_gcu_edu/IQCth27bkUiKTL_u9yv-p5AIAR81_4SFGqJsceC7kFq7cpM?download=1"
        ).content
    )
)

# Clean coordinates
df_privacy = df_privacy[
    df_privacy["latitude"].notna() &
    df_privacy["longitude"].notna()
]

df_privacy["latitude"] = df_privacy["latitude"].astype(float)
df_privacy["longitude"] = df_privacy["longitude"].astype(float)

# Convert arrest to readable label
df_privacy["arrest_label"] = df_privacy["arrest"].map({
    True: "Arrest Made",
    False: "No Arrest"
})

# Dropdown filter
primary_types = sorted(df_privacy["primary_type"].unique())
selected_type = st.selectbox("Filter by Case Type", ["All"] + primary_types)

df_filtered = (
    df_privacy if selected_type == "All"
    else df_privacy[df_privacy["primary_type"] == selected_type]
)

# Sample
if len(df_filtered) > 8000:
    df_filtered = df_filtered.sample(8000, random_state=42)

# Build map
fig = px.scatter(
    df_filtered,
    x="longitude",
    y="latitude",
    color="arrest_label",
    opacity=0.55,
    hover_data=["primary_type", "privacy_location", "time_of_day"],
    color_discrete_map={
        "Arrest Made": "#4c8bf5",
        "No Arrest": "#9bbcf5"
    },
    height=600
)

fig.update_xaxes(
    visible=False,
    showgrid=False,
    zeroline=False,
    showticklabels=False
)
fig.update_yaxes(
    visible=False,
    showgrid=False,
    zeroline=False,
    showticklabels=False
)

fig.update_layout(
    title="Geographic Spread of Privacy‑Related Incidents (Map‑Like Scatter)",
    margin={"r":0,"t":40,"l":0,"b":0},
    plot_bgcolor="#0e1117",   
    paper_bgcolor="#0e1117",
    font_color="white",
    showlegend=True,
    legend=dict(
        bgcolor="#0e1117",
        bordercolor="#0e1117"
    )
)
st.plotly_chart(fig, use_container_width=True)
