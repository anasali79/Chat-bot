#!/usr/bin/env python3
"""
Startup script for Render deployment
"""

import os
import sys
import uvicorn

# Add the project root to the path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import app with proper error handling
try:
    from backend.main import app
except ImportError as e:
    print(f"Import error: {e}")
    print("Current path:", sys.path)
    print("Current working directory:", os.getcwd())
    raise

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting server on port {port}")
    uvicorn.run(
        "backend.main:app", 
        host="0.0.0.0", 
        port=port,
        reload=False  # Disable reload in production
    )