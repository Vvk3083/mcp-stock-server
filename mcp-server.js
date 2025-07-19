import 'dotenv/config'; // Shorter ES module import for dotenv (auto-loads .env)
import { Server } from '@modelcontextprotocol/sdk';
import axios from 'axios';

const server = new Server('Stock Analysis MCP Server');

// Tool: Get current price of a stock
server.tool('currentPrice', async ({ symbol }) => {
  const response = await axios.get(
    'https://www.alphavantage.co/query',
    {
      params: {
        function: 'GLOBAL_QUOTE',
        symbol,
        apikey: process.env.ALPHA_VANTAGE_KEY
      }
    }
  );

  const price = response.data['Global Quote']?.['05. price'];

  return {
    symbol,
    price
  };
});

server.listen();
