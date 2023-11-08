import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
import streamlit as st
import time
import os
import sys


SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

skey = st.secrets["gsheet_credentials"]
credentials = Credentials.from_service_account_info(
    skey,
    scopes=SCOPES,
)
gc = gspread.authorize(credentials)
sh =  gc.open("SW_E-Racing_23")

def pull_gsheet(sheet):
    wks = sh.worksheet(sheet)
    df = pd.DataFrame(wks.get_all_records())

    return df
