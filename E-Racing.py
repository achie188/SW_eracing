import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import sys
import os
from PIL import Image

sys.path.append('/Users/achie188/Library/CloudStorage/GitHub/Personal/SW_eracing')

from inputs.helpers import get_ids
from inputs.rules import rules
from inputs.press_releases import press_releases
from inputs.race_reports import race_reports
from inputs.pull_zwift import pull_zwift
from pipeline.formatting import get_zwift_ids, final_format, teams_slice, format_results
from pipeline.calcs import get_stage, calc_overall_pts, calc_overall_orange, handicaps_format
from pipeline.ttt import sort_ttt


# Manual overrides
refresh_interval = 300
stages_complete = ['Prologue', 'Stage 1', 'Stage 2', 'Stage 3', 'TTT']



location = os.getcwd()


#Get ids
stages, ath_ids, prologue, pts, handicaps, orange_pass = get_ids("No")

stage_values = ['Stage_1', 'Stage_2', 'Stage_3', 'Stage_4', 'Stage_5', 'Stage_6']
zwift_ids = get_zwift_ids(stage_values, stages)

handicaps = handicaps_format(handicaps)

#Get text
r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, handicaps_rules = rules()
lego_pr, tesla_pr, azt_pr, abs_pr = press_releases()
s1_azt, s1_tesla, s2_tesla, s2_abs, s2_azt, s3_tesla, s3_lego, ttt_gen, ttt_azt, ttt_tesla = race_reports()

#Get stage data
s1, orange_df = get_stage(zwift_ids[0], "Stage_1", ath_ids, "No")
s2, orange_df = get_stage(zwift_ids[1], "Stage_2", ath_ids, "No", orange_df)
s3, orange_df = get_stage(zwift_ids[2], "Stage_3", ath_ids, "No", orange_df)

ttt_ind, ttt_team, orange_df = sort_ttt(orange_df, ath_ids, "No")

s4, orange_df = get_stage(zwift_ids[3], "Stage_4", ath_ids, "No", orange_df)
s5, orange_df = get_stage(zwift_ids[4], "Stage_5", ath_ids, "No", orange_df)
s6, orange_df = get_stage(zwift_ids[5], "Stage_6", ath_ids, "No", orange_df)



#Orange Jersey
orange_df = calc_overall_orange(prologue, s1, s2, s3, ttt_ind, s4, s5, s6, stages_complete, orange_pass)


#Calc points
ind_pts, team_pts, kom_pts, sprinter_pts = calc_overall_pts(prologue, s1, s2, s3, ttt_ind, s4, s5, s6, ttt_team)





#Final formatting
prologue = final_format(prologue)
s1 = final_format(s1)
s2 = final_format(s2)
s3 = final_format(s3)

ttt = final_format(ttt_ind)

s4 = final_format(s4)
s5 = final_format(s5)
s6 = final_format(s6)


#Get live event
live = pull_zwift('3995583')
# live = format_results(live, ath_ids)


#Team slices
lego_boots = teams_slice(ind_pts, "Lego", handicaps, stages_complete)
amazon = teams_slice(ind_pts, "ABS", handicaps, stages_complete)
tesla = teams_slice(ind_pts, "Tesla", handicaps, stages_complete)
astrazen = teams_slice(ind_pts, "AZT", handicaps, stages_complete)


#Get images
lego_image = Image.open(location + '/inputs/raceinfo/lego.png')
amazon_image = Image.open(location + '/inputs/raceinfo/amazon.png')
azt_image = Image.open(location + '/inputs/raceinfo/astrazenaca.png')
tesla_image = Image.open(location + '/inputs/raceinfo/tesla.png')
sw_image = Image.open(location + '/inputs/raceinfo/SW-logo.png')




# Set up Streamlit app
st.set_page_config(
    page_title="SW E-Racing",
    layout="wide"
)

st_autorefresh(refresh_interval*1000, limit=1000)

st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)

st.subheader("Welcome to the Sexy Walrus E-Racing Series! 👋")
st.write("The below shows the results and current standings of the Sexy Walrus E-Racing Series👇 ")

tab1, tab2, tab3, tab4 = st.tabs(["Championship", "All Results", "About", "LIVE NOW!"])




                                                    ###############################
                                                    ######## LIVE DATA TAB ########
                                                    ###############################

with tab4:

    if live is not None and not live.empty:
        st.subheader('Live Race')
        st.dataframe(live, height = int(35.2*(live.shape[0]+1)), hide_index=True)
    else:
        st.write("No live data right now.")
   




                                                    ###############################
                                                    ###### CHAMPIONSHIP TAB #######
                                                    ###############################

with tab1:
    tab11, tab12, tab13, tab14, tab15, tab16 = st.tabs(['Teams', 'Orange', 'Individual', 'KOM', 'Sprinter', 'Handicaps'])

    with tab13:
        col1, col2 = st.columns([2,3])

        with col1:
            st.subheader('Individual Series Standings')
            st.dataframe(ind_pts, height = int(35.2*(ind_pts.shape[0]+1)), hide_index=True)

        with col2:
            st.subheader('Relevant Rules')
            with st.expander("5. THE POINTS SYSTEM EXPLAINED"):
                st.markdown(r5)
            with st.expander("6. Category 1: Finishing Position Points"):
                st.markdown(r6)
            with st.expander("7. Category 2: KOM Points"):
                st.markdown(r7)
            with st.expander("8. Category 3: Intermediate Sprint Points"):
                st.markdown(r8)
            with st.expander("9. Most Aggressive Rider"):
                st.markdown(r9)
            with st.expander("10. Race Reports"):
                st.markdown(r10)
            with st.expander("12. Quibbling"):
                st.markdown(r12)       
            with st.expander("13. Director’s Decision"):
                st.markdown(r13)

    with tab11:
        col1, col2 = st.columns([2,3])

        with col1:
            st.subheader('Teams Series Standings')
            st.dataframe(team_pts, hide_index=True)

        with col2:
            st.subheader('Relevant Rules')
            with st.expander("5. THE POINTS SYSTEM EXPLAINED"):
                st.markdown(r5)
            with st.expander("6. Category 1: Finishing Position Points"):
                st.markdown(r6)
            with st.expander("7. Category 2: KOM Points"):
                st.markdown(r7)
            with st.expander("8. Category 3: Intermediate Sprint Points"):
                st.markdown(r8)
            with st.expander("9. Most Aggressive Rider"):
                st.markdown(r9)
            with st.expander("10. Race Reports"):
                st.markdown(r10)
            with st.expander("12. Quibbling"):
                st.markdown(r12)       
            with st.expander("13. Director’s Decision"):
                st.markdown(r13)    

    with tab12:
        col1, col2 = st.columns([2,3])

        with col1:
            st.subheader('Orange Jersey Race')
            st.dataframe(orange_df, height = int(35.2*(orange_df.shape[0]+1)), hide_index=True)

        with col2:
            st.subheader('Relevant Rules')
            with st.expander("11. Orange Jersey Competition"):
                st.markdown(r11)
            with st.expander("12. Quibbling"):
                st.markdown(r12)       
            with st.expander("13. Director’s Decision"):
                st.markdown(r13)

    with tab14:
        col1, col2 = st.columns([2,3])

        with col1:
            st.subheader('Polka Dot Jersey')
            st.dataframe(kom_pts, height = int(35.2*(kom_pts.shape[0]+1)), hide_index=True)

        with col2:
            st.subheader('Relevant Rules')
            with st.expander("4. Designated Sprinter/Climber"):
                st.markdown(r4)
            with st.expander("7. Category 2: KOM Points"):
                st.markdown(r7)
            with st.expander("12. Quibbling"):
                st.markdown(r12)       
            with st.expander("13. Director’s Decision"):
                st.markdown(r13)

    with tab15:
        col1, col2 = st.columns([2,3])

        with col1:
            st.subheader('Ciclamino Jersey')
            st.dataframe(sprinter_pts, height = int(35.2*(sprinter_pts.shape[0]+1)), hide_index=True)

        with col2:
            st.subheader('Relevant Rules')
            with st.expander("4. Designated Sprinter/Climber"):
                st.markdown(r4)
            with st.expander("8. Category 3: Intermediate Sprint Points"):
                st.markdown(r8)
            with st.expander("12. Quibbling"):
                st.markdown(r12)       
            with st.expander("13. Director’s Decision"):
                st.markdown(r13)

    with tab16:
        col1, col2 = st.columns([2,3])

        with col1: 
            st.subheader('Handicaps')
            st.dataframe(handicaps, height= int(35.2*(handicaps.shape[0]+1)), hide_index=True)
        
        with col2:
            st.subheader('Relevant Rules')
            with st.expander("Handicapping System"):
                st.markdown(handicaps_rules)
            with st.expander("12. Quibbling"):
                st.markdown(r12)       
            with st.expander("13. Director’s Decision"):
                st.markdown(r13)




                                                ###############################
                                                ######### RESULTS TAB #########
                                                ###############################

with tab2:
    tab21, tab22, tab23, tab24, tab25, tab26, tab27 = st.tabs(["Prologue", "Stage 1", "Stage 2", "Stage 3", "TTT", "Stage 4", "Stage 5"])

    with tab21:
        col1, col2 = st.columns([3,5])
        
        with col1:
            st.subheader('Prologue Results')
            st.dataframe(prologue, height = int(35.2*(prologue.shape[0]+1)), hide_index=True)

        with col2:
            st.subheader('Relevant Rules')
            with st.expander("1. Overview"):
                st.markdown(r1)
            with st.expander("3. Breakaways"):
                st.markdown(r3)
            with st.expander("4. Designated Sprinter/Climber"):
                st.markdown(r4)
            with st.expander("12. Quibbling"):
                st.markdown(r12)       
            with st.expander("13. Director’s Decision"):
                st.markdown(r13)

    with tab22:
        col1, col2 = st.columns([5,3])

        with col1:
            st.subheader('Stage 1 Results')
            st.dataframe(s1, height = int(35.2*(s1.shape[0]+1)), hide_index=True)

        with col2:
            st.subheader('Race Reports')
            with st.expander("Team Tesla - George Humphreys"):
                st.markdown(s1_tesla)
            with st.expander("Team AstraZenaca - Teo Lopez"):
                st.markdown(s1_azt)

    with tab23:
        col1, col2 = st.columns([5,3])

        with col1:
            st.subheader('Stage 2 Results')
            st.dataframe(s2, height = int(35.2*(s2.shape[0]+1)), hide_index=True)

        with col2:
            st.subheader('Race Reports')
            with st.expander("Team Tesla - George Humphreys"):
                st.markdown(s2_tesla)
            with st.expander("Team ABS - Cameron Graley"):
                st.markdown(s2_abs)
            with st.expander("Team AZT - Rich Tyler"):
                st.markdown(s2_azt)

    with tab24:
        col1, col2 = st.columns([5,3])

        with col1:
            st.subheader('Stage 3 Results')
            st.dataframe(s3, height = int(35.2*(s3.shape[0]+1)), hide_index=True)

        with col2:
            st.subheader('Race Reports')
            with st.expander("Team Tesla - George Humphreys"):
                st.markdown(s3_tesla)
            with st.expander("Team Lego Boots P&O debrief meeting with sponsors - Ed Humphreys"):
                st.markdown(s3_lego)

    with tab25:
        col1, col2 = st.columns([5,3])

        with col1:
            st.subheader('Team Time Trial')
            st.dataframe(ttt_team, height = int(35.2*(ttt_team.shape[0]+1)), hide_index=True)
            st.dataframe(ttt, height = int(35.2*(ttt_ind.shape[0]+1)), hide_index=True)

        with col2:
            st.subheader('Race Reports')
            with st.expander("ARCHIVES - The Dark Art of the Team Time Trial"):
                 st.markdown(ttt_gen)
            with st.expander("Team AZT - Teo Lopez"):
                st.markdown(ttt_azt)
            with st.expander("Team Tesla Press Briefing - Graeme Acheson"):
                st.markdown(ttt_tesla)

    with tab26:
        col1, col2 = st.columns([5,3])

        with col1:
            st.subheader('Stage 4 Results')
            # st.dataframe(s4, height = int(35.2*(s4.shape[0]+1)), hide_index=True)

    with tab27:
        col1, col2 = st.columns([5,3])

        with col1:
            st.subheader('Stage 5 Results')
            # st.dataframe(s5, height = int(35.2*(s5.shape[0]+1)), hide_index=True)






                                                ###############################
                                                ########## ABOUT TAB ##########
                                                ###############################

with tab3:
    tab41, tab42, tab43, tab44, tab45 = st.tabs(['Walrus E-Racing', 'Lego Boots', 'Amazon Beaconsfield Services', 'Tesla Thames Water', 'AstraZenaca Trailfinders'])

    with tab41:
        st.subheader('Sexy Walrus E-Racing League Rules 2023')
        with st.expander("1. Overview"):
            st.markdown(r1)       
        with st.expander("2. How To Win?"):
            st.markdown(r2)       
        with st.expander("3. Breakaways"):
            st.markdown(r3)       
        with st.expander("4. Designated Sprinter/Climber"):
            st.markdown(r4)       
        with st.expander("5. THE POINTS SYSTEM EXPLAINED"):
            st.markdown(r5)       
        with st.expander("6. Category 1: Finishing Position Points"):
            st.markdown(r6)       
        with st.expander("7. Category 2: KOM Points"):
            st.markdown(r7)       
        with st.expander("8. Category 3: Intermediate Sprint Points"):
            st.markdown(r8)       
        with st.expander("9. Most Aggressive Rider"):
            st.markdown(r9)       
        with st.expander("10. Race Reports"):
            st.markdown(r10)       
        with st.expander("11. Orange Jersey Competition"):
            st.markdown(r11)       
        with st.expander("12. Quibbling"):
            st.markdown(r12)       
        with st.expander("13. Director’s Decision"):
            st.markdown(r13)

    with tab42:
        col1, col2 = st.columns(2)

        with col1:
            col11, col12 = st.columns([1,4])

            with col12:           
                st.subheader('Lego Pours Millions Into Doomed Vanity Project')
                st.markdown('''
                            Sunday 5th November 2023 
                            
                            Legoland
                            ''')
                
            with col11:
                st.image(lego_image, width = 150)
            
            st.markdown(lego_pr)
        
        with col2:
            st.subheader('Team Lego Boots')
            st.dataframe(lego_boots, height = int(35.2*(lego_boots.shape[0]+1)), hide_index=True)

    with tab43:
        col1, col2 = st.columns(2)

        with col1:
            col11, col12 = st.columns([1,4])

            with col12:           
                st.subheader('Amazon Beaconsfield Services')
                st.markdown('''
                            10th November 2023 
                            
                            Beaconsfield Services, M40, J2
                            ''')
                
            with col11:
                st.image(amazon_image, width = 150)

            st.markdown(abs_pr)

        with col2:
            st.subheader('Team Amazon Beaconsfield Services')
            st.dataframe(amazon, height = int(35.2*(amazon.shape[0]+1)), hide_index=True)

    with tab44:
        col1, col2 = st.columns(2)

        with col1:
            col11, col12 = st.columns([1,4])

            with col12: 
                st.subheader('Tesla and Thames Water Unite in Cycling Endeavor for the Greater Good')
                st.markdown('''
                            FOR IMMEDIATE RELEASE
                         
                            London, UK, November 4, 2023
                            ''')
            with col11:
                st.image(tesla_image, width = 150)

            st.markdown(tesla_pr)

        with col2:
            st.subheader('Team Tesla Thames Water')
            st.dataframe(tesla, height = int(35.2*(tesla.shape[0]+1)), hide_index=True)

    with tab45:
        col1, col2 = st.columns(2)

        with col1:
            col11, col12 = st.columns([1,4])

            with col12: 
                st.subheader('The E-Pedlars Lancet - AstraZenaca Trailfinders Partnership')
                st.markdown('''
                            By Penny Farthing
                         
                            7th November 2023
                            ''')
            with col11:
                st.image(azt_image, width = 150)

            st.markdown(azt_pr)
        
        with col2:
            st.subheader('The Evil Greens')
            st.dataframe(astrazen, height = int(35.2*(astrazen.shape[0]+1)), hide_index=True)