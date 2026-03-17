import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

st.title("AI Trade Finder")

ticker = st.text_input("Enter a stock ticker:")

if ticker:
    stock = yf.download(ticker, period="3mo")
    stock.columns = stock.columns.get_level_values(0)

    if not stock.empty:
        current_price = float(stock["Close"].iloc[-1])
        high_3m = float(stock["High"].max())
        low_3m = float(stock["Low"].min())

        stock["SMA20"] = stock["Close"].rolling(20).mean()
        stock["SMA50"] = stock["Close"].rolling(50).mean()

        sma20 = float(stock["SMA20"].iloc[-1]) if pd.notna(stock["SMA20"].iloc[-1]) else None
        sma50 = float(stock["SMA50"].iloc[-1]) if pd.notna(stock["SMA50"].iloc[-1]) else None

        distance_from_high = ((high_3m - current_price) / high_3m) * 100

        fig = go.Figure()

        fig.add_trace(go.Candlestick(
            x=stock.index,
            open=stock["Open"],
            high=stock["High"],
            low=stock["Low"],
            close=stock["Close"],
            name="Price"
        ))

        fig.add_trace(go.Scatter(
            x=stock.index,
            y=stock["SMA20"],
            mode="lines",
            name="SMA20"
        ))

        fig.add_trace(go.Scatter(
            x=stock.index,
            y=stock["SMA50"],
            mode="lines",
            name="SMA50"
        ))

        fig.update_layout(
            title=f"{ticker.upper()} Price Chart",
            xaxis_title="Date",
            yaxis_title="Price",
            xaxis_rangeslider_visible=False
        )

        st.plotly_chart(fig, use_container_width=True)

        summary_data = {
            "Metric": [
                "Current Price",
                "3-Month High",
                "3-Month Low",
                "Distance From 3M High (%)",
                "SMA20",
                "SMA50"
            ],
            "Value": [
                round(current_price, 2),
                round(high_3m, 2),
                round(low_3m, 2),
                round(distance_from_high, 2),
                round(sma20, 2) if sma20 is not None else "N/A",
                round(sma50, 2) if sma50 is not None else "N/A"
            ]
        }

        summary_df = pd.DataFrame(summary_data)

        st.subheader("Technical Summary")
        st.table(summary_df)

    else:
        st.error("No data found for this ticker.")