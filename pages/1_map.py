import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from pathlib import Path
import pydeck as pdk

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

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
nav1, nav2 = st.columns([1,1])
with nav1:
    if st.button("Previous"):
        st.switch_page("overview.py")
with nav2:
    if st.button("Next"):
        st.switch_page("pages/2_arrest_rate.py")

# Accessible headings
st.markdown("<h1 style='text-align:center; color:#f2f2f2;'>Arrest Outcomes in Privacy‑Related Incidents</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#7db3ff;'>Chicago Crime Data • 2001–Present • Privacy‑Linked Case Subset (~3%)</h3>", unsafe_allow_html=True)

# Survey summary (clean, no extra text)
q1 = st.session_state.get("q1", "")
q2 = st.session_state.get("q2", "")

st.markdown(f"""
<div style="max-width: 780px; margin-left:auto; margin-right:auto; font-size:1.15rem; line-height:1.7; padding-top:10px; color:#e0e0e0;">
<p>Your survey responses indicate:</p>
<ul style="list-style-type:none; padding-left:0;">
    <li><strong style="color:#7db3ff;">• Time spent in public spaces: {q1}</strong></li>
    <li><strong style="color:#7db3ff;">• Experiences of discomfort or feeling watched: {q2}</strong></li>
    <li><strong style="color:#7db3ff;">• Where privacy intrusions are most likely to occur: {st.session_state.get("q3", "")}</strong></li>
    <li><strong style="color:#7db3ff;">• When privacy intrusions are most common: {st.session_state.get("q4", "")}</strong></li>
</ul>
</div>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_privacy_data():
    candidates = [
        Path(__file__).resolve().parents[1] / "chicago_crime_snapshot_08242026.parquet",
        Path(__file__).resolve().parents[1] / "chicago_crimes.parquet",
        Path(__file__).resolve().parents[1] / "data" / "chicago_crime_snapshot_08242026.parquet",
    ]
    for path in candidates:
        if path.exists():
            return pd.read_parquet(path)

    url = "https://www.dropbox.com/scl/fi/t457ji4mnih7zuegq4lzz/chicago_crime_snapshot_08242026.parquet?rlkey=ghoq2totei52mym13ai3d054r&st=01zmb58y&dl=1"
    response = requests.get(url, timeout=120)
    response.raise_for_status()

    content = response.content
    if not content.startswith(b"PAR1"):
        raise ValueError("Dataset URL did not return a Parquet file.")

    return pd.read_parquet(BytesIO(content))

if "df_privacy" not in st.session_state:
    st.session_state.df_privacy = load_privacy_data()

df_privacy = st.session_state.df_privacy.copy()

# Clean lat/lon
df_privacy = df_privacy[
    df_privacy["latitude"].notna() &
    df_privacy["longitude"].notna()
]
df_privacy["latitude"] = df_privacy["latitude"].astype(float)
df_privacy["longitude"] = df_privacy["longitude"].astype(float)

# Labels
df_privacy["arrest_label"] = df_privacy["arrest"].map({
    True: "Arrest Made",
    False: "Released"
})

# Filter
primary_types = sorted(df_privacy["primary_type"].unique())
selected_type = st.selectbox("Filter by Case Type", ["All"] + primary_types)

df_filtered = df_privacy if selected_type == "All" else df_privacy[df_privacy["primary_type"] == selected_type]

if len(df_filtered) > 8000:
    df_filtered = df_filtered.sample(8000, random_state=42)

# --- ANNOTATION ABOVE MAP ---
st.markdown("""
<div style="text-align:center; color:#cfcfcf; font-size:1.05rem; margin-top:20px; margin-bottom:10px;">
These incidents aren’t clustered in one neighborhood — they appear across the entire city.
</div>
""", unsafe_allow_html=True)

# --- REAL STREET MAP USING PYDECK (MAPLIBRE) ---
layer = pdk.Layer(
    "ScatterplotLayer",
    df_filtered,
    get_position=["longitude", "latitude"],
    get_fill_color=[
        "255 if arrest_label == 'Arrest Made' else 120",
        "180",
        "255",
        160
    ],
    radius_scale=2,
    radius_min_pixels=3,
)

view_state = pdk.ViewState(
    latitude=41.8781,
    longitude=-87.6298,
    zoom=10,
    pitch=0
)

map_style = "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"

r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style=map_style,
    tooltip={"text": "{primary_type}\n{privacy_location}\n{time_of_day}"}
)

st.pydeck_chart(r)
