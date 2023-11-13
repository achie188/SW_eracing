import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import sys

sys.path.append('/Users/achie188/Library/CloudStorage/GitHub/Personal/SW_eracing')

from inputs.pull_zwift import pull_zwift
from inputs.pull_gsheet import pull_gsheet
from pipeline.formatting import add_team, get_zwift_ids, final_format
from pipeline.calcs import get_stage, calc_overall_pts, calc_overall_orange


interval=60 * 1000

stages_complete = ['Prologue', 'Stage 1']


#Stage_ids
stages = pull_gsheet("Stage_ids")

stage_values = ['Stage_1', 'Stage_2a', 'Stage_2b', 'Stage_3', 'Stage_4', 'Stage_5', 'Stage_6']
zwift_ids = get_zwift_ids(stage_values, stages)

#Get athlete_ids
ath_ids = pull_gsheet("Athlete_ids")

#Get Events
prologue = pull_gsheet("Prologue")
prologue = add_team(prologue, ath_ids)


s1, orange_df = get_stage(zwift_ids[0], "Stage_1", ath_ids)
s2a, orange_df = get_stage(zwift_ids[1], "Stage_2a", ath_ids, orange_df)
s2b, orange_df = get_stage(zwift_ids[2], "Stage_2b", ath_ids, orange_df)
s3, orange_df = get_stage(zwift_ids[3], "Stage_3", ath_ids, orange_df)
s4, orange_df = get_stage(zwift_ids[4], "Stage_4", ath_ids, orange_df)
s5, orange_df = get_stage(zwift_ids[5], "Stage_5", ath_ids, orange_df)
s6, orange_df = get_stage(zwift_ids[6], "Stage_6", ath_ids, orange_df)


ind_pts, team_pts = calc_overall_pts(prologue, s1, s2a, s2b, s3, s4, s5, s6)
orange_df = calc_overall_orange(prologue, s1, s2a, s2b, s3, s4, s5, s6, stages_complete)

ind_pts = add_team(ind_pts, ath_ids)
team_pts = add_team(team_pts, ath_ids)
orange_df = add_team(orange_df, ath_ids)


prologue = final_format(prologue)
s1 = final_format(s1)
s2a = final_format(s2a)
s2b = final_format(s2b)
s3 = final_format(s3)
s4 = final_format(s4)
s5 = final_format(s5)
s6 = final_format(s6)


#Get live event
live = pull_zwift(zwift_ids[1])


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

st.write("The below shows the results and current standings of the Sexy Walrus E-Racing Series👇 ")

tab1, tab2, tab3 = st.tabs(["Championship", "All Results", "LIVE NOW"])


with tab3:
    if live is not None and not live.empty:
        st.dataframe(live, height=2000, hide_index=True)
    else:
        st.write("No live data right now.")


with tab1:
    tab11, tab12, tab13 = st.tabs(['Individual', 'Teams', 'Orange'])

    with tab11:
        st.subheader('Individual')
        st.dataframe(ind_pts, height=1500, hide_index=True)

    with tab12:
        st.subheader('Teams')
        st.dataframe(team_pts, hide_index=True)

    with tab13:
        st.subheader('Orange Jersey')
        st.dataframe(orange_df, height=1500, hide_index=True)

with tab2:
    tab21, tab22, tab23, tab24, tab25, tab26 = st.tabs(["Prologue", "Stage 1", "Stage 2", "Stage 3", "Stage 4", "Stage 5"])

    with tab21:
        st.subheader('Prologue Results')

        st.dataframe(prologue, height=1500, hide_index=True)

    with tab22:
        st.subheader('Stage 1 Results')

        st.dataframe(s1, height=1500, hide_index=True)