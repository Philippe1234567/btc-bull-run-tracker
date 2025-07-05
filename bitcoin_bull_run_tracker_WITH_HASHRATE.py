
import streamlit as st
import requests
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Bitcoin Bull Run Tracker", layout="wide")
st.title("📈 Bitcoin Bull Run Tracker")
st.caption("Suivi de 6 indicateurs pour détecter un bull run Bitcoin")

# ---------- 1. BTC vs ATH ----------
st.subheader("1. 🟦 Prix BTC vs ATH")
try:
    btc_data = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd").json()
    btc_price = btc_data.get("bitcoin", {}).get("usd", None)
    if btc_price is None:
        raise ValueError("Prix introuvable")
except Exception:
    btc_price = 100000
    st.warning("⚠️ Prix BTC estimé à $100,000 (CoinGecko API échouée)")
ath = 109000
st.metric("Prix BTC actuel", f"${btc_price:,.0f}")
st.metric("ATH estimé (2025)", f"${ath:,.0f}")
price_signal = btc_price >= ath

# ---------- 2. Dominance BTC ----------
st.subheader("2. 🟩 Dominance BTC (%)")
try:
    dom_data = requests.get("https://api.coingecko.com/api/v3/global").json()
    btc_dominance = dom_data["data"]["market_cap_percentage"]["btc"]
except Exception:
    btc_dominance = 48.5
    st.warning("⚠️ Dominance estimée à 48.5% (API échouée)")
st.metric("BTC Dominance", f"{btc_dominance:.2f}%")
dominance_signal = btc_dominance >= 50

# ---------- 3. Moyenne mobile 200 semaines ----------
st.subheader("3. 🟧 Moyenne mobile 200 semaines")
try:
    btc_yf = yf.download("BTC-USD", period="5y", interval="1wk")
    btc_yf["200W_MA"] = btc_yf["Close"].rolling(window=200).mean()
    last_price = btc_yf["Close"].iloc[-1]
    last_ma = btc_yf["200W_MA"].iloc[-1]
    if pd.isna(last_price) or pd.isna(last_ma):
        raise ValueError("NaN dans les données")
except Exception:
    last_price = btc_price
    last_ma = btc_price * 0.8
    st.warning("⚠️ Données Yahoo Finance échouées ou incomplètes, estimations utilisées")
st.metric("Prix hebdo", f"${last_price:,.0f}")
st.metric("Moyenne 200 semaines", f"${last_ma:,.0f}")
ma_signal = last_price > last_ma

# ---------- 4. Hashrate réel ----------
st.subheader("4. 🟨 Hashrate réel")
try:
    url = "https://api.blockchain.info/charts/hash-rate?timespan=30days&format=json"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data['values'])
    df['x'] = pd.to_datetime(df['x'], unit='s')
    df = df.rename(columns={'x': 'date', 'y': 'hashrate'})
    latest_hashrate = df['hashrate'].iloc[-1]
    mean_hashrate = df['hashrate'].mean()
    hashrate_signal = latest_hashrate > mean_hashrate
    st.metric("Hashrate actuel", f"{latest_hashrate:.0f}")
    st.metric("Hashrate moyen", f"{mean_hashrate:.0f}")
except Exception:
    hashrate_signal = True
    st.warning("⚠️ Hashrate réel indisponible — valeur estimée utilisée")
    st.metric("Hashrate estimé", "400M")
    st.metric("Hashrate moyen estimé", "350M")

# ---------- 5. Flux ETF (manuel) ----------
st.subheader("5. 🟥 Flux net ETF")
etf_net_flow = 50000000  # valeur fictive
st.metric("Flux estimé", f"${etf_net_flow/1e6:.1f}M")
etf_signal = etf_net_flow > 0

# ---------- 6. Google Trends (manuel) ----------
st.subheader("6. 🟪 Tendance Google 'Bitcoin'")
trend_score = 68
st.metric("Indice de tendance", trend_score)
trends_signal = trend_score > 70

# ---------- Score final ----------
bull_score = sum([
    price_signal,
    dominance_signal,
    ma_signal,
    hashrate_signal,
    etf_signal,
    trends_signal
])
st.subheader("🔎 Score Bull Run")
st.metric("Indicateurs haussiers", f"{bull_score}/6")
if bull_score >= 5:
    st.success("✅ Bull run confirmé !")
elif bull_score >= 3:
    st.info("🟡 Tendance haussière en formation")
else:
    st.warning("🔴 Pas encore de bull run détecté")

st.caption("Certaines données sont simulées ou à compléter avec API.")
