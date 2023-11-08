import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import sys

sys.path.append('/Users/achie188/Library/CloudStorage/GitHub/Personal/SW_eracing')


from inputs.pull_zwift import pull_zwift
from inputs.pull_gsheet import pull_gsheet

#Stage_ids
stage1 = '3921745'

#Events
prologue = pull_gsheet("Prologue")
t1 = pull_zwift(stage1)


interval=5 * 1000





# Set up Streamlit app
st.set_page_config(
    page_title="SW E-Racing",
    layout="wide"
)

#st_autorefresh(interval, limit=1000)

st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)

st.subheader("Welcome to the Sexy Walrus E-Racing Series 2023! 👋")

st.write("The below shows the results and current standings of the Sexy Walrus E-Racing Series.")

tab1, tab2, tab3 = st.tabs(["Current Race", "Championship", "All Results"])


with tab1:
    if t1.empty:
        st.write("Race not started yet, no data. Please be patient.")
    else:
        st.dataframe(t1, height=2000, hide_index=True)

with tab2:
    tab11, tab12, tab13, tab14, tab15, tab16 = st.tabs("Prologue", "Stage 1", "Stage 2", "Stage 3", "Stage 4", "Stage 5")

    with tab11:
        st.subheader('Prologue Results')

        st.dataframe(prologue, hide_index=True)