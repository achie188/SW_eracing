import pandas as pd

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

    return df
