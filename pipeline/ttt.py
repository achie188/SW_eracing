import pandas as pd
import os

from inputs.pull_zwift import pull_ttt
from inputs.pull_gsheet import pull_gsheet, push_gsheet
from pipeline.calcs import orange
from pipeline.formatting import format_mmss, format_results
from inputs.helpers import load_csv, save_csv


location = os.getcwd()
live_race_path = location + r'/inputs/raceinfo/'


def get_ttt(ath_ids):
    zwift_ids = [3977847, 3977849, 3977853, 3977842]
    teams = ['Tesla', 'Amazon', 'AZT', 'Lego']

    dfs = []

    for i, team in zip(zwift_ids, teams):
        df = pull_ttt(i)
        dfs.append(df)

    ttt_ind = pd.concat(dfs, ignore_index=True)

    ttt_ind['playerId'] = pd.to_numeric(ttt_ind['playerId'], errors='coerce')
    ath_ids['Zwift_Id'] = pd.to_numeric(ath_ids['Zwift_Id'], errors='coerce')
                                                
    df = pd.merge(ttt_ind, ath_ids, left_on='playerId', right_on='Zwift_Id', how='inner')

    #rename columns
    df = df.rename(columns={'position': '#'})
    df = df.rename(columns={'heartRateInBpm': 'HR'})
    df = df.rename(columns={'powerOutputInWatts': 'Power'})
    df = df.rename(columns={'powerInWattsPerKg': 'W/Kg'}).round(2)
    df = df.rename(columns={'completionTimeInSeconds': 'Time_secs'})

    df['Time_nice'] = df['Time_secs'].apply(format_mmss)
    df['#'] = df.index + 1

    fastest_time = df['Time_secs'].min()
    df['Gap'] = df['Time_secs'] - fastest_time

    df = df.rename(columns={'Ed_Name': 'Name'})

    # Filter the DataFrame to keep only the 4th fastest time from each team
    team_summary = df.groupby('Team').apply(lambda x: x.nsmallest(4, 'Time_secs')).reset_index(drop=True)
    team_summary = team_summary.groupby('Team').nth(3).reset_index()
    team_summary = team_summary.sort_values(by='Time_secs', ascending=True).reset_index(drop=True)
    team_summary['Pos'] = team_summary.index + 1
    
    
    df['Time_nice'] = df['Time_secs'].apply(format_mmss)
    team_summary['Time_nice'] = team_summary['Time_secs'].apply(format_mmss)

    df = df[['#', 'Name', 'Team', 'Time_nice', 'Time_secs', 'Gap', 'Power', 'W/Kg', 'HR']]
    team_summary = team_summary.rename(columns={'Time_nice': 'Time'})
    team_summary = team_summary[['Pos', 'Team', 'Name', 'Time']]
    

    return df, team_summary

def sort_ttt(orange_df, ath_ids, gsheets):
    
    ind, team = get_ttt(ath_ids)

    ind_path = live_race_path  + 'ttt_ind.csv'
    team_path = live_race_path  + 'ttt_team.csv'

    if gsheets == "Yes":
        ind_o, orange_df = orange(orange_df, ind)
        ind_o_pts = pd.merge(ind, ind_o, left_on='Name', right_on='Name', how='inner')

        ind_o_pts = ind_o_pts.sort_values(by='Time_secs', ascending=True).reset_index(drop=True)
        ind_o_pts['Time_nice'] = ind_o_pts['Time_secs'].apply(format_mmss)
        
        ind_o_pts['Pos'] = ind_o_pts.index + 1
        ind_o_pts = ind_o_pts[['Pos', 'Team', 'Name', 'Time_nice', 'Time_secs', 'Power', 'W/Kg', 'HR', 'Orange']]

        push_gsheet(ind_o_pts, "TTT")
        push_gsheet(team, "TTT_Teams")

        ind_ttt = pull_gsheet("TTT")
        team_ttt = pull_gsheet("TTT_Teams")

        save_csv(ind_ttt, ind_path)
        save_csv(team_ttt, team_path)
    
    else:
        ind_ttt = load_csv(ind_path)
        team_ttt = load_csv(team_path)


    return ind_ttt, team_ttt, orange_df