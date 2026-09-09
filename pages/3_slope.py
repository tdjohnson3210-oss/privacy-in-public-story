import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="Slide 4 — Public vs Private Arrest Rate",
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
    st.switch_page("pages/2_arrest_rate.py")
if st.button("Next"):
    st.switch_page("pages/4_layered.py")

# Titles
st.markdown("<h1 style='text-align:center;'>Arrest Rate: Public vs Private Spaces</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#3182bd;'>How Enforcement Differs When Privacy is Violated in Public vs Private Settings</h3>", unsafe_allow_html=True)

df = st.session_state.df_privacy.copy()

# Simplify space type
df["space_type"] = df["privacy_location"].apply(
    lambda x: "Private" if x == "Residential" else "Public"
)

# Compute arrest rate
summary = (
    df.groupby("space_type")["arrest"]
    .mean()
    .reset_index()
)

summary["percent"] = summary["arrest"] * 100
summary = summary.sort_values("percent", ascending=False)

# Build slope graph
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=[0, 1],
    y=summary["percent"],
    mode="lines+markers+text",
    text=[f"Public ({summary['percent'].iloc[0]:.1f}%)",
          f"Private ({summary['percent'].iloc[1]:.1f}%)"],
    textposition="middle right",
    line=dict(width=3, color="#6baed6"),
    marker=dict(size=10, color="#08519c")
))

fig.update_layout(
    title="Arrest Rate Comparison: Public vs Private Spaces",
    xaxis=dict(
        tickvals=[0, 1],
        ticktext=["Public", "Private"],
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(title="Arrest Rate (%)", range=[0, 100]),
    paper_bgcolor="#0e1117",
    plot_bgcolor="#0e1117",
    font_color="#e0e0e0",
    margin={"r":20,"t":50,"l":20,"b":20}
)

# Accessible annotation
private_rate = summary[summary["space_type"] == "Private"]["percent"].iloc[0]
fig.add_annotation(
    x=1,
    y=private_rate,
    text=f"<b>Private Arrest Rate</b><br>{private_rate:.1f}%",
    showarrow=True,
    arrowhead=2,
    ax=40,
    ay=0,
    font=dict(color="#f4d35e", size=12),
    bgcolor="rgba(20,20,20,0.7)",
    bordercolor="#f4d35e",
    borderwidth=1
)

st.plotly_chart(fig, use_container_width=True)
