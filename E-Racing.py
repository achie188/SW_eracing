import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import sys
import os
from PIL import Image

sys.path.append('/Users/achie188/Library/CloudStorage/GitHub/Personal/SW_eracing')

from inputs.pull_zwift import pull_zwift
from inputs.helpers import get_ids
from inputs.rules import rules
from pipeline.formatting import get_zwift_ids, final_format, teams_slice
from pipeline.calcs import get_stage, calc_overall_pts, calc_overall_orange, handicaps_format


# Manual overrides
refresh_interval = 300
stages_complete = ['Prologue', 'Stage 1']



location = os.getcwd()


#Get ids
stages, ath_ids, prologue, pts, handicaps = get_ids()

stage_values = ['Stage_1', 'Stage_2', 'Stage_3', 'Stage_4', 'Stage_5', 'Stage_6']
zwift_ids = get_zwift_ids(stage_values, stages)

handicaps = handicaps_format(handicaps)

r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, handicaps_rules = rules()


#Get stage data
s1, orange_df = get_stage(zwift_ids[0], "Stage_1", ath_ids)
s2, orange_df = get_stage(zwift_ids[1], "Stage_2", ath_ids, orange_df)
s3, orange_df = get_stage(zwift_ids[2], "Stage_3", ath_ids, orange_df)
s4, orange_df = get_stage(zwift_ids[3], "Stage_4", ath_ids, orange_df)
s5, orange_df = get_stage(zwift_ids[4], "Stage_5", ath_ids, orange_df)
s6, orange_df = get_stage(zwift_ids[5], "Stage_6", ath_ids, orange_df)


#Calc points
ind_pts, team_pts, kom_pts, sprinter_pts = calc_overall_pts(prologue, s1, s2, s3, s4, s5, s6)
orange_df = calc_overall_orange(prologue, s1, s2, s3, s4, s5, s6, stages_complete)


#Final formatting
prologue = final_format(prologue)
s1 = final_format(s1)
s2 = final_format(s2)
s3 = final_format(s3)
s4 = final_format(s4)
s5 = final_format(s5)
s6 = final_format(s6)


#Get live event
live = pull_zwift(zwift_ids[1])

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
        st.dataframe(live, height=2000, hide_index=True)
    else:
        st.write("No live data right now.")




                                                    ###############################
                                                    ###### CHAMPIONSHIP TAB #######
                                                    ###############################

with tab1:
    tab11, tab12, tab13, tab14, tab15, tab16 = st.tabs(['Individual', 'Teams', 'Orange', 'KOM', 'Sprinter', 'Handicaps'])

    with tab11:
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

    with tab12:
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

    with tab13:
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
    tab21, tab22, tab23, tab24, tab25, tab26 = st.tabs(["Prologue", "Stage 1", "Stage 2", "Stage 3", "Stage 4", "Stage 5"])

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
            with st.expander("Team Tesla"):
                st.markdown('''
                            #### Race Report - Tesla
                            
                            Go go go. George Dix is flying at the front of the race. His team behind them. They look amazing in their Amazon Prime blue jerseys. Dixy is so angry you can tell by looking at his electronic avatar. Why the hell are they going so fast.

                            Meanwhile the Tesla Thames Water team with sponsors hell bent on rehabilitating their reputation look formidable in our red T jerseys! Looking comfortable we were all present and corrrect with Scottie up in the break feeding us live information on Chris Monk’s state of mind. 

                            We appproached Mount doom looming in the distance like a bunch of super charged hobbits who have got to get back to the shire in time for Old Gaffer Gamgee’s mutton eating competition.

                            The sprint came and went with no one on our team clear where the sprint was and our main sprinter Edwin unable to hear the rest of us which led to a comical if not frustrating 3 mins of people shouting into the wind and Ed smith sprinting at anything he could see.

                            Anyway the real quiz came along pretty sharpish and the pack was set. About half way some bastard launched themselves and the pack was split and only one TTW was in the front group, me. Scottie was quickly gobbled up and spat out and up ahead Chris Monk continued to forge on in his skin tight orange jersey. 

                            We reached the top and toppled over the edge. I found myself in a group of 2 chasing Tom and Chris up ahead. I worked as hard as I could to stave off any chance of the group behind catching and James Warman sat neatly behind like Frodo to my Sam. We were catching Chris but would run out of road and so we were fighting for 3rd place. Just like in the books at the last minute Frodo snuck past Sam and took the win. 

                            The remainder of the TTWs fellowship rolled in happily as a group bruised but in no way beaten. 

                            The old truism was muttered over comms..
                            ‘The winners of week 1 have never won the season!’ 

                            Someone belched loudly''')
            with st.expander("Team AstraZenaca"):
                st.markdown('''
                            #### Race Report - AstraZenaca
                            
                            A tough night for the Trailfinders.

                            Camp was very upbeat leading up to the season opener. The new faces had settled in nicely and they’d put together a more than respectable set of prologue times. And instead of the habitual pre-race panic, there was an air of serenity in the group. Confidence was high.
                            
                            New signing Foley, in particular, was chomping at the bit to prove his worth to the sponsors. He was in great shape and he knew it. He was straight out into the breakaway, going toe to toe with the mercurial Monkfish. 

                            Unfortunately, the rest of the team were no match for ‘Foley Fever’. Friend, Lopez and Tyler looked well short of last season’s form. The diamonds they once had in their legs, had turned into thick, gloopy, treacle. Normally so reliable in the sprint, they were caught at the back of the peloton reminiscing over former glories. Singh did fight hard on the climb, but his lungs were soon full of toxic levels of Volcanic ash and that was his day done. Wilson was perhaps the bravest of the Trailfinders tonight – this was her first race as a professional, and she was shown no mercy by the cut-throat Amazonian prime captain, Dix. 

                            Lego Boots – with the race director in their ranks – were unstoppable tonight and deserve real credit. With their big budget and unlimited supply of baby oil, they’ve cemented their reputation as the bookie’s favourites.  Foley, Tesla captain Humphreys, and Amazon debutant Warmachine – were all up there at the business end…but they couldn’t quite get hold of those slippery Boots out front. 

                            It'll be a restless night for the AZ Trailfinders there’s no doubt about it. But we’re only in week 1. And as the old saying goes, you can’t lose it in week 1. Can you?''')




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
            col11, col12 = st.columns([1,3])

            with col12:           
                st.subheader('Lego pours millions into doomed vanity project')
                st.markdown('''
                            Sunday 5th November 2023 Legoland
                         
                            For years the top team at Lego have been considering a move into the world of pro cycling. And this year, they have finally taken the plunge, emptied their pockets, gathered up the scattered pennies, and spent them on a pro e-cycling outfit.
                            ''')
                
            with col11:
                st.image(lego_image, width = 150)
            
            st.markdown('''
                        To do so they have teamed up with Boots. It feels like an odd combination, (and a few stories have circulated about how the CFO at Boots was taken out for a lobster lunch by a few Lego directors. It transpired the CFO was on the way out of the company anyway, got totally pissed, and ended up signing up to the agreement muttering “fuck it all” under his breath). 

                        Despite the coming together of these two behemoths, Lego Boots have been struggling to raise the cash to entice one rider in particular: Bill Smith.  According to reliable sources, Bill was demanding an extortionate salary, and therefore a third title sponsor had to be found at short notice. Some big names were interested, but time was cripplingly short, and the best the Lego Boots partnership could do was P&O ferries, who gladly provided the extra cash to secure the services of the hardened professional Bill Smith,(despite P&O knowing that P&O was bound to be left off the title name when used by Adam Bylthe on GCN commentary). 

                        As part of Bill’s contract, he had demanded that he would need a full team to support him in his GC bid, and insisted it would be “all in for Bill”.  So what was needed was domestiques willing to turn themselves inside out, upside down, and over the hill and far away for Bill, week in, week out. 

                        To do this, Lego Boots immediately crawled all over the decaying carcass of what was previously Routes Coffee TZA Draconi. And like a hungry vulture, they picked up nearly the whole squad that had previously been punching holes in walls for the ‘Al brothers’.  

                        With contracts expired, and the wise heads of Al and Al now out the picture, Lizzy, Nic, Tom and Tom were happy to sign up to Lego Boots and look for new opportunities of their own. (Little did they know Bill Smith had his own designs as to what they would be allowed to do on the road.)

                        With a dwindling purse, Lego Boots still had spots in their rooster to fill. Wetbeak and Monk, a couple of older riders well past their peak, were brought on board. Largely because no other team would take them, and Lego Boots is paying them peanuts. 

                        And the final spot went to Alex Hadcock. A talented climber, but a neo-pro and totally untested in the heated world of Walrus e-cycling. Some say this deal was a gamble, Lego Boots would say this deal was cheap as chips. 

                        Only time will tell how delicious those chips will be.
                        ''')
        
        with col2:
            st.subheader('Team Lego Boots')
            st.dataframe(lego_boots, height = int(35.2*(lego_boots.shape[0]+1)), hide_index=True)

    with tab43:
        col1, col2 = st.columns(2)

        with col1:
            col11, col12 = st.columns([3,1])

            with col11:           
                st.subheader('Amazon Beaconsfield Services')

            with col12:
                st.image(amazon_image, width = 150)

        with col2:
            st.subheader('Team Amazon Beaconsfield Services')
            st.dataframe(amazon, height = int(35.2*(amazon.shape[0]+1)), hide_index=True)

    with tab44:
        col1, col2 = st.columns(2)

        with col1:
            col11, col12 = st.columns([3,1])

            with col11: 
                st.subheader('Tesla and Thames Water Unite in Cycling Endeavor for the Greater Good')
                st.markdown('''
                            FOR IMMEDIATE RELEASE
                         
                            London, UK, November 4, 2023
                            ''')
            with col12:
                st.image(tesla_image, width = 150)

            st.markdown('''
                        In a groundbreaking collaboration that defies expectations, Tesla, the pioneering electric car company, and Thames Water, the UK's leading water utility provider, have joined forces to propel the world of professional cycling into a new era.

                        The partnership was officially unveiled at a press conference attended by Elon Musk, the visionary CEO of Tesla, and Alastair Cochran, the forward-thinking CEO of Thames Water. Their announcement marks a significant moment in the history of cycling as the two seemingly unrelated giants pool their resources to launch a brand-new cycling team: Team Tesla Thames Water.

                        This unique partnership is set to bring a fresh perspective to the world of professional cycling, as Tesla's commitment to clean energy and innovation marries Thames Water's dedication to responsible water management. The unlikely union underscores the shared ambition to conquer the 2023 Zwift Championships, one of the most prestigious events in the cycling calendar.

                        In a surprising twist, the newly formed Team Tesla Thames Water has signed Rich Tyler, a rising star in the cycling world, to bolster their roster. Known for his remarkable sprinting skills and podium finishes, Tyler is poised to be a key asset in the team's pursuit of championship glory.

                        However, the team's lineup isn't complete without the enigmatic Edwin Smith, a mercurial talent whose career has spanned decades. The question on everyone's mind is whether Smith, now considered "long in the tooth" by some, still possesses the prowess to contribute to the team's quest for victory. His inclusion adds an element of intrigue to the team's composition.

                        When asked about the partnership, Elon Musk stated, "Cycling is more than just sport; it's a symbol of human potential and the power of sustainable transportation. Our partnership with Thames Water aims to underscore the importance of preserving our planet's resources, just as we do with electric vehicles. Team Tesla Thames Water is not just a cycling team; it's a testament to our shared commitment to a greener future."

                        Alastair Cochran, CEO of Thames Water, added, "As stewards of water, we understand the significance of responsible resource management. Joining forces with Tesla is a declaration that our actions speak louder than words. We're excited about the journey ahead, both on the road and in our shared mission to champion sustainability."

                        The team's distinctive blue and green jerseys symbolize the fusion of electric energy and water, while reflecting their dedication to clean, renewable energy sources. It's a visual reminder of their commitment to a more sustainable future.

                        Team Tesla Thames Water also announced an exciting partnership with Scott bikes and Volvo cars to elevate their on-road and off-road experiences. Sunweb remains a valued partner, ensuring the team's continued growth and success.

                        With the 2023 Zwift Championships on the horizon, Team Tesla Thames Water's journey promises to be a thrilling blend of competition and commitment to the environment, as they ride towards a future where sport and sustainability go hand in hand.
                        ''')

        with col2:
            st.subheader('Team Tesla Thames Water')
            st.dataframe(tesla, height = int(35.2*(tesla.shape[0]+1)), hide_index=True)

    with tab45:
        col1, col2 = st.columns(2)

        with col1:
            col11, col12 = st.columns([3,1])

            with col11: 
                st.subheader('The e-Pedlars Lancet - AstraZenaca Trailfinders Partnership')
                st.markdown('''
                            By Penny Farthing
                         
                            7/11/2023
                            ''')
            with col12:
                st.image(azt_image, width = 150)

            st.markdown('''
                        In a surprising twist in the world of SW eracing, the remnants of the infamous Evil Greens have found a new lease of life through a partnership between AstraZeneca and Trailfinders. This unexpected alliance was driven by a unique vision: AstraZeneca's aspiration to invest more in Watopian diseases whilst supporting washed up Greens' bruiser, Teo Lopez.

                        Now captain Lopez had endured a challenging summer, having been attacked by a swarm of extremely venomous Watopian feather beetles, on a late season training ride. His personal journey resonated with AstraZeneca's mission, and the addition of Trailfinders was perfect for this new, intrepid, outfit.

                        Vice Captain Dickie Tyler will play a crucial role in maintaining team morale and optimising strategy, whilst seasoned veterans, Rob Friend and Duncan Singh, bring a wealth of experience and camaraderie. Duncan Singh aptly remarked, "We might be 'wily old heads,' but we still have a few tricks up our sleeves."

                        The team welcoms fresh faces, including Davyd Greenish, who excitedly declared, "I'm thrilled to be part of this team!" Beth Wilson and Nick Foley add youthful enthusiasm and unpredictability to the squad.

                        This partnership not only breathes new life into the Greens but also signifies a unique fusion of goals – AstraZeneca's commitment to Watopian diseases and the resilience and determination of the once-feared Evil Greens. It's a story of renewal and hope, anchored by the experienced, the determined, and the newcomers, all propelled forward by a shared mission to make a meaningful impact in the e-racing world.
                        ''')
        
        with col2:
            st.subheader('The Evil Greens')
            st.dataframe(astrazen, height = int(35.2*(astrazen.shape[0]+1)), hide_index=True)