from fastapi import FastAPI
import yfinance as yf
import pandas as pd

app = FastAPI()

@app.get("/current_price")
def current_price(symbol: str):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1d")
    if data.empty:
        return {"error": "No data found"}
    price = data['Close'].iloc[-1]
    return {"symbol": symbol, "current_price": float(price)}

@app.get("/moving_average")
def moving_average(symbol: str, window: int = 20):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1y")
    if data.empty:
        return {"error": "No data found"}
    ma = data['Close'].rolling(window=window).mean().iloc[-1]
    return {"symbol": symbol, "moving_average": float(ma), "window": window}
