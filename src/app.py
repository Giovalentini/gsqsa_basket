import altair as alt
import pandas as pd
import streamlit as st

# read data
data_path = "C:/Users/valen/OneDrive/Documenti/GSQSA/gsqsa_basket/output/"
df = pd.read_csv(data_path+'tabs.csv')

# build app
st.write("""
# GSQSA Basket
*An analysis of the GSQSA Basketball Team 2022/2023 stats*
""")

player_option = st.selectbox('Choose the player', df.PLAYER.unique())

line_chart = alt.Chart(df[df.PLAYER==player_option]).mark_line(interpolate='basis').encode(
    alt.X([1,2,3,4,5,6], title='Year'),
    alt.Y('PTS', title='Amount in liters')
    #color='category:N'
).properties(
    title='Points per Games'
)

st.altair_chart(line_chart)
#st.line_chart(
#    df[df.PLAYER==player_option].PTS
#)