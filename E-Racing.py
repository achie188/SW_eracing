import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import sys

sys.path.append('/Users/achie188/Library/CloudStorage/GitHub/Personal/SW_eracing')

from inputs.pull_zwift import pull_zwift
from inputs.pull_gsheet import pull_gsheet
from pipeline.formatting import format_results, add_team


interval=60 * 1000


#Stage_ids
stage1 = '3921745'
stage2 = '1111111'


#Get athlete_ids
ath_ids = pull_gsheet("Athlete_ids")

#Get Events
prologue = pull_gsheet("Prologue")
prologue = add_team(prologue, ath_ids)

s1r = pull_zwift(stage1)
s1p = pull_gsheet("Stage1")
s1 = format_results(s1r, s1p, ath_ids)



#Live event
live = pull_zwift(stage2)


#Get Standings
ind = pull_gsheet("Individual")
ind = add_team(ind, ath_ids)

team = pull_gsheet("Team")

ind['Total'] = pd.to_numeric(ind['Total'], errors='coerce')
team['Total Pts'] = pd.to_numeric(team['Total Pts'], errors='coerce')

ind = ind.sort_values(by='Total', ascending=False)
team = team.sort_values(by='Total Pts', ascending=False)

#orange = pull_gsheet("Orange")


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

st.write("The below shows the results and current standings of the Sexy Walrus E-Racing Series.")

tab1, tab2, tab3 = st.tabs(["Championship", "All Results", "LIVE NOW"])


with tab3:
    if live.empty:
        st.write("No live data right now.")
    else:
        st.dataframe(live, height=2000, hide_index=True)


with tab1:
    tab11, tab12 = st.tabs(['Individual', 'Teams'])

    with tab11:
        st.subheader('Individual')

        other_columns = [col for col in ind.columns if col != 'Total']
        column_order = other_columns[:2] + ['Total'] + other_columns[2:]
        ind = ind.reindex(columns=column_order)

        st.dataframe(ind, height=1500, hide_index=True)

    with tab12:
        st.subheader('Teams')

        other_columns = [col for col in team.columns if col != 'Total Pts']
        column_order = other_columns[:1] + ['Total Pts'] + other_columns[1:]
        team = team.reindex(columns=column_order)

        st.dataframe(team, hide_index=True)

with tab2:
    tab21, tab22, tab23, tab24, tab25, tab26 = st.tabs(["Prologue", "Stage 1", "Stage 2", "Stage 3", "Stage 4", "Stage 5"])

    with tab21:
        st.subheader('Prologue Results')

        st.dataframe(prologue, height=1500, hide_index=True)

    with tab22:
        st.subheader('Stage 1 Results')

        st.dataframe(s1, height=1500, hide_index=True)