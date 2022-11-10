import numpy as np
import pandas as pd
import sys

sys.path.insert(0, 'C:\\Users\\valen\\OneDrive\\Documenti\\GSQSA\\gsqsa_basket\\src')

from utils import *

if __name__ == "__main__":

    data_path = "C:/Users/valen/OneDrive/Documenti/GSQSA/gsqsa_basket/input_data/"
    output_path = "C:/Users/valen/OneDrive/Documenti/GSQSA/gsqsa_basket/output/"
    
    # read all sheets into dict
    df_dict = pd.read_excel(data_path+"tabellini.xlsx", sheet_name=None)

    # read players bio
    players_bio = pd.read_excel(data_path+"players_bio.xlsx")
    players_bio['Age'] = players_bio.BORN.apply(lambda x: age(x))
    
    # clean df
    df_dict_cleaned = {k:clean_stats(v) for k, v in df_dict.items()}
    
    # concat tabs
    tabs = pd.concat(list(df_dict_cleaned.values()))

    # merge with players bio
    tabs = pd.merge(
        tabs,
        players_bio.drop(['NUMBER','BORN'],axis=1),
        on='PLAYER',
        how='left'
    )

    # aggregates
    tab_mean = tabs.groupby('PLAYER', as_index=False).agg({
        'Age':'max',
        'POS':'max',
        'HEIGHT':'max',
        'PTS':'mean',
        'FGM':'mean',
        'FGA':'mean',
        '3PM':'mean', 
        '3PA':'mean',
        '2PM':'mean',
        '2PA':'mean',
        'FTM':'mean',
        'FTA':'mean',       
        'RO':'mean',
        'RD':'mean',
        'RT':'mean',
        'AST':'mean',
        'PP':'mean',
        'PR':'mean',
        'ST':'mean',
        'FF':'mean',
        'FS':'mean',
        '+/-':'mean'}).round(2)#.rename(columns={'size':'G'})

    tab_sum = tabs.groupby('PLAYER', as_index=False).agg({
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

    # games per player
    games_per_player = tabs.groupby('PLAYER', as_index=False).size().rename(columns={'size':'G'})

    tab_agg = pd.merge(
        pd.merge(
            tab_mean,
            tab_sum[['PLAYER','FG%','FT%','2P%','3P%']],
            on='PLAYER',
            how='left'            
        ),
        games_per_player,
        on='PLAYER',
        how='left'
    )

    cols_order = ['PLAYER','PTS','FGM','FGA','FG%','3PM','3PA','3P%','2PM','2PA','2P%','FTM','FTA','FT%',
                  'RO','RD','RT','AST','PR','PP','ST','FF','FS','+/-']

    tab_sum = tab_sum[cols_order]
    tab_agg = tab_agg[cols_order]
    
    # send to csv
    tabs.to_csv(output_path+"tabs.csv", index=False)
    tab_agg.sort_values(by='PTS', ascending=False).to_csv(output_path+"tab_agg.csv", index=False)
    tab_sum.sort_values(by='PTS', ascending=False).to_csv(output_path+"tab_sum.csv", index=False)