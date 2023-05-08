import streamlit as st
## TO BE REMOVED: test
import camelot

#from st_aggrid import GridOptionsBuilder, AgGrid

st.write("""
# GSQSA Basket
*An analysis of the GSQSA Basketball Team 2022/2023 stats*
""")

st.sidebar.success("Select between Players or Team Stats above")

# GSQSA logo
github_data_path = "https://raw.githubusercontent.com/Giovalentini/gsqsa_basket/main/"
st.image(github_data_path+"gsqsa_logo.png", width=300)
