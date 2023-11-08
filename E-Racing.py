import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import sys

sys.path.append('/Users/achie188/Library/CloudStorage/GitHub/Personal/SW_eracing')


from pull_zwift import pull_zwift

#3921745
event_id = '3917221'

#Test event
t1 = pull_zwift(event_id)


interval=5 * 1000

#rename columns
t1 = t1.rename(columns={'position': '#'})
t1 = t1.rename(columns={'heartRateInBpm': 'HR'})
t1 = t1.rename(columns={'powerOutputInWatts': 'Watts'})
t1 = t1.rename(columns={'powerInWattsPerKg': 'Watts/Kg'}).round(2)
t1 = t1.rename(columns={'liveTimeGapToLeaderInSeconds': 'Gap'})
t1 = t1.rename(columns={'completionTimeInSeconds': 'Finish Time'})
t1 = t1.rename(columns={'distanceInMeters': 'Distance'}).round(1)
t1 = t1.rename(columns={'speedInKmHours': 'Speed'}).round(1)
t1 = t1.rename(columns={'powerUpUsed': 'PowerUps Used'})



# Set up Streamlit app
st.set_page_config(
    page_title="SW E-Racing",
    layout="wide"
)

st_autorefresh(interval, limit=1000)

st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)

st.subheader("Welcome to the Sexy Walrus E-Racing Series 2023! 👋")

st.write("The below show live data from the Sexy Walrus E-Racing Series - Stage 1.")

if t1.empty:
    st.write("Race not started yet, no data. Please be patient.")
else:
    st.dataframe(t1, height=2000, hide_index=True)