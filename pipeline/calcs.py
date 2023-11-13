import pandas as pd
import numpy as np

from inputs.pull_gsheet import pull_gsheet, push_gsheet
from inputs.pull_zwift import pull_zwift
from pipeline.formatting import format_results, format_mmss

pts = pull_gsheet("Points")
prologue = pull_gsheet("Prologue")


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
    replacement_value = max(fastest_time + 300, slowest_time + 30)
    
    return np.where(np.isnan(column_numeric), replacement_value, column_numeric)


def orange(orange_df, new_stage):

    pts = pull_gsheet("Points")

    if orange_df is None:
        orange_df = prologue
    
    combined_df = pd.merge(orange_df, new_stage, on='Name', suffixes=('_orange', '_new_stage'))

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
    orange_df = orange_df.rename(columns={'Total' : 'Time'})

    df = df[['Name', 'Orange']]

    return df, orange_df


def calc_points(stage, stage_num):
    
    pts = pull_gsheet("Points")

    columns_to_keep = ["#", stage_num]
    pts.drop(pts.columns.difference(columns_to_keep), axis=1, inplace=True)
    pts = pts.rename(columns={stage_num : 'Points'})

    df = pd.merge(stage, pts, left_on='#', right_on='#', how='inner')

    return df


def get_stage(stage, stage_num, ath_ids, orange_df=prologue):
    if stage == '':
        return None, orange_df
    else:
        df = pull_zwift(stage)
        f_df = format_results(df, ath_ids)
        f_df_o, orange_df = orange(orange_df, f_df)
        f_df_pts = calc_points(f_df, stage_num)

        f_df_o_pts = pd.merge(f_df_pts, f_df_o, left_on='Name', right_on='Name', how='inner')
        # f_df_o_pts.drop(columns=['#'], inplace=True   )

        push_gsheet(f_df_o_pts, stage_num)
        stage_res = pull_gsheet(stage_num)

    return stage_res, orange_df


def calc_overall_pts(pro, s1, s2a, s2b, s3, s4, s5, s6):
    all_dataframes = [
        process_dataframe(pro, 'Prologue'),
        process_dataframe(s1, 'Stage 1'),
        process_dataframe(s2a, 'Stage 2a'),
        process_dataframe(s2b, 'Stage 2b'),
        process_dataframe(s3, 'Stage 3'),
        process_dataframe(s4, 'Stage 4'),
        process_dataframe(s5, 'Stage 5'),
        process_dataframe(s6, 'Stage 6'),
    ]

    # Concatenate the DataFrames
    all_dataframes = [pro, s1, s2a, s2b, s3, s4, s5, s6]
    combined_df = pd.concat(all_dataframes, ignore_index=True)

    # calc individual pts
    ind_df = combined_df.pivot_table(index='Name', columns='Stage', values='Total', aggfunc='sum', fill_value=0)
    ind_df = ind_df.reset_index()
    ind_df['Total'] = ind_df.sum(axis=1)
    ind_df = ind_df.sort_values(by='Total', ascending=False)

    ind_df = ind_df.loc[ind_df['Total'] != 0]

    ind_df.reset_index(inplace=True)
    ind_df['#'] = ind_df.index + 1

    other_columns = [col for col in ind_df.columns if col != '#']
    column_order = ['#'] + other_columns[0:]
    ind_df = ind_df.reindex(columns=column_order)
    ind_df.drop(columns=['index'], inplace=True)

    # calc team pts
    team_df = combined_df.pivot_table(index='Team', columns='Stage', values='Total', aggfunc='sum', fill_value=0)
    team_df.reset_index(inplace=True)
    team_df['Total'] = team_df.sum(axis=1)
    team_df = team_df.sort_values(by='Total', ascending=False)

    team_df = team_df.loc[team_df['Total'] != 0]

    team_df.reset_index(inplace=True)
    team_df['#'] = team_df.index + 1

    other_columns = [col for col in team_df.columns if col != '#']
    column_order = ['#'] + other_columns[0:]
    team_df = team_df.reindex(columns=column_order)
    team_df.drop(columns=['index'], inplace=True)  

    return ind_df, team_df


def calc_overall_orange(pro, s1, s2a, s2b, s3, s4, s5, s6, columns_to_replace):

    all_dataframes = [
        process_dataframe(pro, 'Prologue'),
        process_dataframe(s1, 'Stage 1'),
        process_dataframe(s2a, 'Stage 2a'),
        process_dataframe(s2b, 'Stage 2b'),
        process_dataframe(s3, 'Stage 3'),
        process_dataframe(s4, 'Stage 4'),
        process_dataframe(s5, 'Stage 5'),
        process_dataframe(s6, 'Stage 6'),
    ]

    # Concatenate the DataFramesome    all_dataframes = [pro, s1, s2a, s2b, s3, s4, s5, s6]
    combined_df = pd.concat(all_dataframes, ignore_index=True)
    combined_df['Time_secs'] = pd.to_numeric(combined_df['Time_secs'], errors='coerce')

    # calc times
    orange_df = combined_df.pivot_table(index='Name', columns='Stage', values='Time_secs', aggfunc='sum', fill_value=0)
    orange_df = orange_df.reset_index()
    numeric_columns = orange_df.select_dtypes(include=[np.number]).columns
    orange_df['Time_secs'] = orange_df[numeric_columns].sum(axis=1)

    orange_df[columns_to_replace] = orange_df[columns_to_replace].apply(replace_zeros, axis=0)

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



    return orange_df