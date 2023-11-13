import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe
import streamlit as st


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


def pull_ids(sheet1, sheet2, sheet3, sheet4):
    wks = sh.worksheet(sheet1)
    df1 = pd.DataFrame(wks.get_all_records())

    wks = sh.worksheet(sheet2)
    df2 = pd.DataFrame(wks.get_all_records())

    wks = sh.worksheet(sheet3)
    df3 = pd.DataFrame(wks.get_all_records())

    wks = sh.worksheet(sheet4)
    df4 = pd.DataFrame(wks.get_all_records())

    return df1, df2, df3, df4


def pull_gsheet(sheet):
    wks = sh.worksheet(sheet)
    df = pd.DataFrame(wks.get_all_records())

    return df


def push_gsheet(df, sheet):
    wks = sh.worksheet(sheet)

    set_with_dataframe(wks, df, row=1, col=1, include_index=False)


    