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


## GRAPH 1 - Line chart -------------------------------------

# Select variables to display in dropdown menu
var_options = df.columns.tolist()
var_select = st.selectbox("Select variable to plot", var_options)
line_chart_df = df.reset_index()
chart_sort = [x for x in line_chart_df["Game"]]

# Calculate the cumulative average
cumulative_average = alt.Chart(line_chart_df).transform_window(
    rolling_mean=f"mean({var_select})",
    frame=[None,0]
).mark_line(color="orange").encode(
    alt.X('Game', title='Game', sort=chart_sort),
    alt.Y('rolling_mean:Q', title=f"{var_select} (cumulative average)", axis=alt.Axis(titleFontSize=12)),
    color=alt.value('orange'),
    #legend=alt.Legend(title='Average', labelFontSize=12, titleFontSize=12)
)

# Create line chart for selected variable
chart = alt.Chart(line_chart_df).mark_line().encode(
    x=alt.X("Game", title="Game", sort=chart_sort),
    y=alt.Y(var_select, scale=alt.Scale(domain=(line_chart_df[var_select].min(), line_chart_df[var_select].max()))),
).properties(width=600, height=400)

# Circles
circles = alt.Chart(line_chart_df).mark_circle().encode(
    x=alt.X("Game", title="Game", sort=chart_sort),
    y=alt.Y(var_select, scale=alt.Scale(domain=(line_chart_df[var_select].min(), line_chart_df[var_select].max()))),
).properties(width=600, height=400)

# Display line chart
st.altair_chart(chart + cumulative_average + circles)

## GRAPH 2 - Averages -------------------------------------

# Create bar chart of mean for all variables
mean_df = df.mean().reset_index(name="mean").rename(columns={"index": "variable"})
mean_chart = alt.Chart(mean_df).mark_bar().encode(
    x="variable",
    y="mean"
).properties(width=600, height=400)

# Display bar chart
st.altair_chart(mean_chart)

