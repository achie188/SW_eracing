import pandas as pd

from inputs.pull_zwift import pull_ttt
from pipeline.formatting import format_mmss


def get_ttt():
    zwift_ids = [3977847, 3977849, 3977853, 3977842]
    teams = ['Tesla', 'Amazon', 'AZT', 'Lego']

    dfs = []

    for i, team in zip(zwift_ids, teams):
        df = pull_ttt(i)
        df['Team'] = team
        dfs.append(df)

    live = pd.concat(dfs, ignore_index=True)
    if not live.empty:
        live = live.sort_values(by='Time', ascending=True).reset_index(drop=True)
        live['Pos'] = live.index + 1

        # furthest = live['Distance'].nlargest(4).iloc[-1]
        # live['Diff'] = furthest - live['Distance']

        
        live = live[['Pos', 'Team', 'Name', 'W/Kg', 'Time']]

        # Filter the DataFrame to keep only the 4th fastest time from each team
        team_summary = live.groupby('Team').apply(lambda x: x.nsmallest(4, 'Time')).reset_index(drop=True)
        team_summary = team_summary.groupby('Team').nth(3).reset_index()
        team_summary = team_summary.sort_values(by='Time', ascending=True).reset_index(drop=True)
        team_summary['Pos'] = team_summary.index + 1
        team_summary = team_summary[['Pos', 'Team', 'Name', 'W/Kg', 'Time']]

        live['Time'] = live['Time'].apply(format_mmss)
        team_summary['Time'] = team_summary['Time'].apply(format_mmss)

    return live, team_summary