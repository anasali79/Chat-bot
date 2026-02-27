from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
import json

from ..models.titanic_agent import create_titanic_agent

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/ask")
async def ask_titanic_question(request: QueryRequest) -> Dict[str, Any]:
    """
    Process a natural language query about the Titanic dataset.
    
    Args:
        request: QueryRequest containing the user's question
        
    Returns:
        Dictionary containing the response and any visualizations
    """
    try:
        # Create the agent
        agent = create_titanic_agent()
        
        # Process the query
        response = agent(request.query)
        
        # Check if the response contains HTML for visualization
        has_visualization = "<div" in response and "plotly" in response
        visualization_html = ""
        
        if has_visualization:
            # Extract the visualization HTML
            start_idx = response.find('<div')
            end_idx = response.rfind('</div>') + 6
            visualization_html = response[start_idx:end_idx]
            
            # Get the text part (before or after HTML)
            text_response = response.replace(visualization_html, "").strip()
            if text_response.endswith("Here it is:") or "I've created" in text_response:
                text_response = text_response.split("Here it is:")[0].split("I've created")[0].strip()
        else:
            text_response = response
            visualization_html = ""
        
        return {
            "query": request.query,
            "text_response": text_response,
            "visualization": visualization_html,
            "success": True
        }
        
    except Exception as e:
        return {
            "query": request.query,
            "text_response": f"Error processing your query: {str(e)}",
            "visualization": "",
            "success": False
        }

@router.get("/health")
async def health_check():
    """
    Health check endpoint to verify the service is running.
    """
    return {"status": "healthy", "service": "Titanic Chatbot API"}

@router.get("/info")
async def get_dataset_info():
    """
    Get basic information about the Titanic dataset.
    """
    from ..utils.data_loader import titanic_data
    
    df = titanic_data.get_dataframe()
    
    info = {
        "total_passengers": len(df),
        "columns": list(df.columns),
        "numeric_columns": df.select_dtypes(include=['number']).columns.tolist(),
        "categorical_columns": df.select_dtypes(include=['object']).columns.tolist(),
        "sample_questions": [
            "What percentage of passengers were male on the Titanic?",
            "Show me a histogram of passenger ages",
            "What was the average ticket fare?",
            "How many passengers embarked from each port?"
        ]
    }
    
    return info