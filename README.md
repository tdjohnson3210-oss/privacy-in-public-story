# (DSC527) Privacy Intrusion Data Story – Part 1
Author: Tracey Johnson/
Date: 08-26-2026/
Python version 3.13

## Overview
This project develops a data story centered on privacy intrusions in public spaces, using a filtered snapshot of the Chicago Crime Data dataset. Rather than focusing on violent crime, the analysis isolates non‑violent offenses that reflect moments where individuals may feel watched, unsafe, or vulnerable—such as criminal trespassing, stalking, intimidation, public indecency, and other privacy‑related violations.

The purpose of this data story is to explore how these seemingly minor public‑space intrusions connect to broader sociological patterns of fear and psychological safety. As recent research suggests, even small privacy disruptions can evoke discomfort, heighten vigilance, and serve as precursors to more serious interpersonal harms. This project examines whether such incidents show meaningful patterns across time, location, and behavior that help explain when fear may escalate.

The data story is outlined through an interactive Jupyter Notebook and HTML export, combining narrative explanation with Plotly visualizations and engineered features.

## Installation
To run this notebook, ensure you have Python 3.13 installed along with the following libraries:
`import pandas as pd`
`import numpy as np`
`import matplotlib.pyplot as plt`
`import seaborn as sns`
`import pyarrow as pa`
`import pyarrow.parquet as pq`
`import plotly.express as px`

## Usage
1. Open the Jupyter Notebook containing the data storyboarding draft.
2. Interact with Plotly charts within the notebook or HTML export.
3. Test linked Microsoft Forms survey for user interaction.

## Project Structure
- Data Story Preparation.ipynb – Notebook for preparing the data story.
- Storyboarding.html – Main file containing the narrative, visualizations, and analysis.
- README.md – Project documentation and instructions.
- Crimes_-_2001_to_Present_20250603.csv – Raw dataset containing all recorded crimes in Chicago from 2001 to the present.
- chicago_crime_snapshot_08242026.parquet – Filtered dataset snapshot used for analysis.

## Synthetic Dataset Features        
0   id                135067 non-null  Int64         
1   case_number       135067 non-null  category      
2   date              135067 non-null  datetime64[ns]
3   block             135067 non-null  category      
4   iucr              135067 non-null  category      
5   primary_type      135067 non-null  category      
6   privacy_location  135067 non-null  category      
7   arrest            135067 non-null  bool          
8   domestic          135067 non-null  bool          
9   beat              135067 non-null  Int64         
10  district          135067 non-null  Int64         
11  ward              135063 non-null  Int64         
12  community_area    135047 non-null  Int64         
13  fbi_code          135067 non-null  category      
14  x_coordinate      134619 non-null  float64       
15  y_coordinate      134619 non-null  float64       
16  year              135067 non-null  Int64         
17  updated_on        135067 non-null  datetime64[ns]
18  latitude          134619 non-null  float64       
19  longitude         134619 non-null  float64       
20  location          134619 non-null  category      
21  time_of_day       135067 non-null  category      
22  privacy_category  135067 non-null  category      

## Engineered Features
- `privacy_category` – Groups offenses into high-level privacy‑intrusion types.
- `privacy_location` – Simplifies location descriptions into meaningful public‑space categories.
- `time_of_day` – Categorizes incidents into morning, afternoon, evening, and overnight.

## License
This project uses publicly available open data from the Chicago Data Portal, released under the City of Chicago Open Data License. The filtered dataset snapshot used here is for academic purposes only.