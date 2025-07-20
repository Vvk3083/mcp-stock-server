from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

app = FastAPI(
    title="Stock Analysis MCP Server",
    description="A comprehensive stock analysis server with technical indicators",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StockData(BaseModel):
    symbol: str
    current_price: float
    change: float
    change_percent: float
    volume: int
    high: float
    low: float
    open_price: float
    previous_close: float

class TechnicalIndicators(BaseModel):
    symbol: str
    sma_20: float
    sma_50: float
    sma_200: float
    rsi: float
    macd: float
    macd_signal: float
    macd_histogram: float
    bollinger_upper: float
    bollinger_lower: float
    bollinger_middle: float

@app.get("/")
def root():
    """Root endpoint with server information"""
    return {
        "message": "Stock Analysis MCP Server",
        "version": "1.0.0",
        "endpoints": [
            "/current_price",
            "/stock_data", 
            "/moving_average",
            "/technical_indicators",
            "/historical_data",
            "/health"
        ]
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/current_price")
def current_price(symbol: str):
    """Get current stock price using Yahoo Finance"""
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        if data.empty:
            raise HTTPException(status_code=404, detail=f"No data found for symbol {symbol}")
        
        price = data['Close'].iloc[-1]
        return {"symbol": symbol, "current_price": float(price)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")

@app.get("/stock_data")
def stock_data(symbol: str):
    """Get comprehensive stock data including price, volume, and daily stats"""
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="5d")
        if data.empty:
            raise HTTPException(status_code=404, detail=f"No data found for symbol {symbol}")
        
        latest = data.iloc[-1]
        previous = data.iloc[-2] if len(data) > 1 else latest
        
        change = latest['Close'] - previous['Close']
        change_percent = (change / previous['Close']) * 100
        
        return StockData(
            symbol=symbol,
            current_price=float(latest['Close']),
            change=float(change),
            change_percent=float(change_percent),
            volume=int(latest['Volume']),
            high=float(latest['High']),
            low=float(latest['Low']),
            open_price=float(latest['Open']),
            previous_close=float(previous['Close'])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")

@app.get("/moving_average")
def moving_average(symbol: str, window: int = 20):
    """Get moving average for a stock"""
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1y")
        if data.empty:
            raise HTTPException(status_code=404, detail=f"No data found for symbol {symbol}")
        
        ma = data['Close'].rolling(window=window).mean().iloc[-1]
        return {"symbol": symbol, "moving_average": float(ma), "window": window}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")

@app.get("/technical_indicators")
def technical_indicators(symbol: str):
    """Get comprehensive technical indicators for a stock"""
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1y")
        if data.empty:
            raise HTTPException(status_code=404, detail=f"No data found for symbol {symbol}")
        
        # Calculate Simple Moving Averages
        sma_20 = data['Close'].rolling(window=20).mean().iloc[-1]
        sma_50 = data['Close'].rolling(window=50).mean().iloc[-1]
        sma_200 = data['Close'].rolling(window=200).mean().iloc[-1]
        
        # Calculate RSI
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs)).iloc[-1]
        
        # Calculate MACD
        exp1 = data['Close'].ewm(span=12).mean()
        exp2 = data['Close'].ewm(span=26).mean()
        macd = exp1 - exp2
        macd_signal = macd.ewm(span=9).mean()
        macd_histogram = macd - macd_signal
        
        # Calculate Bollinger Bands
        bb_middle = data['Close'].rolling(window=20).mean()
        bb_std = data['Close'].rolling(window=20).std()
        bb_upper = bb_middle + (bb_std * 2)
        bb_lower = bb_middle - (bb_std * 2)
        
        return TechnicalIndicators(
            symbol=symbol,
            sma_20=float(sma_20),
            sma_50=float(sma_50),
            sma_200=float(sma_200),
            rsi=float(rsi),
            macd=float(macd.iloc[-1]),
            macd_signal=float(macd_signal.iloc[-1]),
            macd_histogram=float(macd_histogram.iloc[-1]),
            bollinger_upper=float(bb_upper.iloc[-1]),
            bollinger_lower=float(bb_lower.iloc[-1]),
            bollinger_middle=float(bb_middle.iloc[-1])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating indicators: {str(e)}")

@app.get("/historical_data")
def historical_data(symbol: str, period: str = "1y"):
    """Get historical stock data"""
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period)
        if data.empty:
            raise HTTPException(status_code=404, detail=f"No data found for symbol {symbol}")
        
        # Convert to list of dictionaries for JSON serialization
        historical = []
        for date, row in data.iterrows():
            historical.append({
                "date": date.strftime("%Y-%m-%d"),
                "open": float(row['Open']),
                "high": float(row['High']),
                "low": float(row['Low']),
                "close": float(row['Close']),
                "volume": int(row['Volume'])
            })
        
        return {
            "symbol": symbol,
            "period": period,
            "data": historical
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching historical data: {str(e)}")

@app.get("/stock_info")
def stock_info(symbol: str):
    """Get basic stock information"""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        return {
            "symbol": symbol,
            "name": info.get('longName', 'N/A'),
            "sector": info.get('sector', 'N/A'),
            "industry": info.get('industry', 'N/A'),
            "market_cap": info.get('marketCap', 'N/A'),
            "pe_ratio": info.get('trailingPE', 'N/A'),
            "dividend_yield": info.get('dividendYield', 'N/A'),
            "beta": info.get('beta', 'N/A'),
            "fifty_two_week_high": info.get('fiftyTwoWeekHigh', 'N/A'),
            "fifty_two_week_low": info.get('fiftyTwoWeekLow', 'N/A')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stock info: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8765)
