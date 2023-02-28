import numpy as np
import pandas as pd
import sys

pd.options.mode.chained_assignment = None
sys.path.insert(0, 'C:\\Users\\valen\\OneDrive\\Documenti\\GSQSA\\gsqsa_basket\\src')

from utils import *

if __name__ == "__main__":

    data_path = "C:/Users/valen/OneDrive/Documenti/GSQSA/gsqsa_basket/input_data/"
    output_path = "C:/Users/valen/OneDrive/Documenti/GSQSA/gsqsa_basket/output/"
    
    # read all sheets into dict
    df_dict = pd.read_excel(data_path+"tabellini.xlsx", sheet_name=None)

    # validity checks
    games_list, opp_FTM_list, opp_FTA_list, opp_2PM_list, opp_2PA_list, opp_3PM_list, opp_3PA_list = ([] for i in range(7))
    for tab in df_dict.values():

        # checks
        tab_check = tab[~tab.NUMERO.isin([98,99])]
        assert ((tab_check.FTM > tab_check.FTA).sum()==0),"Free Throws Made can't be greater than Free Throws Attempted"
        assert ((tab_check['2PM'] > tab_check['2PA']).sum()==0),"2 Points Made can't be greater than 2 Points Attempted"
        assert ((tab_check['3PM'] > tab_check['3PA']).sum()==0),"3 Points Made can't be greater than 3 Points Attempted"
        assert ((tab_check.FF > 5).sum()==0), "A player can't make more than 5 fouls"

        #get opponent team name (if 99 GSQSA played home, else played away)
        if tab.iloc[-1].NUMERO == 99:
            games_list.append("vs "+tab.iloc[-1].PLAYER)
        else:
            games_list.append("@ "+tab.iloc[-1].PLAYER)

        # opponent points
        opp_FTM_list.append(tab.iloc[-1].FTM)
        opp_FTA_list.append(tab.iloc[-1].FTA)
        opp_2PM_list.append(tab.iloc[-1]['2PM'])
        opp_2PA_list.append(tab.iloc[-1]['2PA'])
        opp_3PM_list.append(tab.iloc[-1]['3PM'])
        opp_3PA_list.append(tab.iloc[-1]['3PA'])

    print("Games played:", games_list)
        
    # read players bio
    players_bio = pd.read_excel(data_path+"players_bio.xlsx")
    players_bio['Age'] = players_bio.BORN.apply(lambda x: age(x))
    
    # clean df
    df_dict_cleaned = {k:clean_stats(v) for k, v in df_dict.items()}

    # add game number and calculate teams stats
    for i, k in enumerate(df_dict_cleaned.keys()):
        
        # game number
        df_dict_cleaned[k]['game'] = i+1

        # team stats
        tmp = pd.DataFrame(df_dict_cleaned[k][team_cols].sum()).T
        tmp.rename(columns={0:i})
        if i == 0:
            team_stats = tmp
        else:
            team_stats = pd.concat([team_stats,tmp])
        team_stats = team_stats.reset_index().drop('index',axis=1).astype(int)

    team_stats = clean_team_stats(team_stats)
    team_stats['Game'] = games_list

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
        '+/-':'mean',
        'MIN':'mean'}).round(2)#.rename(columns={'size':'G'})
    tab_mean.Age = tab_mean.Age.astype('Int64')
    tab_mean.POS = tab_mean.POS.astype('Int64')
    tab_mean.HEIGHT = tab_mean.HEIGHT.astype('Int64')

    tab_sum = tabs.groupby('PLAYER', as_index=False).agg({
        'Age':'max',
        'POS':'max',
        'HEIGHT':'max',
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
        '+/-':'sum',
        'MIN':'sum'
    })

    tab_sum['FG%'] = round(tab_sum['FGM'] / tab_sum['FGA'] * 100, 2)
    tab_sum['FT%'] = round(tab_sum['FTM'] / tab_sum['FTA'] * 100, 2)
    tab_sum['2P%'] = round(tab_sum['2PM'] / tab_sum['2PA'] * 100, 2)
    tab_sum['3P%'] = round(tab_sum['3PM'] / tab_sum['3PA'] * 100, 2)

    # games per player
    games_per_player = tabs.groupby('PLAYER', as_index=False).size().rename(columns={'size':'G'})

    tab_mean = pd.merge(
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

    tab_sum = pd.merge(
        tab_sum,
        games_per_player,
        on='PLAYER',
        how='left'
    )

    tab_mean.MIN = tab_mean.MIN.apply(lambda x: fix_mins(x))
    tab_sum.MIN = tab_sum.MIN.apply(lambda x: fix_mins(x))

    # prepare output
    cols_order = ['PLAYER','Age','POS','HEIGHT','G',
                  'PTS','FGM','FGA','FG%','3PM','3PA','3P%','2PM','2PA','2P%','FTM','FTA','FT%',
                  'RO','RD','RT','AST','PR','PP','ST','FF','FS','+/-','MIN']

    team_cols_order = ['Game','PTS','FGM','FGA','FG%','3PM','3PA','3P%','2PM','2PA','2P%','FTM','FTA','FT%',
                       'RO','RD','RT','AST','PR','PP','ST','FF','FS']

    tab_sum = tab_sum[cols_order]
    tab_mean = tab_mean[cols_order]
    team_stats = team_stats[team_cols_order]

    # averages of team
    team_averages = team_stats.drop(["Game", "FG%", "3P%", "2P%", "FT%"], axis=1).mean().round(2)
    team_shooting = team_stats[['FGM','FGA','3PM','3PA','2PM','2PA','FTM','FTA']].sum()
    team_shooting = clean_team_stats(team_shooting)
    team_shooting = team_shooting[["FG%", "3P%", "2P%", "FT%"]]
    team_averages = pd.concat([team_averages, team_shooting])
    print(team_averages)
    
    # send to csv
    #tabs.to_csv(output_path+"tabs.csv", index=False)
    tab_mean.sort_values(by='PTS', ascending=False).to_csv(output_path+"Averages_per_Player.csv", index=False)
    tab_sum.sort_values(by='PTS', ascending=False).to_csv(output_path+"Totals_per_Player.csv", index=False)
    team_stats.to_csv(output_path+"GSQSA_team_stats.csv", index=False)
    team_averages.to_csv(output_path+"GSQSA_Averages.csv", index=True, header=False)