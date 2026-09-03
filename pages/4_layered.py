import streamlit as st
import plotly.express as px
import pandas as pd

# Page config/hide sidebar
st.set_page_config(
    page_title="Slide 5 — Layered Trend Analysis",
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

# Navigation
if st.button("Previous"):
        st.switch_page("pages/3_slope.py")
if st.button("Next"):
    st.switch_page("pages/5_conclusion.py")

# Title/subtitle
st.markdown("<h1 style='text-align:center;'>When Criminal Trespass Peaks... and When It Doesn’t</h1>", unsafe_allow_html=True)

# Narrative
st.markdown("""
<div style="max-width: 750px; margin-left:auto; margin-right:auto; font-size:1.05rem; line-height:1.6; padding-top:10px;">
Looking at arrest rates across the day adds another layer to the story. Criminal Trespass makes up most of the privacy-related caseload, 
but its enforcement rhythm doesn’t mirror its volume. Across much of the day, its arrest rate stays steady, only rising as the city moves 
into the late evening hours. The remaining offenses follow a softer, more stable rhythm. Seeing these layers together shows how people 
experience enforcement in shared spaces: the offense that happens most often peaks later in the day, while the rest maintain a quieter profile. 
Time of day shapes not just when incidents occur, but how likely they are to escalate into enforcement.
</div>
""", unsafe_allow_html=True)

# Load data
df = pd.read_parquet("chicago_crime_snapshot_08242026.parquet")

# Create 'hour' column from datetime
df["hour"] = df["date"].dt.hour

# Criminal Trespass vs remaining case types
df["group"] = df["primary_type"].apply(
    lambda x: "Criminal Trespass" if x == "CRIMINAL TRESPASS" else "All Other Offenses"
)

# Compute arrest rate
total = df.groupby(["hour", "group"]).size().reset_index(name="total")
arrests = df[df["arrest"] == True].groupby(["hour", "group"]).size().reset_index(name="arrests")

merged = pd.merge(total, arrests, on=["hour", "group"], how="left")
merged["arrests"] = merged["arrests"].fillna(0)
merged["percent"] = (merged["arrests"] / merged["total"]) * 100

# Area chart
fig = px.area(
    merged,
    x="hour",
    y="percent",
    color="group",
    labels={"percent": "Arrest Rate (%)", "hour": "Hour of Day"},
    title="",
    color_discrete_map={
        "Criminal Trespass": "#08306b",
        "All Other Offenses": "#9ecae1"
    }
)

fig.for_each_trace(
    lambda t: t.update(opacity=0.9, line=dict(width=4)) if t.name == "Criminal Trespass"
    else t.update(opacity=0.5, line=dict(width=2))
)

for i, trace in enumerate(fig.data):
    trace.stackgroup = str(i)

# Shading
fig.add_shape(
    type="rect",
    x0=18, x1=23,
    y0=0, y1=100,
    fillcolor="rgba(20,20,20,0.15)",
    line_width=0,
    layer="below"
)

# Annotation
ct_peak = merged[merged["group"] == "Criminal Trespass"].sort_values("percent", ascending=False).iloc[0]
fig.add_annotation(
    x=ct_peak["hour"],
    y=ct_peak["percent"],
    text=f"Criminal Trespass Peak: {ct_peak['percent']:.1f}%",
    showarrow=True,
    arrowhead=2,
    ax=-100,
    ay=-50,
    font=dict(color="red", size=12),
    arrowcolor="red",
    bgcolor="white",
    bordercolor="red",
    borderwidth=1
)

fig.update_layout(
    margin={"r":0,"t":50,"l":0,"b":0},
    legend_title_text="Offense Group",
    yaxis=dict(range=[0, 100])
)
st.plotly_chart(fig, use_container_width=True)