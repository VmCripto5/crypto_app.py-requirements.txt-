import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from datetime import datetime, timedelta

# Configuração da página Streamlit
st.set_page_config(page_title="Crypto Bot", layout="wide")
st.title("🤖 Crypto Bot - Monitor de Criptomoedas (CoinGecko)")

# Lista de criptomoedas principais
CRYPTO_IDS = {
    "Bitcoin": "bitcoin",
    "Ethereum": "ethereum",
    "Binance Coin": "binancecoin",
    "Cardano": "cardano",
    "Solana": "solana"
}

# Função para buscar dados históricos do CoinGecko
@st.cache_data(show_spinner=False)
def get_coingecko_data(crypto_id, vs_currency="usd", days=7):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart"
    params = {
        "vs_currency": vs_currency,
        "days": days
    }
    r = requests.get(url, params=params)
    if r.status_code != 200:
        return None
    data = r.json()
    prices = data.get("prices", [])
    if not prices:
        return None
    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)
    return df

def calculate_signals(df):
    if df is None or len(df) < 50:
        return None
    df["SMA20"] = df["price"].rolling(window=20).mean()
    df["SMA50"] = df["price"].rolling(window=50).mean()
    df["Signal"] = 0
    df.loc[df["SMA20"] > df["SMA50"], "Signal"] = 1
    df.loc[df["SMA20"] < df["SMA50"], "Signal"] = -1
    return df

def plot_crypto_chart(df, symbol):
    if df is None or len(df) < 50:
        return
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["price"],
        name="Preço",
        line=dict(color="white")
    ))
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["SMA20"],
        name="SMA 20",
        line=dict(color="blue")
    ))
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["SMA50"],
        name="SMA 50",
        line=dict(color="red")
    ))
    buy_signals = df[df["Signal"] == 1]
    sell_signals = df[df["Signal"] == -1]
    fig.add_trace(go.Scatter(
        x=buy_signals.index,
        y=buy_signals["price"],
        mode="markers",
        name="Comprar",
        marker=dict(color="green", size=10, symbol="triangle-up")
    ))
    fig.add_trace(go.Scatter(
        x=sell_signals.index,
        y=sell_signals["price"],
        mode="markers",
        name="Vender",
        marker=dict(color="red", size=10, symbol="triangle-down")
    ))
    fig.update_layout(
        title=f"{symbol} - Gráfico em Tempo Real (USD)",
        yaxis_title="Preço (USD)",
        xaxis_title="Data/Hora",
        template="plotly_dark"
    )
    return fig

def main():
    selected_crypto = st.sidebar.selectbox(
        "Selecione a Criptomoeda",
        list(CRYPTO_IDS.keys())
    )
    crypto_id = CRYPTO_IDS[selected_crypto]
    # Buscar 7 dias (CoinGecko retorna dados horários automaticamente)
    df = get_coingecko_data(crypto_id, vs_currency="usd", days=7)
    if df is not None and len(df) > 50:
        df = calculate_signals(df)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Preço Atual",
                f"${df['price'].iloc[-1]:.2f}",
                f"{df['price'].iloc[-1] - df['price'].iloc[-2]:.2f}"
            )
        with col2:
            st.metric(
                "Variação 7d",
                f"{(df['price'].iloc[-1] - df['price'].iloc[0]):.2f}"
            )
        with col3:
            last_signal = df['Signal'].iloc[-1]
            signal_text = "COMPRAR" if last_signal == 1 else "VENDER" if last_signal == -1 else "AGUARDAR"
            signal_color = "green" if last_signal == 1 else "red" if last_signal == -1 else "yellow"
            st.markdown(f"<h2 style='color: {signal_color};'>{signal_text}</h2>", unsafe_allow_html=True)
        fig = plot_crypto_chart(df, selected_crypto)
        st.plotly_chart(fig, use_container_width=True)
        st.subheader("Últimos Dados")
        st.dataframe(df.tail(10).style.format({
            'price': '${:.2f}',
            'SMA20': '${:.2f}',
            'SMA50': '${:.2f}'
        }))
    else:
        st.warning("Não foi possível obter dados suficientes para esta criptomoeda.")

if __name__ == "__main__":
    main() 
