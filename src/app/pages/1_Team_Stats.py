# page 2 content

import pandas as pd
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

# read data
github_data_path = "https://raw.githubusercontent.com/Giovalentini/gsqsa_basket/main/output/"
df = pd.read_csv(github_data_path+'GSQSA_team_stats.csv')

# build app
st.write("""
GSQSA Team Stats
""",unsafe_allow_html=True)

cols_to_round = ['FG%','3P%','2P%','FT%']
st.dataframe(df.style.format(subset=cols_to_round, formatter="{:.2f}"))
#AgGrid(df.style.format(subset=cols_to_round, formatter="{:.2f}"))

#gb = GridOptionsBuilder.from_dataframe(df)
#gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
#gb.configure_side_bar() #Add a sidebar
#gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
#gridOptions = gb.build()
#
#grid_response = AgGrid(
#    df,
#    gridOptions=gridOptions,
#    data_return_mode='AS_INPUT', 
#    update_mode='MODEL_CHANGED', 
#    fit_columns_on_grid_load=False,
#    theme='alpine', #Add theme color to the table
#    enable_enterprise_modules=True,
#    height=350, 
#    width='100%',
#    reload_data=True
#)
#
#df = grid_response['data']
#selected = grid_response['selected_rows'] 
#df = pd.DataFrame(selected) #Pass the selected rows to a new dataframe df