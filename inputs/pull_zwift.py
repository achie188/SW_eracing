import pandas as pd
import requests
import streamlit as st

AUTH_TOKEN = st.secrets["zwift_credentials"]["AUTH_TOKEN"]



def pull_zwift(event_id):
    if event_id is None:
        return None
    

    url = "https://us-or-rly101.zwift.com/relay/race/events/" + str(event_id) + "/placement?from=1&to=50&chipTime=true"

    payload = {}
    headers = {
        'Authorization': f'Bearer {AUTH_TOKEN}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    data = response.json()

    # Extract 'placement' details
    placement_data = data.get('placement', [])

    race_data = pd.DataFrame(placement_data)

    if not(race_data).empty:
        race_data.drop(columns=['jerseyHash', 'location', 'countryCodeAlpha2Code', 'crossingStartingLineGap', 'rideOnsCounter', 'arrivalAtInSeconds', 'groupNumber'], inplace=True)

    return race_data


def pull_ttt(event_id):
    if event_id is None:
        return None
    

    url = "https://us-or-rly101.zwift.com/relay/race/events/" + str(event_id) + "/placement?from=1&to=50&chipTime=true"

    payload = {}
    headers = {
        'Authorization': f'Bearer {AUTH_TOKEN}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    data = response.json()

    # Extract 'placement' details
    placement_data = data.get('placement', [])

    race_data = pd.DataFrame(placement_data)

    if not(race_data).empty:
        race_data.drop(columns=['playerId', 'heartRateInBpm', 'powerOutputInWatts', 'liveTimeGapToLeaderInSeconds', 'speedInKmHours', 'powerupUsed', 'jerseyHash', 'location', 'countryCodeAlpha2Code', 'crossingStartingLineGap', 'rideOnsCounter', 'arrivalAtInSeconds', 'groupNumber'], inplace=True)

    race_data = race_data.rename(columns={'distanceInMeters': 'Distance'}).round(0)
    race_data = race_data.rename(columns={'powerInWattsPerKg': 'W/Kg'})
    race_data = race_data.rename(columns={'completionTimeInSeconds': 'Time'}).round(1)
    race_data['Name'] = race_data['firstName'] + race_data['lastName'] 

    race_data.drop(columns=['firstName', 'lastName'], inplace=True)

    return race_data
