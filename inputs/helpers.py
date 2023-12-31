import pandas as pd
import json
import time
import os

from inputs.pull_gsheet import pull_ids
from pipeline.formatting import add_team

location = os.getcwd()

stage_path = location + r'/inputs/raceinfo/stages.csv'
athlete_path = location + r'/inputs/raceinfo/athletes.csv'
prologue_path = location + r'/inputs/raceinfo/prologue.csv'
pts_path = location + r'/inputs/raceinfo/points.csv'
handicaps_path = location + r'/inputs/raceinfo/handicaps.csv'
orange_pass_path = location + r'/inputs/raceinfo/orange_pass.csv'


def load_csv(file_path):
    try:
        dataframe = pd.read_csv(file_path)
        return dataframe
    except Exception as e:
        print(f"Error loading DataFrame: {e}")
        return None


def save_csv(dataframe, file_path):
    try:
        dataframe.to_csv(file_path, index=False)  # index=False to exclude the DataFrame index from the CSV
    except Exception as e:
        print(f"Error saving DataFrame: {e}")


def save_json(data, file_path):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file)
    except Exception as e:
        print(f"Error saving data: {e}")


def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None
    

def get_ids(gsheets):
    current_time = time.localtime()

    if gsheets == "Yes":
        stages, ath_ids, prologue, pts, handicaps, orange_pass = pull_ids("Stage_ids", "Athlete_ids", "Prologue", "Points", "Handicaps", "Orange_passes")

        prologue = add_team(prologue, ath_ids)
        
        save_csv(stages, stage_path)
        save_csv(ath_ids, athlete_path)
        save_csv(prologue, prologue_path)
        save_csv(pts, pts_path)
        save_csv(handicaps, handicaps_path)
        save_csv(orange_pass, orange_pass_path)

    else:
        stages = load_csv(stage_path)
        ath_ids = load_csv(athlete_path)
        prologue = load_csv(prologue_path)
        pts = load_csv(pts_path)
        handicaps = load_csv(handicaps_path)
        orange_pass = load_csv(orange_pass_path)

    handicaps[['True Weight', 'Race Weight']] = handicaps[['True Weight', 'Race Weight']].apply(pd.to_numeric, errors='coerce')

    return stages, ath_ids, prologue, pts, handicaps, orange_pass