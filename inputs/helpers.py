import pandas as pd
import json

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