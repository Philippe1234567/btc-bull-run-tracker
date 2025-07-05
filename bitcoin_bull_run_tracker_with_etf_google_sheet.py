
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# CONFIGURATION GOOGLE SHEETS
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name("etf-writer-key.json", scope)
client = gspread.authorize(creds)

# Accès au Google Sheet
sheet = client.open("ETF_Flows_BTC").sheet1
records = sheet.get_all_records()
df = pd.DataFrame(records)

# Calcul total cumulé des flux ETF
total_etf_flow = df["Montant"].sum()

# STREAMLIT APP
st.title("📈 Bitcoin Bull Run Tracker")
st.header("5. 🟥 Flux net ETF (automatisé via Google Sheet)")

if total_etf_flow >= 0:
    st.metric("Flux net ETF", f"${total_etf_flow/1e6:.1f}M", delta="+")
else:
    st.metric("Flux net ETF", f"${total_etf_flow/1e6:.1f}M", delta="-")

st.caption("Source : Google Sheets partagé avec service account")
