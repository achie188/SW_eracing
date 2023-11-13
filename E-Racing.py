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
        st.subheader('Sexy Walrus E-Racing League 2023')
        st.markdown('''
### 1. Overview
                 
1.1 There will be 5 weeks of action. Each week will have one or two races. Details of what each week will entail will be released in good time before each week.
                    
1.2. Here is a summary of what is in store:  
                 
- Prologue: Individual time trial. 7.3km. Done on handicapped bikes. Route is the start of Road to Ruins, ending on the climb at a virtual banner. (Keen eyes will spot this is the same prologue as last year. This allows some fine tuning of handicaps prior to the real racing. 
- Weeks 1, 2, 3 and 4: classic Zwift racing. 30-45 mins. Each week the course will be chosen by a different team. 
- Team Time Trial: Circa 40-45 min race. The time for this TTT is TBC. 
- Week 5: a longer race on an attritional course, serving as the grand finale. (Circa 55 mins). 
                    
1.3 There will be organised breakaways for weeks 1 to 4. There will also be ‘designated sprinters’ or ‘designated climbers’ for these weeks. And the usual orange jersey competition will be happening.

### 2. How To Win?

2.1 The league will be won by the team that amasses the most points over the course of the season.
2.2. See later on in this document for a summary of how the points system works.
3. Breakaways
3.1. Some races will have a breakaway. This will work by 3 riders being chosen to form a breakaway.
3.2. There will be 4 races which will feature a Break. For each of these 4 races, each of 3 teams will select a rider (in secret) to be in the break. Therefore one team will miss out on the break each time.
3.3. The 3 person breakaway will then set off a set time interval before the main bunch.
  
 3.4. The team that will miss the breakaway will be decided randomly. But each team will only miss out on 1 breakaway during the season.
4. Designatedsprinter/designatedclimber
4.1. For each race (other than the TTT), each team will be able to designate either a sprinter, or a climber. They must declare their designated sprinter/climber publicly at least 30 minutes before the start of the stage.
4.2. If a designated sprinter is chosen, then any intermediate sprint points that that rider acquires are doubled. And any finish line points (on stages that are classified as sprint finishes) that that rider acquires are increased by 20%.
4.3. If a designated climber is chosen, then any KOM points that that rider acquires are doubled. And any finish line points (on stages that are classified as hill top finishes) that that rider acquires are increased by 20%.
4.4. A rider may only be a designated sprinter or designated climber once. (For example, if a rider is the designated climber in week 1, they will not be allowed to be the designated climber or the designated sprinter for any other races).
5. THEPOINTSSYSTEMEXPLAINED
5.1. Each week there will be a points pot, all of which will be distributed out across three different categories (Finishing position, Intermediate sprints, KOM points). The categories are explained below. Each different category will have a % of the points pot allocated to it, which may be different each week.
For example, a race that had points solely for finishing position would have 100% of the points for the ‘Finishing Position’ category, and 0% for the other categories. A race that was all about intermediate sprinting might have 70% of the points pot allocated to the ‘intermediate sprints’ category, and 30% allocated to finishing position.
5.2. The prologue will have 500 points available in the points pot. Weeks 1 through to and including week 5 will have 1,000 points in the pot. And the final week will have 2,000 points.
5.3. In addition to the above (Ie outside of the points pots), further points are available for the Orange Jersey, most aggressive rider, and race reports (see below).
6. Category1:Finishingposition
     
 6.1. These points will be awarded to the riders on a % of the category pot basis (Ie. a % of the allocated Finishing Position %) . Whereby the higher the finishing position, the higher % of the pot you receive. See Schedule 3 for the percentage distributions.
6.2. As an example, if you come first you would get 10% of the pot. But if you came 21st you would get 2.1% of the pot.
6.3. However, if there are fewer than 40 riders racing, then not all the pot will be distributed out (as the lower placings will now not be filled), leaving a ‘remainder’ amount.
6.4. This ‘remainder’ (whatever it may be) will be reallocated to the riders equally amongst all riders that raced.
7. Category 2: KOM points
7.1. These may be awarded on certain races but not necessarily every race.
7.2. The points allocated will be determined on a race by race basis, as it will depend on the severity of the climb it relates to
8. Category 3: Intermediate Sprint points
8.1. The points allocated will be determined on a race by race basis.
8.2. Details of the intermediate sprints and KOM will be made clear in advance of the relevant race.
9. Most aggressive rider
9.1. Twenty points available each week to the most aggressive rider, as chosen by agreement by team leaders. (Things that might win you this award are activities such as going on a wild hopeless attack that is doomed to fail, and inevitably does fail.)
9.2. Only one MAR per night
9.3. Most aggressive rider over the course of the season will be awarded 100 points after the conclusion of the final week’s race.
10. Race reports
Twenty points will be awarded to the team of any rider that submits a race report after each week, that is deemed to be ‘up to snuff’ by agreement of the team captains.
    
 11. Orange jersey competition
11.1. Points available at the end of each week (starting after the conclusion of Week 1 - Ie. No points awarded after the Prologue) for rider’s position in Orange jersey leaderboard. A rider must have finished a race to be awarded any points.
11.2. Points available at the end of the season for the top 10 in the orange jersey leaderboard. 11.3. See Schedules 1 and 2 below for the points available.
11.4. The Orange Jersey leaderboard tracks overall time over each stage. (Otherwise known as General Classification.)
11.5. If a rider does not start, or does not finish, a stage, then their time taken will be the greater of (i) 5 minutes slower than the fastest finisher for that stage, and (ii) 30 seconds slower than the slowest finisher on that stage.
Orange passes
11.6. Each team will have 6 Orange Passes. A team can use an Orange Pass on any given stage for any rider that has either:
(i) not started that stage, or
(ii) has had a technical problem meaning that they could not complete that stage.
11.7. Where an Orange Pass is used, instead of calculating their time as per 11.5 above that rider will receive the slower of:
(i) the same time as the second slowest rider in their team; and
(ii) 90s slower than the rider who finishes first in that race.
11.8. If a rider uses an Orange Pass, they will not receive any Orange Jeresy points for that week, except for the final week, in which case that rider will receive points for their final finishing position (if they so qualify)..
12. Quibbling
Any quibbling of any nature by any of the riders or wider team members may result in a fine up to €1,500 and/or a rider being given last place for the race or stage to which the quibbling relates.
13. Director’s decision
A race director’s decision, no matter how erratic, inconsistent or unlawful, shall be binding, final and shall not be quibbled with. In case of any quibbling, see Rule 12. 
  ''')

    with tab42:
        st.subheader('Lego pours millions into doomed vanity project')
        st.write('''Sunday 5th November 2023 Legoland

For years the top team at Lego have been considering a move into the world of pro cycling. And this year, they have finally taken the plunge, emptied their pockets, gathered up the scattered pennies, and spent them on a pro e-cycling outfit. 

To do so they have teamed up with Boots. It feels like an odd combination, (and a few stories have circulated about how the CFO at Boots was taken out for a lobster lunch by a few Lego directors. It transpired the CFO was on the way out of the company anyway, got totally pissed, and ended up signing up to the agreement muttering “fuck it all” under his breath). 

Despite the coming together of these two behemoths, Lego Boots have been struggling to raise the cash to entice one rider in particular: Bill Smith.  According to reliable sources, Bill was demanding an extortionate salary, and therefore a third title sponsor had to be found at short notice. Some big names were interested, but time was cripplingly short, and the best the Lego Boots partnership could do was P&O ferries, who gladly provided the extra cash to secure the services of the hardened professional Bill Smith,(despite P&O knowing that P&O was bound to be left off the title name when used by Adam Bylthe on GCN commentary). 

As part of Bill’s contract, he had demanded that he would need a full team to support him in his GC bid, and insisted it would be “all in for Bill”.  So what was needed was domestiques willing to turn themselves inside out, upside down, and over the hill and far away for Bill, week in, week out. 

To do this, Lego Boots immediately crawled all over the decaying carcass of what was previously Routes Coffee TZA Draconi. And like a hungry vulture, they picked up nearly the whole squad that had previously been punching holes in walls for the ‘Al brothers’.  

With contracts expired, and the wise heads of Al and Al now out the picture, Lizzy, Nic, Tom and Tom were happy to sign up to Lego Boots and look for new opportunities of their own. (Little did they know Bill Smith had his own designs as to what they would be allowed to do on the road.)

With a dwindling purse, Lego Boots still had spots in their rooster to fill. Wetbeak and Monk, a couple of older riders well past their peak, were brought on board. Largely because no other team would take them, and Lego Boots is paying them peanuts. 

And the final spot went to Alex Hadcock. A talented climber, but a neo-pro and totally untested in the heated world of Walrus e-cycling. Some say this deal was a gamble, Lego Boots would say this deal was cheap as chips. 

Only time will tell how delicious those chips will be.''')

    with tab43:
        st.subheader('Amazon Beaconsfield Services')
        st.write('')

    with tab44:
        st.subheader('FOR IMMEDIATE RELEASE')
        st.write('''London, UK, November 4, 2023

Tesla and Thames Water Unite in Cycling Endeavor for the Greater Good

In a groundbreaking collaboration that defies expectations, Tesla, the pioneering electric car company, and Thames Water, the UK's leading water utility provider, have joined forces to propel the world of professional cycling into a new era.

The partnership was officially unveiled at a press conference attended by Elon Musk, the visionary CEO of Tesla, and Alastair Cochran, the forward-thinking CEO of Thames Water. Their announcement marks a significant moment in the history of cycling as the two seemingly unrelated giants pool their resources to launch a brand-new cycling team: Team Tesla Thames Water.

This unique partnership is set to bring a fresh perspective to the world of professional cycling, as Tesla's commitment to clean energy and innovation marries Thames Water's dedication to responsible water management. The unlikely union underscores the shared ambition to conquer the 2023 Zwift Championships, one of the most prestigious events in the cycling calendar.

In a surprising twist, the newly formed Team Tesla Thames Water has signed Rich Tyler, a rising star in the cycling world, to bolster their roster. Known for his remarkable sprinting skills and podium finishes, Tyler is poised to be a key asset in the team's pursuit of championship glory.

However, the team's lineup isn't complete without the enigmatic Edwin Smith, a mercurial talent whose career has spanned decades. The question on everyone's mind is whether Smith, now considered "long in the tooth" by some, still possesses the prowess to contribute to the team's quest for victory. His inclusion adds an element of intrigue to the team's composition.

When asked about the partnership, Elon Musk stated, "Cycling is more than just sport; it's a symbol of human potential and the power of sustainable transportation. Our partnership with Thames Water aims to underscore the importance of preserving our planet's resources, just as we do with electric vehicles. Team Tesla Thames Water is not just a cycling team; it's a testament to our shared commitment to a greener future."

Alastair Cochran, CEO of Thames Water, added, "As stewards of water, we understand the significance of responsible resource management. Joining forces with Tesla is a declaration that our actions speak louder than words. We're excited about the journey ahead, both on the road and in our shared mission to champion sustainability."

The team's distinctive blue and green jerseys symbolize the fusion of electric energy and water, while reflecting their dedication to clean, renewable energy sources. It's a visual reminder of their commitment to a more sustainable future.

Team Tesla Thames Water also announced an exciting partnership with Scott bikes and Volvo cars to elevate their on-road and off-road experiences. Sunweb remains a valued partner, ensuring the team's continued growth and success.

With the 2023 Zwift Championships on the horizon, Team Tesla Thames Water's journey promises to be a thrilling blend of competition and commitment to the environment, as they ride towards a future where sport and sustainability go hand in hand.''')

    with tab45:
        st.subheader('The e-Pedlars Lancet 7/11/2023')
        st.write('''By Penny Farthing

In a surprising twist in the world of SW eracing, the remnants of the infamous Evil Greens have found a new lease of life through a partnership between AstraZeneca and Trailfinders. This unexpected alliance was driven by a unique vision: AstraZeneca's aspiration to invest more in Watopian diseases whilst supporting washed up Greens' bruiser, Teo Lopez.

Now captain Lopez had endured a challenging summer, having been attacked by a swarm of extremely venomous Watopian feather beetles, on a late season training ride. His personal journey resonated with AstraZeneca's mission, and the addition of Trailfinders was perfect for this new, intrepid, outfit.

Vice Captain Dickie Tyler will play a crucial role in maintaining team morale and optimising strategy, whilst seasoned veterans, Rob Friend and Duncan Singh, bring a wealth of experience and camaraderie. Duncan Singh aptly remarked, "We might be 'wily old heads,' but we still have a few tricks up our sleeves."

The team welcoms fresh faces, including Davyd Greenish, who excitedly declared, "I'm thrilled to be part of this team!" Beth Wilson and Nick Foley add youthful enthusiasm and unpredictability to the squad.

This partnership not only breathes new life into the Greens but also signifies a unique fusion of goals – AstraZeneca's commitment to Watopian diseases and the resilience and determination of the once-feared Evil Greens. It's a story of renewal and hope, anchored by the experienced, the determined, and the newcomers, all propelled forward by a shared mission to make a meaningful impact in the e-racing world.''')