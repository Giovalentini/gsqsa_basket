import pandas as pd
from datetime import date

#def input_data_checks(df):
#    """Validity checks on input data"""
#    if df.FTM>df.FTA:
#        raise ValueError("Free Throws Made can't be higher than Free Throws Attempted")
#    if df['2PM']>df['2PA']:
#        raise ValueError("Two Pointers Made can't be higher than Twp Pointers Attempted")

def clean_stats(df: pd.DataFrame)->pd.DataFrame:
    '''
    Return cleaned stats
    '''
    df = df[-df.NUMERO.isin([98,99])]

    # mins
    df.MIN = df.MIN.apply(lambda x: pd.Timedelta("00:"+x))

    # shots
    df['PTS'] = df['FTM'] + 2*df['2PM'] + 3*df['3PM']
    df['FGM'] = df['2PM'] + df['3PM']
    df['FGA'] = df['2PA'] + df['3PA']
    df['FG%'] = df['FGM'] / df['FGA'] * 100
    df['FT%'] = df['FTM'] / df['FTA'] * 100
    df['2P%'] = df['2PM'] / df['2PA'] * 100
    df['3P%'] = df['3PM'] / df['3PA'] * 100

    # rebounds
    df['RT'] = df['RO'] + df['RD']
      
    return df

def opponent_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate opponents field goals and points"""
    df["OPP_FGM"] = df["OPP_2PM"] + df["OPP_3PM"]
    df["OPP_FGA"] = df["OPP_2PA"] + df["OPP_3PA"]
    df["OPP_PTS"] = df["OPP_FTM"] + 2*df["OPP_2PM"] + 3*df["OPP_3PM"]
    return df

def clean_team_stats(df: pd.DataFrame, opp=False)->pd.DataFrame:
    '''
    Return team's cleaned stats
    '''
    if opp==False:
        df['FG%'] = round(df['FGM'] / df['FGA'] * 100,2)
        df['FT%'] = round(df['FTM'] / df['FTA'] * 100,2)
        df['2P%'] = round(df['2PM'] / df['2PA'] * 100,2)
        df['3P%'] = round(df['3PM'] / df['3PA'] * 100,2)

    # opponent team's stats
    else:
        df['OPP_FG%'] = round(df['OPP_FGM'] / df['OPP_FGA'] * 100,2)
        df['OPP_FT%'] = round(df['OPP_FTM'] / df['OPP_FTA'] * 100,2)
        df['OPP_2P%'] = round(df['OPP_2PM'] / df['OPP_2PA'] * 100,2)
        df['OPP_3P%'] = round(df['OPP_3PM'] / df['OPP_3PA'] * 100,2)

    return df

def age(birthdate):
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

def fix_mins(mins_played):
    return str(mins_played.seconds//60)+':'+str(mins_played.seconds%60)

team_cols = ['PTS','FGM','FGA','3PM','3PA','2PM','2PA','FTM','FTA',
             'RO','RD','RT','AST','PR','PP','ST','FF','FS']