import pandas as pd

def clean_stats(df: pd.DataFrame)->pd.DataFrame:
    '''
    Return cleaned stats
    '''
    df = df[-df.NUMERO.isin([98,99])]

    # shots
    df['PTS'] = df['FTM'] + 2*df['2PM'] + 3*df['3PM']
    df['RT'] = df['RO'] + df['RD']
    df['FT%'] = df['FTM'] / df['FTA']
      
    return df