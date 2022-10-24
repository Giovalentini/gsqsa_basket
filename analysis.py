import numpy as np
import pandas as pd

data_path = "C:/Users/valen/OneDrive/Documenti/GSQSA/tabellini/"
output_path = "C:/Users/valen/OneDrive/Documenti/GSQSA/gsqsa_basket/output/"

# read number of sheets
tabellini = pd.ExcelFile(data_path+"tabellini.xlsx")
n_partite = len(tabellini.sheet_names)
print(f'number of matches: {n_partite}')

# read all sheets into dict
df_dict = pd.read_excel(data_path+"tabellini.xlsx", sheet_name=None)

# clean df
df_dict_cleaned = {k:clean_stats(v) for k, v in df_dict.items()}

# concat tabs
tabs = pd.concat(list(df_dict_cleaned.values()))

# aggregates
tab_agg = tabs.groupby('NOME', as_index=False).agg({'PTS':'mean','RT':'mean','AST':'mean'}).round(2)

# send to csv
tab_agg.sort_values(by='PTS', ascending=False).to_csv(output_path+"tab_agg.csv", index=False)