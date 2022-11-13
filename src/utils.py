import pandas as pd

from datetime import date

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

def age(birthdate):
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

def fix_mins(mins_played):
    return str(mins_played.seconds//60)+':'+str(mins_played.seconds%60)