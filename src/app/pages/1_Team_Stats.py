# page 2 content

import altair as alt
import pandas as pd
import streamlit as st

# read data
#data_path = "C:/Users/valen/OneDrive/Documenti/GSQSA/gsqsa_basket/output/"
github_data_path = "https://raw.githubusercontent.com/Giovalentini/gsqsa_basket/main/output/"
df = pd.read_csv(github_data_path+'GSQSA_team_stats.csv')

# build app
st.write("""
GSQSA Team Stats
""")

cols_to_round = ['FG%','3P%','2P%','FT%']

st.dataframe(df.style.format(subset=cols_to_round, formatter="{:.2f}"))