import pandas as pd
import numpy as np
import os
import time
import sys

sys.path.append('/Users/achie188/Library/CloudStorage/GitHub/Personal/SW_eracing')

from inputs.pull_gsheet import pull_gsheet, push_gsheet
from inputs.pull_zwift import pull_zwift
from inputs.helpers import load_csv, save_csv
from pipeline.formatting import format_results, format_mmss, add_team

location = os.getcwd()

prologue_path = location + r'/inputs/raceinfo/prologue.csv'
pts_path = location + r'/inputs/raceinfo/points.csv'
athlete_path = location + r'/inputs/raceinfo/athletes.csv'
live_race_path = location + r'/inputs/raceinfo/'

pts = load_csv(pts_path)
prologue = load_csv(prologue_path)
ath_ids = load_csv(athlete_path)

current_time = time.localtime()

def process_dataframe(df, stage_name):
    if df is not None and not df.empty:
        df['Stage'] = stage_name
        return df
    

def replace_zeros(column):
    # Convert the column to numeric, handling both integers and strings
    column_numeric = pd.to_numeric(column, errors='coerce')
    
    # Replace 0 with sN for numeric values
    column_numeric = np.where(column_numeric == 0, np.nan, column_numeric)

    # Apply replacement value based on conditions
    fastest_time = np.nanmin(column_numeric)
    slowest_time = np.nanmax(column_numeric)
    team_time = np.nanmax(column_numeric)
    replacement_value = max(fastest_time + 300, slowest_time + 30)
    
    return np.where(np.isnan(column_numeric), replacement_value, column_numeric)


def orange(orange_df, new_stage):

    pts = load_csv(pts_path)
    prologue = load_csv(prologue_path)

    if orange_df is None:
        orange_df = prologue
    
    combined_df = pd.merge(orange_df, new_stage, on='Name', suffixes=('_orange', '_new_stage'), how='outer')

    #fill non finishing times
    # Calculate the fastest and slowest times for new stage
    columns_to_replace = ['Time_secs_orange', 'Time_secs_new_stage']
    combined_df[columns_to_replace] = combined_df[columns_to_replace].apply(replace_zeros, axis=0)

    combined_df['Total'] = combined_df['Time_secs_orange'] + combined_df['Time_secs_new_stage']

    combined_df = combined_df.sort_values(by='Total')
    combined_df.reset_index(drop=True, inplace=True)
    combined_df['#'] = combined_df.index + 1

    columns_to_keep = ["#", "Orange"]
    pts.drop(pts.columns.difference(columns_to_keep), axis=1, inplace=True)

    df = pd.merge(combined_df, pts, left_on='#', right_on='#', how='inner')

    orange_df = df[['Name', 'Total']]
    orange_df = orange_df.rename(columns={'Total' : 'Time_secs'})

    df = df.rename(columns={'Orange_y': 'Orange'})

    if 'Orange_x' in df.columns:
        df.drop(columns=['Orange_x'], inplace=True)
        df = df.rename(columns={'Orange_y': 'Orange'})
    df = df[['Name', 'Orange']]
    
    return df, orange_df


def calc_points(stage, stage_num, pts):

    pts = load_csv(pts_path)

    columns_to_keep = ["#", stage_num]
    pts.drop(pts.columns.difference(columns_to_keep), axis=1, inplace=True)
    pts = pts.rename(columns={stage_num : 'Points'})

    df = pd.merge(stage, pts, left_on='#', right_on='#', how='inner')

    return df


def get_stage(stage, stage_num, ath_ids, gsheet="No", orange_df=prologue):
    if stage == '' or pd.isna(stage):
        return None, orange_df
    else:
        df = pull_zwift(stage)

        if df.empty:
            return None, orange_df
        else:
            
            path = live_race_path + stage_num + '.csv'

            if gsheet == 'Yes':
                f_df = format_results(df, ath_ids)
                f_df_o, orange_df = orange(orange_df, f_df)
                f_df_pts = calc_points(f_df, stage_num, pts)
                f_df_o_pts = pd.merge(f_df_pts, f_df_o, left_on='Name', right_on='Name', how='inner')
                push_gsheet(f_df_o_pts, stage_num)
                stage_res = pull_gsheet(stage_num)

                columns_to_process = ['KOM', 'Int. S', 'DS/DC', 'Report', 'MAR']

                for column in columns_to_process:
                    stage_res[column] = pd.to_numeric(stage_res[column], errors='coerce')
                    stage_res[column].fillna(0, inplace=True)
                    stage_res[column] = stage_res[column].astype('int64')

                path = live_race_path + stage_num + '.csv'
                save_csv(stage_res, path )
            else:
                stage_res = load_csv(path)
                f_df_o, orange_df = orange(orange_df, stage_res)

        
    return stage_res, orange_df


def calc_overall_pts(pro, s1, s2, s3, ttt, s4, s5):

    ath_ids = load_csv(athlete_path)

    all_dataframes = [
        process_dataframe(pro, 'Prologue'),
        process_dataframe(s1, 'Stage 1'),
        process_dataframe(s2, 'Stage 2'),
        process_dataframe(s3, 'Stage 3'),
        process_dataframe(ttt, 'TTT'),
        process_dataframe(s4, 'Stage 4'),
        process_dataframe(s5, 'Stage 5'),
    ]

    # Concatenate the DataFrames
    all_dataframes = [pro, s1, s2, s3, ttt, s4, s5]
    combined_df = pd.concat(all_dataframes, ignore_index=True)
    combined_df['Total'] = pd.to_numeric(combined_df['Total'], errors='coerce')
    combined_df['KOM'] = pd.to_numeric(combined_df['KOM'], errors='coerce')
    combined_df['Int. S'] = pd.to_numeric(combined_df['Int. S'], errors='coerce')
    combined_df['Total'].fillna(0, inplace=True)




    # calc individual pts
    ind_df = combined_df.pivot_table(index='Name', columns='Stage', values='Total', aggfunc='sum', fill_value=0)
    ind_df = ind_df.reset_index()
    numeric_columns = ind_df.select_dtypes(include=[np.number]).columns
    ind_df['Total'] = ind_df[numeric_columns].sum(axis=1)

    ind_df = ind_df.loc[ind_df['Total'] != 0]

    ind_df = ind_df.sort_values(by='Total', ascending=False)
    ind_df.reset_index(inplace=True)
    ind_df['#'] = ind_df.index + 1

    other_columns = [col for col in ind_df.columns if col != '#']
    column_order = ['#'] + other_columns[0:]
    ind_df = ind_df.reindex(columns=column_order)
    ind_df.drop(columns=['index'], inplace=True)

    ind_df = ind_df.round(0)
    ind_df = add_team(ind_df, ath_ids)

    column_order = list(ind_df.columns)
    column_order.remove('TTT')  
    column_order.insert(7, 'TTT')  
    ind_df = ind_df[column_order]

    # calc team pts
    team_df = combined_df.pivot_table(index='Team', columns='Stage', values='Total', aggfunc='sum', fill_value=0)
    team_df.reset_index(inplace=True)
    numeric_columns = team_df.select_dtypes(include=[np.number]).columns

    # add ttt
    # ttt_teams = ttt_teams[['Team', 'Total']]
    # team_df = pd.merge(team_df, ttt_teams[['Team', 'Total']], on='Team', how='left')
    # team_df['TTT'] += team_df['Total']  
    # team_df = team_df.drop(columns='Total')

    team_df['Total'] = team_df[numeric_columns].sum(axis=1)

    team_df = team_df.loc[team_df['Total'] != 0]

    team_df = team_df.sort_values(by='Total', ascending=False)
    team_df.reset_index(inplace=True)
    team_df['#'] = team_df.index + 1

    team_df.loc[team_df['Team'] == 'Tesla', 'Team'] = 'Tesla Thames Water'
    team_df.loc[team_df['Team'] == 'ABS', 'Team'] = 'Amazon Beaconsfield Services'
    team_df.loc[team_df['Team'] == 'AZT', 'Team'] = 'AstraZenaca Trailfinders'
    team_df.loc[team_df['Team'] == 'Lego', 'Team'] = 'Lego Boots'

    other_columns = [col for col in team_df.columns if col != '#']
    column_order = ['#'] + other_columns[0:]
    team_df = team_df.reindex(columns=column_order)
    team_df.drop(columns=['index'], inplace=True)  

    team_df = team_df.round(0)

    column_order = list(team_df.columns)
    column_order.remove('TTT')  
    column_order.insert(6, 'TTT')  
    team_df = team_df[column_order]

    # calc KOM pts
    kom_df = combined_df.pivot_table(index='Name', columns='Stage', values='KOM', aggfunc='sum', fill_value=0)
    kom_df.reset_index(inplace=True)
    numeric_columns = kom_df.select_dtypes(include=[np.number]).columns
    kom_df['Total'] = kom_df[numeric_columns].sum(axis=1)

    kom_df = kom_df.loc[kom_df['Total'] != 0]

    kom_df = kom_df.sort_values(by='Total', ascending=False)
    kom_df.reset_index(inplace=True)
    kom_df['#'] = kom_df.index + 1

    other_columns = [col for col in kom_df.columns if col != '#']
    column_order = ['#'] + other_columns[0:]
    kom_df = kom_df.reindex(columns=column_order)
    kom_df.drop(columns=['index', 'Prologue'], inplace=True)  

    kom_df = kom_df.round(0)

    column_order = list(kom_df.columns)
    column_order.remove('TTT')  
    column_order.insert(5, 'TTT')  
    kom_df = kom_df[column_order]

    # calc sprinter pts
    sprinter_df = combined_df.pivot_table(index='Name', columns='Stage', values='Int. S', aggfunc='sum', fill_value=0)
    sprinter_df.reset_index(inplace=True)
    numeric_columns = sprinter_df.select_dtypes(include=[np.number]).columns
    sprinter_df['Total'] = sprinter_df[numeric_columns].sum(axis=1)

    sprinter_df = sprinter_df.loc[sprinter_df['Total'] != 0]

    sprinter_df = sprinter_df.sort_values(by='Total', ascending=False)
    sprinter_df.reset_index(inplace=True)
    sprinter_df['#'] = sprinter_df.index + 1

    other_columns = [col for col in sprinter_df.columns if col != '#']
    column_order = ['#'] + other_columns[0:]
    sprinter_df = sprinter_df.reindex(columns=column_order)
    sprinter_df.drop(columns=['index', 'Prologue'], inplace=True)  

    sprinter_df = sprinter_df.round(0)

    column_order = list(sprinter_df.columns)
    column_order.remove('TTT')  
    column_order.insert(5, 'TTT')  
    sprinter_df = sprinter_df[column_order]

    return ind_df, team_df, kom_df, sprinter_df


def calc_overall_orange(pro, s1, s2, s3, ttt, s4, s5, columns_to_replace, orange_pass):

    all_dataframes = [
        process_dataframe(pro, 'Prologue'),
        process_dataframe(s1, 'Stage 1'),
        process_dataframe(s2, 'Stage 2'),
        process_dataframe(s3, 'Stage 3'),
        process_dataframe(ttt, 'TTT'),
        process_dataframe(s4, 'Stage 4'),
        process_dataframe(s5, 'Stage 5'),
    ]

    # Concatenate the DataFramesome    all_dataframes = [pro, s1, s2a, s2b, s3, s4, s5, s6]
    combined_df = pd.concat(all_dataframes, ignore_index=True)
    combined_df['Time_secs'] = pd.to_numeric(combined_df['Time_secs'], errors='coerce')

    # calc times
    orange_df = combined_df.pivot_table(index='Name', columns='Stage', values='Time_secs', aggfunc='sum', fill_value=0)
    orange_df = orange_df.reset_index()

    orange_df[columns_to_replace] = orange_df[columns_to_replace].apply(replace_zeros, axis=0)

    # merge with orange pass
    orange_pass.columns = [col.replace('_', ' ') for col in orange_pass.columns]
    columns_to_keep = ['Name'] + columns_to_replace
    orange_pass = orange_pass[columns_to_keep]

    orange_pass[columns_to_replace] = orange_pass[columns_to_replace].apply(pd.to_numeric, errors='coerce')
    orange_pass[columns_to_replace] = orange_pass[columns_to_replace].fillna(1000000)

    orange_df = pd.merge(orange_df, orange_pass, on='Name', how='outer', suffixes=('_df1', '_df2'))

    for column in columns_to_replace:
        orange_df[column] = orange_df[[column + '_df1', column + '_df2']].min(axis=1)

    columns_to_drop = [column + '_df1' for column in columns_to_replace] + [column + '_df2' for column in columns_to_replace]
    orange_df.drop(columns=columns_to_drop, inplace=True)

    numeric_columns = orange_df.select_dtypes(include=[np.number]).columns

    orange_df['Time_secs'] = orange_df[numeric_columns].sum(axis=1)

    orange_df = orange_df[~(orange_df[columns_to_replace] == 0).any(axis=1)]

    orange_df['Total'] = orange_df[columns_to_replace].sum(axis=1)

    orange_df = orange_df.loc[orange_df['Time_secs'] != 0]

    orange_df = orange_df.sort_values(by='Total', ascending=True)

    fastest_time = orange_df['Total'].min()
    orange_df['Diff'] = orange_df['Total'] - fastest_time

    orange_df[columns_to_replace] = orange_df[columns_to_replace].applymap(format_mmss)
    orange_df['Total'] = orange_df['Total'].apply(format_mmss)
    orange_df['Diff'] = orange_df['Diff'].apply(format_mmss)

    orange_df.reset_index(inplace=True)
    orange_df['#'] = orange_df.index + 1

    other_columns = [col for col in orange_df.columns if col != '#']
    column_order = ['#'] + other_columns[0:]
    orange_df = orange_df.reindex(columns=column_order)
    orange_df.drop(columns=['index', 'Time_secs'], inplace=True)

    orange_df = add_team(orange_df, ath_ids)

    return orange_df

def handicaps_format(df):
    df.drop(columns=['Zwift_id'], inplace=True)
    df['#'] = df.index + 1
    df = df[['#', 'Name', 'True Weight', 'Race Weight', 'Bike']]
    df[['True Weight', 'Race Weight']] = df[['True Weight', 'Race Weight']].round(1)
    df.replace({None: '', 0: '', 'None': '', np.nan: ''}, inplace=True)
    df = add_team(df, ath_ids)

    df[['True Weight', 'Race Weight']] = df[['True Weight', 'Race Weight']].apply(pd.to_numeric, errors='coerce')

    return df