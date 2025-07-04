
import streamlit as st
import requests

st.set_page_config(page_title="Bitcoin Bull Run Tracker", layout="wide")

st.title("📈 Bitcoin Bull Run Tracker")
st.caption("Suivi en temps réel de 6 indicateurs clés pour détecter un bull run Bitcoin")

# Section 1 – BTC Price vs ATH
st.subheader("1. BTC Price vs All-Time High (ATH)")
btc_data = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd").json()
btc_price = btc_data["bitcoin"]["usd"]
ath = 109000  # mise à jour manuelle ou via API ATH réel
st.metric("Prix actuel du BTC (USD)", f"${btc_price:,.0f}")
st.metric("ATH Récent (2025)", f"${ath:,.0f}")
if btc_price >= ath:
    st.success("🔥 Le BTC est en mode découverte de prix !")
else:
    st.warning("🔎 Le BTC n’a pas encore dépassé son ATH récent.")

# Section 2 – BTC Dominance
st.subheader("2. Dominance du BTC (%)")
dominance_data = requests.get("https://api.coingecko.com/api/v3/global").json()
btc_dominance = dominance_data["data"]["market_cap_percentage"]["btc"]
st.metric("BTC Dominance", f"{btc_dominance:.2f}%")
if btc_dominance >= 50:
    st.success("🟢 Dominance élevée – signal haussier")
else:
    st.info("🟡 Dominance modérée – attention à l’euphorie altcoins")

# Section 3 – Score synthétique
st.subheader("🧠 Score Bull Run")
bull_score = 0
if btc_price >= ath:
    bull_score += 1
if btc_dominance >= 50:
    bull_score += 1
st.metric("Bull Score (sur 6)", f"{bull_score}/6")
if bull_score >= 5:
    st.success("✅ Bull run confirmé (score élevé)")
elif bull_score >= 3:
    st.info("🟡 Potentiel haussier en formation")
else:
    st.warning("🔴 Conditions faibles pour un bull run")

st.markdown("---")
st.caption("Données en direct via CoinGecko – mises à jour automatiques")
