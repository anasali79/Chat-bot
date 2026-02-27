import streamlit as st
import requests
import json
import os
from typing import Dict, Any
import streamlit.components.v1 as components

# Set up the Streamlit page
st.set_page_config(
    page_title="Titanic Dataset Chatbot",
    page_icon="🚢",
    layout="wide"
)

# Title and description
st.title("🚢 Titanic Dataset Explorer")
st.markdown("""
Welcome to the Titanic Dataset Explorer! Ask questions about the Titanic passengers in plain English, 
and get both text answers and visual insights.
""")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar with example questions
with st.sidebar:
    st.header("🔍 Example Questions")
    st.markdown("""
    - What percentage of passengers were male on the Titanic?
    - Show me a histogram of passenger ages
    - What was the average ticket fare?
    - How many passengers embarked from each port?
    - What was the survival rate by gender?
    - Show me the distribution of passenger classes
    - What was the average age of survivors vs non-survivors?
    """)
    
    if st.button("Load Example: Male Passengers"):
        st.session_state.example_query = "What percentage of passengers were male on the Titanic?"
    elif st.button("Load Example: Age Histogram"):
        st.session_state.example_query = "Show me a histogram of passenger ages"
    elif st.button("Load Example: Avg Fare"):
        st.session_state.example_query = "What was the average ticket fare?"
    elif st.button("Load Example: Embark Ports"):
        st.session_state.example_query = "How many passengers embarked from each port?"

# Main chat interface
chat_container = st.container()

# Display chat history
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# User input form
with st.form(key="chat_form", clear_on_submit=True):
    # Use example query if available, otherwise empty string
    default_query = st.session_state.get("example_query", "")
    user_input = st.text_input("Ask a question about the Titanic dataset:", default_query)
    submit_button = st.form_submit_button(label="Send")
    
    # Clear example query after using it
    if submit_button and "example_query" in st.session_state:
        del st.session_state["example_query"]

# Process user input
if submit_button and user_input.strip():
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Show user message immediately
    with chat_container:
        with st.chat_message("user"):
            st.write(user_input)
    
    # Show a spinner while processing
    with st.spinner("Analyzing your question..."):
        try:
            # Send request to the backend API
            api_url = os.getenv("BACKEND_URL", "http://localhost:8000") + "/api/v1/ask"
            payload = {"query": user_input}
            
            response = requests.post(api_url, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                
                if result["success"]:
                    # Add bot response to history
                    response_text = result["text_response"]
                    visualization_html = result["visualization"]
                    
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                    
                    # Display bot response
                    with chat_container:
                        with st.chat_message("assistant"):
                            st.write(response_text)
                            
                            # Display visualization if available
                            if visualization_html:
                                components.html(visualization_html, height=600)
                else:
                    error_msg = f"Error: {result['text_response']}"
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    
                    with chat_container:
                        with st.chat_message("assistant"):
                            st.error(error_msg)
            else:
                error_msg = f"Error connecting to the backend API: {response.status_code}"
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                
                with chat_container:
                    with st.chat_message("assistant"):
                        st.error(error_msg)
                        
        except requests.exceptions.ConnectionError:
            error_msg = "Could not connect to the backend API. Please make sure the FastAPI server is running on http://localhost:8000"
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            
            with chat_container:
                with st.chat_message("assistant"):
                    st.error(error_msg)
        except Exception as e:
            error_msg = f"An unexpected error occurred: {str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            
            with chat_container:
                with st.chat_message("assistant"):
                    st.error(error_msg)

# Add some space at the bottom
st.markdown("---")
st.markdown("**Note:** This application connects to a FastAPI backend. Make sure to start the backend server before asking questions.")