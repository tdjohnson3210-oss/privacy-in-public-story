# (DSC527) Privacy Intrusion Data Story – Part 3  
Author: Tracey Johnson  
Date: 09‑09‑2026  
Python version: 3.13

## Overview
This project builds a data story about privacy intrusions in public spaces using a filtered snapshot of the Chicago Crime Data dataset. Instead of focusing on violent crime, the analysis highlights non‑violent offenses that involve boundary‑crossing behavior — the kinds of incidents that can make someone feel watched, bothered, or unsettled in everyday public life. These include offenses such as criminal trespassing, stalking, intimidation, public indecency, and other privacy‑related violations.

The goal is to understand when and where these smaller public‑space intrusions tend to occur. By examining how they cluster across different environments and times of day, the project reveals patterns in how privacy gets disrupted in shared spaces — from residential blocks to commercial areas to outdoor public settings.

The data story is presented through an interactive Streamlit application, supported by a development‑stage Jupyter Notebook used for feature engineering and exploration.

## Streamlit Application
Interactive Streamlit application:  
**https://privacy-in-public-story-isgwkmv4keh2hjqrfyczps.streamlit.app/**

Purpose: The app provides an interactive walkthrough of privacy‑related crime patterns, allowing users to explore arrest rates, geographic spread, time‑of‑day trends, and layered behavioral rhythms.  

The app also includes an **embedded Streamlit survey**, replacing the earlier Microsoft Forms version.

## Data Source
This project uses publicly available crime data from the **Chicago Data Portal**, which provides detailed records of all reported crimes from 2001 to the present. The full dataset contains millions of observations and is used here to determine **high‑level proportions** of privacy‑related case types within Chicago’s broader crime landscape.

A filtered snapshot (**chicago_crime_snapshot_08242026.parquet**, downloaded 08‑24‑2026) was created to isolate incidents most relevant to privacy intrusion. The snapshot is stored on **Dropbox**, and the Streamlit application loads it directly from the hosted link.

All analysis, visualizations, and engineered features in this project are based on this filtered subset.

## Installation
To run the project locally:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt 
