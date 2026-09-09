# (DSC527) Privacy Intrusion Data Story – Part 3  
Author: Tracey Johnson  
Date: 09‑09‑2026  
Python version: 3.13

## Overview
This project develops a data story centered on privacy intrusions in public spaces, using a filtered snapshot of the Chicago Crime Data dataset. Rather than focusing on violent crime, the analysis isolates non‑violent offenses that reflect moments where individuals may feel watched, unsafe, or vulnerable—such as criminal trespassing, stalking, intimidation, public indecency, and other privacy‑related violations.

The purpose of this data story is to explore how these seemingly minor public‑space intrusions connect to broader social patterns of fear and psychological safety. As recent research suggests, even small privacy disruptions can evoke discomfort, heighten vigilance, and serve as precursors to more serious interpersonal harms. This project examines whether such incidents show meaningful patterns across time, location, and behavior.

The data story is presented through an interactive Streamlit application and a supporting Jupyter Notebook used during development.

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
