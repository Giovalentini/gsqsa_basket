import altair as alt
import pandas as pd
import streamlit as st

# read data
#data_path = "C:/Users/valen/OneDrive/Documenti/GSQSA/gsqsa_basket/output/"
github_data_path = "https://raw.githubusercontent.com/Giovalentini/gsqsa_basket/main/output/"
df = pd.read_csv(github_data_path+'tabs.csv')
tab_agg = pd.read_csv(github_data_path+"Averages_per_Player.csv")

# build app
st.write("""
# GSQSA Basket
*An analysis of the GSQSA Basketball Team 2022/2023 stats*
""")

cols_to_round = ['PTS','FGM','FGA','FG%','3PM','3PA','3P%','2PM','2PA','2P%','FTM','FTA','FT%',
                'RO','RD','RT','AST','PR','PP','ST','FF','FS','+/-']
#st.table(tab_agg.style.format(subset=cols_to_round, formatter="{:.2f}"))
st.dataframe(tab_agg.style.format(subset=cols_to_round, formatter="{:.2f}"))


player_option = st.selectbox('Choose the player', df.PLAYER.unique())
stat_option = st.selectbox('Choose the stat', ('PTS','RT','AST'))

line_chart = alt.Chart(df[df.PLAYER==player_option]).mark_line().encode(
    alt.X('game', title='Game'),
    alt.Y(stat_option, title=stat_option)
    #color='PLAYER:N'
).properties(
    title=f"{player_option}'s {stat_option} over Games"
)

st.altair_chart(line_chart)
#st.line_chart(
#    df[df.PLAYER==player_option].PTS
#)