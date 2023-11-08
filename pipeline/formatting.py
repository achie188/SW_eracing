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

def format(df):

    #rename columns
    df = df.rename(columns={'position': '#'})
    df = df.rename(columns={'heartRateInBpm': 'HR'})
    df = df.rename(columns={'powerOutputInWatts': 'Watts'})
    df = df.rename(columns={'powerInWattsPerKg': 'Watts/Kg'}).round(2)
    df = df.rename(columns={'liveTimeGapToLeaderInSeconds': 'Gap'})
    df = df.rename(columns={'completionTimeInSeconds': 'Finish Time'})
    df = df.rename(columns={'distanceInMeters': 'Distance'}).round(1)
    df = df.rename(columns={'speedInKmHours': 'Speed'}).round(1)
    df = df.rename(columns={'powerupUsed': 'PowerUps Used'})

    df['Finish Time'] = df['Finish Time'].apply(format_mmss)
    
    return df
