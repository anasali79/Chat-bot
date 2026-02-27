#!/usr/bin/env python3
"""
Startup script for Render deployment
"""

import os
import sys
from backend.main import app
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting server on port {port}")
    uvicorn.run(
        "backend.main:app", 
        host="0.0.0.0", 
        port=port,
        reload=False  # Disable reload in production
    )