import numpy as np
import pandas as pd
import sys

sys.path.insert(0, 'C:\\Users\\valen\\OneDrive\\Documenti\\GSQSA\\gsqsa_basket\\src')

from utils import clean_stats

if __name__ == "__main__":

    data_path = "C:/Users/valen/OneDrive/Documenti/GSQSA/gsqsa_basket/input_data/"
    output_path = "C:/Users/valen/OneDrive/Documenti/GSQSA/gsqsa_basket/output/"
    
    # read all sheets into dict
    df_dict = pd.read_excel(data_path+"tabellini.xlsx", sheet_name=None)
    
    # clean df
    df_dict_cleaned = {k:clean_stats(v) for k, v in df_dict.items()}
    
    # concat tabs
    tabs = pd.concat(list(df_dict_cleaned.values()))
    
    # aggregates
    tab_mean = tabs.groupby('NOME', as_index=False).agg({
        'PTS':'mean',
        'RO':'mean',
        'RD':'mean',
        'RT':'mean',
        'AST':'mean',
        'PP':'mean',
        'PR':'mean',
        'ST':'mean',
        'FF':'mean',
        'FS':'mean',
        '+/-':'mean'}).round(2)

    tab_sum = tabs.groupby('NOME', as_index=False).agg({
        'PTS':'sum',
        'FTM':'sum',
        'FTA':'sum',
        'FGM':'sum',
        'FGA':'sum',
        '2PM':'sum',
        '2PA':'sum',
        '3PM':'sum',
        '3PA':'sum',
        'RO':'sum',
        'RD':'sum',
        'RT':'sum',
        'AST':'sum',
        'PP':'sum',
        'PR':'sum',
        'ST':'sum',
        'FF':'sum',
        'FS':'sum',
        '+/-':'sum'})

    tab_sum['FG%'] = round(tab_sum['FGM'] / tab_sum['FGA'] * 100, 2)
    tab_sum['FT%'] = round(tab_sum['FTM'] / tab_sum['FTA'] * 100, 2)
    tab_sum['2P%'] = round(tab_sum['2PM'] / tab_sum['2PA'] * 100, 2)
    tab_sum['3P%'] = round(tab_sum['3PM'] / tab_sum['3PA'] * 100, 2)

    tab_agg = pd.merge(
        tab_mean,
        tab_sum[['NOME','FG%','FT%','2P%','3P%']],
        on='NOME',
        how='left'
    )
    
    # send to csv
    tab_agg.sort_values(by='PTS', ascending=False).to_csv(output_path+"tab_agg.csv", index=False)
    tab_sum.sort_values(by='PTS', ascending=False).to_csv(output_path+"tab_sum.csv", index=False)