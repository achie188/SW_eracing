import pandas as pd
import numpy as np



#Format mm:ss
def format_mmss(seconds):

    if seconds is None or np.isnan(seconds):
        return '0:00'
    elif seconds < 600:  # Less than 10 minutes
        return '{:01d}:{:02d}'.format(int(seconds // 60), int(seconds % 60))  # M:SS format
    else:
        return '{:02d}:{:02d}'.format(int(seconds // 60), int(seconds % 60))  # MM:SS format


def format_results(res, ath_ids):

    res['playerId'] = pd.to_numeric(res['playerId'], errors='coerce')
    ath_ids['Zwift_Id'] = pd.to_numeric(ath_ids['Zwift_Id'], errors='coerce')
                                                
    df = pd.merge(res, ath_ids, left_on='playerId', right_on='Zwift_Id', how='inner')

    #rename columns
    df = df.rename(columns={'position': '#'})
    df = df.rename(columns={'heartRateInBpm': 'HR'})
    df = df.rename(columns={'powerOutputInWatts': 'Watts'})
    df = df.rename(columns={'powerInWattsPerKg': 'W/Kg'}).round(2)
    df = df.rename(columns={'liveTimeGapToLeaderInSeconds': 'Gap'})
    df = df.rename(columns={'completionTimeInSeconds': 'Time_secs'})
    df = df.rename(columns={'distanceInMeters': 'Distance'}).round(1)
    df = df.rename(columns={'speedInKmHours': 'Speed'}).round(1)
    df = df.rename(columns={'powerupUsed': 'PowerUps Used'})

    df['Time_nice'] = df['Time_secs'].apply(format_mmss)

    df = df[['#', 'Ed_Name', 'Team', 'Time_nice', 'Time_secs', 'Gap', 'HR', 'Watts', 'W/Kg']]

    df = df.rename(columns={'Ed_Name': 'Name'})

    return df


def add_team(df, ath_ids):

    ath_ids = ath_ids[['Ed_Name', 'Team']]

    df = pd.merge(df, ath_ids, left_on='Name', right_on='Ed_Name', how='inner')
    other_columns = [col for col in df.columns if col != 'Team']

    column_order = other_columns[:2] + ['Team'] + other_columns[2:]
    df = df.reindex(columns=column_order)

    df.drop(columns=['Ed_Name'], inplace=True)

    return df


def convert_to_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def get_zwift_ids(stage_values, df):
    zwift_ids = []
    for stage_value in stage_values:
        try:
            zwift_id_value = df.loc[df['Stage'] == stage_value, 'Zwift_id'].iloc[0]
            zwift_ids.append(zwift_id_value)
        except IndexError:
            # Handle the case where no matching row is found
            zwift_ids.append(None)

    zwift_ids = [convert_to_int(value) for value in zwift_ids]

    return zwift_ids


def final_format(df):
    if df is None:

        return df
    
    else:
        df.drop(columns=['Time_secs', 'Stage'], inplace=True)
        df = df.rename(columns={'Time_nice': 'Time'})

        # columns_to_convert = ['KOM', 'Int. S', 'DS/DC', 'Report', 'MAR']

        # if all(col in df.columns for col in columns_to_convert):
        #     df[columns_to_convert] = df[columns_to_convert].apply(pd.to_numeric).round(0)
        #     df.replace({np.nan: ''}, inplace=True)
        return df
    

def highlight_team(team):
    colors = {
            'Lego Boots': 'lightcoral', 
            'Amazon Beaconsfield Services': 'lightblue', 
            'AstraZenaca Trailfinders': 'lightgreen',
            'Tesla Thames Water': 'lightgreen',
            }
    return [f'background-color: {colors.get(t, "")}' for t in team]


def teams_slice(df, team, handicaps, columns_to_replace):
    filtered_df = df[df['Team'] == team].copy()

    filtered_df = pd.merge(filtered_df, handicaps, left_on='Name', right_on='Name', how='inner')
    filtered_df.drop(columns=['#_y', 'Team_y'], inplace=True)
    filtered_df = filtered_df.rename(columns={'#_x': '#', 'Team_x': 'Team'})

    filtered_df[['True Weight', 'Race Weight']] = filtered_df[['True Weight', 'Race Weight']].round(1)
    
    add_columns1 = ['#', 'Name', 'True Weight', 'Race Weight', 'Bike']

    add_columns2 = ['Total']

    filtered_df = filtered_df[add_columns1 + columns_to_replace + add_columns2].copy()

    # sum_columns = ['#', 'Weight']
    # columns_to_sum = sum_columns + columns_to_replace
    # total_row = filtered_df[columns_to_sum].sum(axis=0)

    # filtered_df = filtered_df.append(total_row, ignore_index=True)

    return filtered_df


