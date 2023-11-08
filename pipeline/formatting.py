import pandas as pd
import numpy as np



#Format mm:ss
def format_mmss(seconds):
    if np.isnan(seconds):
        return '0:00'
    elif seconds < 600:  # Less than 10 minutes
        return '{:01d}:{:02d}'.format(int(seconds // 60), int(seconds % 60))  # M:SS format
    else:
        return '{:02d}:{:02d}'.format(int(seconds // 60), int(seconds % 60))  # MM:SS format

def format_results(res, pts, ath_ids):

    res['playerId'] = pd.to_numeric(res['playerId'], errors='coerce')
    ath_ids['zwiZwift_Idft_id'] = pd.to_numeric(ath_ids['Zwift_Id'], errors='coerce')
                                                
    df = pd.merge(res, ath_ids, left_on='playerId', right_on='Zwift_Id', how='inner')
    df = pd.merge(df, pts, left_on='Ed_Name', right_on='Name', how='inner')

    #rename columns
    df = df.rename(columns={'position': '#'})
    df = df.rename(columns={'heartRateInBpm': 'HR'})
    df = df.rename(columns={'powerOutputInWatts': 'Watts'})
    df = df.rename(columns={'powerInWattsPerKg': 'Watts/Kg'}).round(2)
    df = df.rename(columns={'liveTimeGapToLeaderInSeconds': 'Gap'})
    df = df.rename(columns={'completionTimeInSeconds': 'Time'})
    df = df.rename(columns={'distanceInMeters': 'Distance'}).round(1)
    df = df.rename(columns={'speedInKmHours': 'Speed'}).round(1)
    df = df.rename(columns={'powerupUsed': 'PowerUps Used'})

    df['Time'] = df['Time'].apply(format_mmss)


    df = df[['#', 'Ed_Name', 'Time', 'Gap', 'HR', 'Watts', 'Watts/Kg', 'Fin pts', 'KoM #', 'KOM', 'Int. S', 'Des Sp/Cl', 'Reports', 'MAR', 'Par. Pts', 'Total pts', 'Orange pts']]

    df = df.rename(columns={'Ed_Name': 'Name'})

    return df
