
import streamlit as st
import requests
import pandas as pd
import datetime
import json
import yfinance as yf
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# CONFIG STREAMLIT
st.set_page_config(page_title="📈 Bitcoin Bull Run Tracker", layout="centered")
st.title("📈 Bitcoin Bull Run Tracker")
st.caption("Suivi de 6 indicateurs pour détecter un bull run Bitcoin")

# ----------------------------
# 1. PRIX BTC VS ATH
# ----------------------------
try:
    btc_data = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd").json()
    btc_price = btc_data["bitcoin"]["usd"]
except:
    btc_price = 100000  # valeur estimée si échec API
    st.warning("⚠️ CoinGecko API échouée — valeur estimée utilisée")

ath_estime = 109000
st.subheader("1. 🟦 Prix BTC vs ATH")
st.metric("Prix BTC actuel", f"${btc_price:,.0f}")
st.text(f"ATH estimé (2025): ${ath_estime:,}")

# ----------------------------
# 2. DOMINANCE BTC
# ----------------------------
try:
    dominance_data = requests.get("https://api.alternative.me/v2/global/").json()
    dominance = float(dominance_data["data"]["bitcoin_dominance"])
except:
    dominance = 48.5
    st.warning("⚠️ API dominance échouée — estimation utilisée")

st.subheader("2. 🟩 Dominance BTC (%)")
st.metric("BTC Dominance", f"{dominance:.2f}%")

# ----------------------------
# 3. MOYENNE MOBILE 200 SEMAINES
# ----------------------------
st.subheader("3. 🟧 Moyenne mobile 200 semaines")
try:
    btc_hist = yf.download("BTC-USD", period="5y", interval="1wk")
    last_price = btc_hist["Close"][-1]
    ma_200w = btc_hist["Close"].rolling(window=200).mean().dropna()[-1]
    st.metric("Prix hebdo", f"${last_price:,.0f}")
    st.metric("Moyenne 200 semaines", f"${ma_200w:,.0f}")
except:
    st.warning("⚠️ Données Yahoo Finance échouées ou incomplètes, estimations utilisées")
    last_price = btc_price  # fallback
    ma_200w = 86494
    st.metric("Prix hebdo", f"${last_price:,.0f}")
    st.metric("Moyenne 200 semaines", f"${ma_200w:,.0f}")

# ----------------------------
# 4. HASHRATE (SIMULÉ POUR EXEMPLE)
# ----------------------------
st.subheader("4. 🟨 Hashrate (approximation)")
st.text("Hashrate considéré haussier pour cet exemple.")

# ----------------------------
# 5. FLUX ETF (GOOGLE SHEETS)
# ----------------------------
st.subheader("5. 🟥 Flux net ETF (Google Sheets)")

try:
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    info = json.loads(st.secrets["GOOGLE_KEY_JSON"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(info, scope)
    client = gspread.authorize(creds)
    sheet = client.open("ETF_Flows_BTC").sheet1
    df = pd.DataFrame(sheet.get_all_records())
    total_etf_flow = df["Net Flow USD"].sum()
    st.metric("Flux net ETF", f"${total_etf_flow/1e6:.1f}M")
except Exception as e:
    st.warning("⚠️ Échec lecture Google Sheets — estimation utilisée")
    total_etf_flow = 50000000
    st.metric("Flux estimé", "$50.0M")

# ----------------------------
# 6. GOOGLE TRENDS (SIMULÉ POUR EXEMPLE)
# ----------------------------
st.subheader("6. 🟪 Tendance Google 'Bitcoin'")
try:
    trend_score = 68  # simulation
    st.metric("Indice de tendance", trend_score)
except:
    st.warning("⚠️ Erreur chargement Google Trends")
    trend_score = 0
    st.metric("Indice de tendance", "N/A")

# ----------------------------
# SCORE FINAL
# ----------------------------
st.markdown("---")
score = 0
if btc_price >= ath_estime * 0.95: score += 1
if dominance >= 50: score += 1
if last_price >= ma_200w: score += 1
if total_etf_flow > 0: score += 1
if trend_score > 60: score += 1
score_text = f"{score}/6"

st.subheader("🔎 Score Bull Run")
st.metric("Indicateurs haussiers", score_text)
if score >= 4:
    st.success("🟢 Signal haussier en formation")
elif score == 3:
    st.warning("🟡 Tendance haussière en formation")
else:
    st.info("🔵 Pas encore de signal fort")
