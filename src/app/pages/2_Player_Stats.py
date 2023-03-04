import altair as alt
import os
import pandas as pd
import streamlit as st
import sys

# add the parent directory to sys.path
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
#from utils import fix_mins

#dataFrameSerialization = "legacy"

# read data
github_data_path = "https://raw.githubusercontent.com/Giovalentini/gsqsa_basket/main/output/"

# all tabs
df = pd.read_pickle(github_data_path+'tabs.pkl')
#df.MIN = df.MIN.apply(lambda x: fix_mins(x))

# player averages
tab_agg = pd.read_csv(github_data_path+"Averages_per_Player.csv")
tab_agg = tab_agg.set_index('PLAYER')

# build app
st.write("""
GSQSA Player Stats
""")

# Table 1 --------------------------
cols_to_round = ['PTS','FGM','FGA','FG%','3PM','3PA','3P%','2PM','2PA','2P%','FTM','FTA','FT%',
                'RO','RD','RT','AST','PR','PP','ST','FF','FS','+/-']
cols_to_int = ["Age", "POS", "HEIGHT"]
styled_df = (
    tab_agg.style
    .format(subset=cols_to_round, formatter="{:.2f}")
    .format(subset=cols_to_int, formatter="{:.0f}")
)
st.dataframe(styled_df)


# Graph 1 -----------------
player_option = st.selectbox('Choose the player', df.PLAYER.unique())
stat_option = st.selectbox('Choose the stat', ('PTS','RT','AST'))

# Calculate the cumulative average
cumulative_average = alt.Chart(df[df.PLAYER==player_option]).transform_window(
    rolling_mean=f"mean({stat_option})",
    frame=[None,0]
).mark_line(color="orange").encode(
    alt.X('game', title='Game'),
    alt.Y('rolling_mean:Q', title=f"{stat_option} (cumulative average)", axis=alt.Axis(titleFontSize=12)),
    color=alt.value('orange'),
    #legend=alt.Legend(title='Average', labelFontSize=12, titleFontSize=12)
)

line_chart = alt.Chart(df[df.PLAYER==player_option]).mark_line().encode(
    alt.X('game', title='Game'),
    alt.Y(stat_option, title=stat_option)
    #color='PLAYER:N'
).properties(
    title=f"{player_option}'s {stat_option} over Games"
)

# Combine the two charts using the '+' operator
combined_chart = (line_chart + cumulative_average).resolve_legend()

# Display the combined chart
st.altair_chart(combined_chart)

## GRAPH 2 - Pie chart -----------------------------

# Calculate the sum of the value for each player
sum_by_player = df.groupby('PLAYER')[stat_option].sum().reset_index()

# Create a pie chart
pie_chart = alt.Chart(sum_by_player).mark_arc().encode(
    theta=alt.Theta(field=stat_option, type="quantitative"),
    color=alt.Color(field="PLAYER", type="nominal"),
).properties(
    title=f'Players Impact on {stat_option}'
).add_selection(
    alt.selection_multi(fields=['PLAYER'], bind='legend')
)

pie_chart

