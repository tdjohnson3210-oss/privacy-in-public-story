# (DSC527) Privacy Intrusion Data Story – Part 2  
Author: Tracey Johnson  
Date: 09‑02‑2026  
Python version 3.13

## Overview
This project develops a data story centered on privacy intrusions in public spaces, using a filtered snapshot of the Chicago Crime Data dataset. Rather than focusing on violent crime, the analysis isolates non‑violent offenses that reflect moments where individuals may feel watched, unsafe, or vulnerable—such as criminal trespassing, stalking, intimidation, public indecency, and other privacy‑related violations.

The purpose of this data story is to explore how these seemingly minor public‑space intrusions connect to broader social patterns of fear and psychological safety. As recent research suggests, even small privacy disruptions can evoke discomfort, heighten vigilance, and serve as precursors to more serious interpersonal harms. This project examines whether such incidents show meaningful patterns across time, location, and behavior that help explain when fear may escalate.

The data story is presented through an interactive Jupyter Notebook, HTML export, and a Streamlit application.

## Streamlit Application
Interactive Streamlit application:  
**https://privacy-in-public-story-isgwkmv4keh2hjqrfyczps.streamlit.app/**

Purpose: The app provides an interactive walkthrough of privacy‑related crime patterns, allowing users to explore arrest rates, geographic spread, time‑of‑day trends, and layered behavioral rhythms.

## Data Source
This project uses publicly available crime data from the **Chicago Data Portal**, which provides detailed records of all reported crimes from 2001 to the present. The full dataset contains millions of observations and is used here to determine **high‑level proportions** of privacy‑related case types within Chicago’s broader crime landscape.

From this larger dataset, a **chicago_crime_snapshot_08242026.parquet** (downloaded on 08‑24‑2026) was created to isolate incidents most relevant to privacy intrusion. This snapshot includes only non‑violent offenses associated with boundary violations, discomfort, or unwanted presence. All analysis, visualizations, and engineered features in this project are based on this filtered subset.


## Installation
To run this notebook, ensure you have Python 3.13 installed along with the following libraries:  
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import pyarrow as pa
import pyarrow.parquet as pq

## Usage
1. Open the Jupyter Notebook containing the data storyboarding draft.  
2. Interact with Plotly charts within the notebook or HTML export.  
3. Test the linked Microsoft Forms survey for user interaction.  
4. Launch the Streamlit application for the full interactive experience.

## Project Structure
- **Data Story Preparation.ipynb** – Notebook for preparing the data story.  
- **Storyboarding.html** – Main file containing the narrative, visualizations, and analysis.  
- **README.md** – Project documentation and instructions.  
- **chicago_crimes** – https://mygcuedu6961-my.sharepoint.com/:u:/g/personal/tjohnson779_my_gcu_edu/IQBQvjBEAclmSqIpWDB8OQ95AetZPkkYrmIzzm0rEtp3Q0E?e=IwKOGw
- **chicago_crime_snapshot_08242026.parquet** – https://mygcuedu6961-my.sharepoint.com/:u:/g/personal/tjohnson779_my_gcu_edu/IQCth27bkUiKTL_u9yv-p5AIAR81_4SFGqJsceC7kFq7cpM?e=Rb8RhQ
- ** Technical Report Draft.docx** 

## Dataset Features
0. id  
1. case_number  
2. date  
3. block  
4. iucr  
5. primary_type  
6. privacy_location  
7. arrest  
8. domestic  
9. beat  
10. district  
11. ward  
12. community_area  
13. fbi_code  
14. x_coordinate  
15. y_coordinate  
16. year  
17. updated_on  
18. latitude  
19. longitude  
20. location  
21. time_of_day  
22. privacy_category  

## Engineered Features
- 'privacy_category' – Groups offenses into high‑level privacy‑intrusion types.  
- 'privacy_location' – Simplifies location descriptions into meaningful public‑space categories.  
- 'time_of_day' – Categorizes incidents into morning, afternoon, evening, and overnight.

## Methods Summary
- Extracted necessary features (hour, time‑of‑day categories)  
- Grouped incidents by privacy category, location type, and arrest outcome  
- Calculated arrest rates and proportions across case types  
- Generated layered visualizations to compare behavioral rhythms  
- Mapped geographic spread using latitude/longitude scatter plots  

## Limitations
Privacy intrusions are inferred from non‑violent crime categories and may not capture all forms of interpersonal boundary violations.

## License
This project uses publicly available open data from the Chicago Data Portal, released under the City of Chicago Open Data License. The filtered dataset snapshot used here is for academic purposes only.
