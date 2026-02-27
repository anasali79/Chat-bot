from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import based on whether running as a script or module
try:
    from .api.routes import router as api_router
except ImportError:
    # Running as a script, import directly
    from api.routes import router as api_router

# Create the FastAPI app
app = FastAPI(
    title="Titanic Dataset Chatbot API",
    description="An API that allows users to ask questions about the Titanic dataset in natural language",
    version="1.0.0"
)

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    """
    Root endpoint that provides basic information about the API.
    """
    return {
        "message": "Welcome to the Titanic Dataset Chatbot API!",
        "endpoints": {
            "ask": "/api/v1/ask (POST)",
            "health": "/api/v1/health (GET)",
            "info": "/api/v1/info (GET)"
        },
        "description": "Send natural language questions about the Titanic dataset to /api/v1/ask"
    }

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)