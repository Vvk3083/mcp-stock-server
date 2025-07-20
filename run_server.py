#!/usr/bin/env python3
"""
Stock Analysis MCP Server Startup Script
"""

import uvicorn

if __name__ == "__main__":
    print("🚀 Starting Stock Analysis MCP Server...")
    print("📍 Server will be available at: http://localhost:8765")
    print("📚 API Documentation: http://localhost:8765/docs")
    print("🔍 Interactive API docs: http://localhost:8765/redoc")
    print("💚 Health check: http://localhost:8765/health")
    print("\nPress Ctrl+C to stop the server\n")
    
    uvicorn.run(
        "main:app",  # Use import string instead of app object
        host="0.0.0.0", 
        port=8765,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    ) 