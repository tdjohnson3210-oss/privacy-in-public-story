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
if st.button("Next"):
    st.switch_page("pages/1_map.py")

# Intro title
st.markdown("<h1 style='text-align: center;'>Can You See My Personal Bubble? The Boundaries of Privacy in Public</h1>", unsafe_allow_html=True)
st.write("")

# Intro paragraphs  html
st.markdown("""
<div style="max-width: 750px; margin-left: auto; margin-right: auto;">
Public spaces are shared, but people still carry a basic expectation of personal privacy when moving through them. 
Even small moments of feeling watched or unsafe can create discomfort and reduce psychological safety. 
This data story explores when and where those moments tend to occur, and how they might build into more serious concerns.
</div>
""", unsafe_allow_html=True)

st.write("")

st.markdown("""
<div style="max-width: 750px; margin-left: auto; margin-right: auto;">
<strong>Before we begin, please take the time to answer a brief four‑question survey in order to understand your expectations of privacy in public spaces.</strong>
</div>
""", unsafe_allow_html=True)

st.write("")

# Participant survey
with st.form("public_privacy_survey"):

    st.markdown("""
    <div style="max-width: 750px; margin-left: auto; margin-right: auto;">
    Please answer the following questions:
    </div>
    """, unsafe_allow_html=True)

    # Q1
    q1 = st.radio(
        "How often do you leave your home and spend time in public spaces?",
        ["Daily", "Weekly", "Monthly", "Never"]
    )

    # Q2
    q2 = st.radio(
        "Have you ever experienced a public interaction that made you feel uncomfortable, watched, or unsafe?",
        ["Yes, frequently", "Yes, occasionally", "Rarely", "Never"]
    )

    # Q3
    q3 = st.radio(
        "Where do you believe privacy intrusions are most likely to occur?",
        ["Residential", "Commercial", "Outdoor", "Industrial", "Transportation"]
    )

    # Q4
    q4 = st.radio(
        "When do you think privacy intrusions are most common?",
        ["Morning", "Afternoon", "Evening"]
    )

    submitted = st.form_submit_button("Submit Survey")

# Store responses for session
if submitted:
    st.session_state['q1'] = q1
    st.session_state['q2'] = q2
    st.session_state['q3'] = q3
    st.session_state['q4'] = q4
    st.success("Your responses have been recorded for this session.")


# Test in terminal
# streamlit run overview.py