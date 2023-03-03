# page 2 content
import altair as alt
import pandas as pd
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

# read data
github_data_path = "https://raw.githubusercontent.com/Giovalentini/gsqsa_basket/main/output/"
df = pd.read_csv(github_data_path+'GSQSA_team_stats.csv')
df = df.set_index('Game')

# build app
st.write("""
GSQSA Team Stats
""",unsafe_allow_html=True)


## TABLE 1 - Each Game -------------------------------------
cols_to_round = ['FG%','3P%','2P%','FT%','OPP_FG%','OPP_3P%','OPP_2P%','OPP_FT%']
cols_to_int = ["OPP_FTM", "OPP_FTA", "OPP_2PM", "OPP_2PA", "OPP_3PM", "OPP_3PA", "OPP_FGM", "OPP_FGA", "OPP_PTS"]

styled_df = (
    df.style
    .format(subset=cols_to_round, formatter="{:.2f}")
    .format(subset=cols_to_int, formatter="{:.0f}")
)
st.dataframe(styled_df)


## PART 2 - Line chart and averages -------------------------------------

# Select variables to display in dropdown menu
var_options = df.columns.tolist()

# Display dropdown menu
var_select = st.selectbox("Select variable to plot", var_options)

# Create line chart for selected variable
#line_chart_df = df.reset_index()
line_chart_df = df.reset_index()
chart = alt.Chart(line_chart_df).mark_line().encode(
    x="Game",
    y=alt.Y(var_select, scale=alt.Scale(domain=(line_chart_df[var_select].min(), line_chart_df[var_select].max()))),
).properties(width=600, height=400)

# Display line chart
st.altair_chart(chart)

# Create bar chart of mean for all variables
mean_df = df.mean().reset_index(name="mean").rename(columns={"index": "variable"})
mean_chart = alt.Chart(mean_df).mark_bar().encode(
    x="variable",
    y="mean"
).properties(width=600, height=400)

# Display bar chart
st.altair_chart(mean_chart)

