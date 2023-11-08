import pandas as pd
import requests
import streamlit as st

AUTH_TOKEN = st.secrets["zwift_credentials"]["AUTH_TOKEN"]



def pull_zwift(event_id):
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


