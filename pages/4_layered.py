import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="Slide 5 — Layered Trend Analysis",
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
if st.button("Previous"):
    st.switch_page("pages/3_slope.py")
if st.button("Next"):
    st.switch_page("pages/5_conclusion.py")

# Title + Narrative
st.markdown("<h1 style='text-align:center;'>When Criminal Trespass Peaks... and When It Doesn’t</h1>", unsafe_allow_html=True)

st.markdown("""
<div style="max-width: 750px; margin-left:auto; margin-right:auto; font-size:1.05rem; line-height:1.6; padding-top:10px;">
Looking at arrest rates across the day adds another layer to the story. Criminal Trespass makes up most of the privacy-related caseload, 
but its enforcement rhythm doesn’t mirror its volume. Across much of the day, its arrest rate stays steady, only rising as the city moves 
into the late evening hours. The remaining offenses follow a softer, more stable rhythm. Seeing these layers together shows how people 
experience enforcement in shared spaces: the offense that happens most often peaks later in the day, while the rest maintain a quieter profile. 
Time of day shapes not just when incidents occur, but how likely they are to escalate into enforcement.
</div>
""", unsafe_allow_html=True)

# Data
df = st.session_state.df_privacy.copy()
df["hour"] = df["date"].dt.hour
df["group"] = df["primary_type"].apply(
    lambda x: "Criminal Trespass" if x == "CRIMINAL TRESPASS" else "All Other Offenses"
)

total = df.groupby(["hour", "group"]).size().reset_index(name="total")
arrests = df[df["arrest"]].groupby(["hour", "group"]).size().reset_index(name="arrests")

merged = pd.merge(total, arrests, on=["hour", "group"], how="left")
merged["arrests"] = merged["arrests"].fillna(0)
merged["percent"] = merged["arrests"] / merged["total"] * 100

# Color-blind-safe palette
color_map = {
    "Criminal Trespass": "#1B4F72",   # dark blue
    "All Other Offenses": "#117A65"   # dark teal
}

# Layered line chart (true layering)
fig = go.Figure()

for group in merged["group"].unique():
    subset = merged[merged["group"] == group]

    fig.add_trace(go.Scatter(
        x=subset["hour"],
        y=subset["percent"],
        mode="lines",
        name=group,
        line=dict(width=4, color=color_map[group]),
        opacity=0.75
    ))

# Evening shading window
fig.add_shape(
    type="rect",
    x0=18, x1=23,
    y0=0, y1=100,
    fillcolor="rgba(20,20,20,0.15)",
    line_width=0,
    layer="below"
)

# Peak annotation
ct_peak = merged[merged["group"] == "Criminal Trespass"].sort_values("percent", ascending=False).iloc[0]
fig.add_annotation(
    x=ct_peak["hour"],
    y=ct_peak["percent"],
    text=f"Peak Arrest Rate: {ct_peak['percent']:.1f}%",
    showarrow=True,
    arrowhead=2,
    ax=-80,
    ay=-40,
    font=dict(color="red", size=12),
    arrowcolor="red",
    bgcolor="white",
    bordercolor="red",
    borderwidth=1
)

# Layout improvements
fig.update_layout(
    title="Layered Arrest Rate Across the Day",
    xaxis=dict(
        title="Hour of Day",
        tickmode="array",
        tickvals=list(range(0, 25, 2)),
        ticktext=[f"{h}:00" for h in range(0, 25, 2)],
        gridcolor="rgba(255,255,255,0.1)"
    ),
    yaxis=dict(
        title="Arrest Rate (%)",
        range=[0, 100],
        tickmode="array",
        tickvals=list(range(0, 101, 10)),
        gridcolor="rgba(255,255,255,0.1)"
    ),
    legend_title_text="Offense Group",
    margin={"r":0,"t":50,"l":0,"b":0},
    paper_bgcolor="#0e1117",
    plot_bgcolor="#0e1117",
    font_color="#e0e0e0"
)

st.plotly_chart(fig, use_container_width=True)
