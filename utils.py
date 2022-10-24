import pandas as pd

def clean_stats(df: pd.DataFrame)->pd.DataFrame:
    '''
    Return cleaned stats
    '''
    
    df = df[-df.NUMERO.isin([98,99])]

    # shots
    df['PTS'] = df['FTM'] + 2*df['2PM'] + 3*df['3PM']
    df['RT'] = df['RO'] + df['RD']
    #df['FTM'] = df['1P'].str.split("/").str[0]
    #df['FTA'] = df['1P'].str.split("/").str[1]
    #df['2PM'] = df['2P'].str.split("/").str[0]
    #df['2PA'] = df['2P'].str.split("/").str[1]
    #df['3PM'] = df['3P'].str.split("/").str[0]
    #df['3PA'] = df['3P'].str.split("/").str[1]
#
    #df = df.fillna(0)
#
    #df.drop(['1P','2P','3P'], axis=1, inplace=True)
      
    return df