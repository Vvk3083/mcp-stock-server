# Stock Analysis MCP Server

A comprehensive FastAPI-based stock analysis server that provides real-time stock data, technical indicators, and financial metrics using Yahoo Finance data.

## Features

- 📈 **Real-time Stock Prices** - Get current stock prices
- 📊 **Technical Indicators** - RSI, MACD, Bollinger Bands, Moving Averages
- 📋 **Comprehensive Stock Data** - Price, volume, high/low, open/close
- 📚 **Historical Data** - Flexible time periods for analysis
- 🏢 **Company Information** - Sector, industry, market cap, P/E ratio
- 🔍 **Health Monitoring** - Server health check endpoint
- 📖 **Auto-generated API Docs** - Interactive Swagger/OpenAPI documentation

## API Endpoints

| Endpoint | Description | Parameters |
|----------|-------------|------------|
| `/` | Server information and available endpoints | None |
| `/health` | Health check endpoint | None |
| `/current_price` | Get current stock price | `symbol` |
| `/stock_data` | Comprehensive stock data | `symbol` |
| `/moving_average` | Moving average calculation | `symbol`, `window` |
| `/technical_indicators` | Technical analysis indicators | `symbol` |
| `/historical_data` | Historical price data | `symbol`, `period` |
| `/stock_info` | Company information | `symbol` |

## Installation

1. **Clone or download the project files**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server:**
   ```bash
   python run_server.py
   ```
   
   Or alternatively:
   ```bash
   python main.py
   ```

## Usage

### Starting the Server

The server will start on `http://localhost:8765`

- **API Documentation**: http://localhost:8765/docs
- **Interactive Docs**: http://localhost:8765/redoc
- **Health Check**: http://localhost:8765/health

### Example API Calls

```bash
# Get current price
curl "http://localhost:8765/current_price?symbol=AAPL"

# Get comprehensive stock data
curl "http://localhost:8765/stock_data?symbol=TSLA"

# Get technical indicators
curl "http://localhost:8765/technical_indicators?symbol=MSFT"

# Get historical data
curl "http://localhost:8765/historical_data?symbol=GOOGL&period=1y"

# Get company information
curl "http://localhost:8765/stock_info?symbol=AMZN"
```

### MCP Integration

This server is designed to work with Model Context Protocol (MCP). The `mcp.txt` file contains the configuration for integrating with MCP-compatible tools.

## Technical Indicators

The server provides the following technical indicators:

- **Simple Moving Averages (SMA)**: 20-day, 50-day, 200-day
- **Relative Strength Index (RSI)**: 14-period RSI
- **MACD**: 12/26/9 MACD with signal line and histogram
- **Bollinger Bands**: 20-period with 2 standard deviations

## Error Handling

The server includes comprehensive error handling:
- Invalid stock symbols return 404 errors
- Network issues return 500 errors
- All errors include descriptive messages

## Dependencies

- **FastAPI**: Modern web framework
- **Uvicorn**: ASGI server
- **yfinance**: Yahoo Finance data
- **pandas**: Data manipulation
- **numpy**: Numerical computations

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port in `main.py` or `run_server.py`
2. **Installation errors**: Try installing packages individually
3. **No data returned**: Check if the stock symbol is valid

### Windows Users

If you encounter compilation issues with pandas/numpy:
1. Install Microsoft Visual C++ Build Tools
2. Or use pre-compiled wheels: `pip install --only-binary=all pandas numpy`

## License

This project is open source and available under the MIT License. 