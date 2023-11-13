import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import sys

sys.path.append('/Users/achie188/Library/CloudStorage/GitHub/Personal/SW_eracing')

from inputs.pull_zwift import pull_zwift
from inputs.pull_gsheet import pull_gsheet
from pipeline.formatting import add_team, get_zwift_ids, final_format, highlight_team
from pipeline.calcs import get_stage, calc_overall_pts, calc_overall_orange


interval=60 * 1000

stages_complete = ['Prologue', 'Stage 1']


#Stage_ids
stages = pull_gsheet("Stage_ids")

stage_values = ['Stage_1', 'Stage_2', 'Stage_3', 'Stage_4', 'Stage_5', 'Stage_6']
zwift_ids = get_zwift_ids(stage_values, stages)

#Get athlete_ids
ath_ids = pull_gsheet("Athlete_ids")

#Get Events
prologue = pull_gsheet("Prologue")
prologue = add_team(prologue, ath_ids)


s1, orange_df = get_stage(zwift_ids[0], "Stage_1", ath_ids)
s2, orange_df = get_stage(zwift_ids[1], "Stage_2", ath_ids, orange_df)
s3, orange_df = get_stage(zwift_ids[2], "Stage_3", ath_ids, orange_df)
s4, orange_df = get_stage(zwift_ids[3], "Stage_4", ath_ids, orange_df)
s5, orange_df = get_stage(zwift_ids[4], "Stage_5", ath_ids, orange_df)
s6, orange_df = get_stage(zwift_ids[5], "Stage_6", ath_ids, orange_df)


ind_pts, team_pts, kom_pts, sprinter_pts = calc_overall_pts(prologue, s1, s2, s3, s4, s5, s6)
orange_df = calc_overall_orange(prologue, s1, s2, s3, s4, s5, s6, stages_complete)

ind_pts = add_team(ind_pts, ath_ids)
orange_df = add_team(orange_df, ath_ids)

# ind_pts = ind_pts.style.apply(highlight_team, subset=['Team'], axis=0)

prologue = final_format(prologue)
s1 = final_format(s1)
s2 = final_format(s2)
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

tab1, tab2, tab3, tab4 = st.tabs(["Championship", "All Results", "LIVE NOW", "About"])


with tab3:
    if live is not None and not live.empty:
        st.dataframe(live, height=2000, hide_index=True)
    else:
        st.write("No live data right now.")


with tab1:
    tab11, tab12, tab13, tab14, tab15 = st.tabs(['Individual', 'Teams', 'Orange', 'KOM', 'Sprinter'])

    with tab11:
        st.subheader('Individual Series Standings')
        st.dataframe(ind_pts, height=1500, hide_index=True)

    with tab12:
        st.subheader('Teams Series Standings')
        st.dataframe(team_pts, hide_index=True)

    with tab13:
        st.subheader('Orange Jersey Race')
        st.dataframe(orange_df, height=1500, hide_index=True)

    with tab14:
        st.subheader('Polka Dot Jersey')
        st.dataframe(kom_pts, height=1500, hide_index=True)

    with tab15:
        st.subheader('Ciclamino Jersey')
        st.dataframe(sprinter_pts, height=1500, hide_index=True)

with tab2:
    tab21, tab22, tab23, tab24, tab25, tab26 = st.tabs(["Prologue", "Stage 1", "Stage 2", "Stage 3", "Stage 4", "Stage 5"])

    with tab21:
        st.subheader('Prologue Results')

        st.dataframe(prologue, height=1500, hide_index=True)

    with tab22:
        st.subheader('Stage 1 Results')

        st.dataframe(s1, height=1500, hide_index=True)

with tab4:
    tab41, tab42, tab43, tab44, tab45 = st.tabs(['Walrus E-Racing', 'Lego Boots', 'Amazon Beaconsfield Services', 'Tesla Thames Water', 'AstraZenaca Trailfinders'])

    with tab41:
        st.subheader('Walrus E-Racing 2023')
        st.write('Prologue Results')

    with tab42:
        st.subheader('Lego Boots')
        st.write('Prologue Results')

    with tab43:
        st.subheader('Amazon Beaconsfield Services')
        st.write('Prologue Results')

    with tab44:
        st.subheader('Tesla Thames Water')
        st.write('Prologue Results')

    with tab45:
        st.subheader('AstraZenaca Trailfinders')
        st.write('''The e-Pedlars Lancet 7/11/2023

By Penny Farthing

In a surprising twist in the world of SW eracing, the remnants of the infamous Evil Greens have found a new lease of life through a partnership between AstraZeneca and Trailfinders. This unexpected alliance was driven by a unique vision: AstraZeneca's aspiration to invest more in Watopian diseases whilst supporting washed up Greens' bruiser, Teo Lopez.

Now captain Lopez had endured a challenging summer, having been attacked by a swarm of extremely venomous Watopian feather beetles, on a late season training ride. His personal journey resonated with AstraZeneca's mission, and the addition of Trailfinders was perfect for this new, intrepid, outfit.

Vice Captain Dickie Tyler will play a crucial role in maintaining team morale and optimising strategy, whilst seasoned veterans, Rob Friend and Duncan Singh, bring a wealth of experience and camaraderie. Duncan Singh aptly remarked, "We might be 'wily old heads,' but we still have a few tricks up our sleeves."

The team welcoms fresh faces, including Davyd Greenish, who excitedly declared, "I'm thrilled to be part of this team!" Beth Wilson and Nick Foley add youthful enthusiasm and unpredictability to the squad.

This partnership not only breathes new life into the Greens but also signifies a unique fusion of goals – AstraZeneca's commitment to Watopian diseases and the resilience and determination of the once-feared Evil Greens. It's a story of renewal and hope, anchored by the experienced, the determined, and the newcomers, all propelled forward by a shared mission to make a meaningful impact in the e-racing world.''')