
import streamlit as st
import requests
import datetime
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Bitcoin Bull Run Tracker", layout="wide")
st.title("📈 Bitcoin Bull Run Tracker")
st.caption("Suivi des 6 indicateurs clés pour détecter un bull run Bitcoin")

# 1. Prix BTC vs ATH
st.subheader("1. 🟦 Prix BTC vs ATH")

try:
    btc_data = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd").json()
    btc_price = btc_data.get("bitcoin", {}).get("usd", None)
    if btc_price is None:
        raise ValueError("BTC price not available")
except Exception as e:
    st.error("❌ Erreur lors de la récupération du prix BTC via CoinGecko.")
    btc_price = 100000  # valeur par défaut si erreur
    st.warning(f"Valeur estimée utilisée : ${btc_price:,}")

ath = 109000
st.metric("Prix actuel", f"${btc_price:,.0f}")
st.metric("ATH 2025", f"${ath:,.0f}")
price_signal = btc_price >= ath

# 2. Dominance BTC
st.subheader("2. 🟩 Dominance du BTC (%)")
try:
    dominance_data = requests.get("https://api.coingecko.com/api/v3/global").json()
    btc_dominance = dominance_data["data"]["market_cap_percentage"]["btc"]
except Exception as e:
    st.error("❌ Erreur lors de la récupération de la dominance BTC.")
    btc_dominance = 48.5  # valeur par défaut
    st.warning(f"Valeur estimée utilisée : {btc_dominance}%")
st.metric("BTC Dominance", f"{btc_dominance:.2f}%")
dominance_signal = btc_dominance >= 50

# 3. Moyenne mobile 200 semaines
st.subheader("3. 🟧 Moyenne mobile 200 semaines")
try:
    btc_yf = yf.download("BTC-USD", period="5y", interval="1wk")
    btc_yf["200W_MA"] = btc_yf["Close"].rolling(window=200).mean()
    last_price = btc_yf["Close"].iloc[-1]
    last_ma = btc_yf["200W_MA"].iloc[-1]
except Exception as e:
    st.error("❌ Erreur lors de l'accès aux données Yahoo Finance.")
    last_price = btc_price
    last_ma = btc_price * 0.8
st.metric("Dernier prix hebdo", f"${last_price:,.0f}")
st.metric("200W MA", f"${last_ma:,.0f}")
ma_signal = last_price > last_ma

# 4. Hashrate (approximatif avec placeholder)
st.subheader("4. 🟨 Hashrate estimé (placeholder)")
hashrate_signal = True
st.info("✅ Hashrate en tendance haussière (exemple)")

# 5. Flux ETF (placeholder manuel)
st.subheader("5. 🟥 Flux ETF net")
etf_net_inflow = 50000000  # $50M net inflow
st.metric("Flux net estimé", f"${etf_net_inflow/1e6:.1f}M")
etf_signal = etf_net_inflow > 0

# 6. Google Trends (manuel ou PyTrends)
st.subheader("6. 🟪 Intérêt Google Trends")
trends_score = 68  # Exemple à mettre à jour manuellement
st.metric("Indice de tendance", f"{trends_score}")
trends_signal = trends_score > 70

# Score total
bull_score = sum([price_signal, dominance_signal, ma_signal, hashrate_signal, etf_signal, trends_signal])
st.subheader("🔎 Score Bull Run")
st.metric("Indicateurs haussiers", f"{bull_score}/6")
if bull_score >= 5:
    st.success("✅ Bull run confirmé !")
elif bull_score >= 3:
    st.info("🟡 Tendance haussière en développement")
else:
    st.warning("🔴 Pas encore en bull run")

st.markdown("---")
st.caption("Certaines données sont placeholders – à automatiser pour version complète.")
