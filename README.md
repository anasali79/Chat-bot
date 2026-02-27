# Titanic Dataset Chatbot

A friendly chatbot that analyzes the famous Titanic dataset, allowing users to ask questions in plain English and receive both text answers and visual insights about the passengers.

## 🚀 Features

- **Natural Language Processing**: Ask questions about the Titanic dataset in plain English
- **Text Responses**: Get clear, accurate answers to your questions
- **Interactive Visualizations**: Generate helpful charts and graphs
- **Clean Interface**: User-friendly Streamlit interface

## 🛠️ Tech Stack

- **Backend**: Python with FastAPI
- **Agent Framework**: LangChain
- **Frontend**: Streamlit
- **Data Visualization**: Plotly, Matplotlib, Seaborn

## 📊 Example Questions

The chatbot can answer various questions about the Titanic dataset, including:

- "What percentage of passengers were male on the Titanic?"
- "Show me a histogram of passenger ages"
- "What was the average ticket fare?"
- "How many passengers embarked from each port?"

## 🏗️ Project Structure

```
titanic_chatbot/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── models/
│   │   ├── __init__.py
│   │   └── titanic_agent.py # LangChain agent
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── data_loader.py   # Data loading and preprocessing
│   │   └── visualizer.py    # Visualization functions
│   └── api/
│       ├── __init__.py
│       └── routes.py        # API endpoints
├── frontend/
│   └── app.py               # Streamlit application
├── data/
│   └── titanic.csv          # Dataset file
└── requirements.txt         # Dependencies
```

## 📋 Installation

1. Clone the repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 Usage

### Backend Server
Start the FastAPI backend server:
```bash
cd backend
python -m main
```

The API will be available at `http://localhost:8000`.

### Frontend Application
Run the Streamlit application:
```bash
cd frontend
streamlit run app.py
```

The chatbot interface will be available in your browser.

## 🔧 API Endpoints

- `GET /` - Root endpoint with API information
- `GET /api/v1/health` - Health check
- `GET /api/v1/info` - Dataset information
- `POST /api/v1/ask` - Ask questions about the dataset

## 📈 Visualizations

The chatbot can generate various visualizations:
- Histograms for age distribution
- Bar charts for categorical data (embarkation ports, gender, class)
- Pie charts for percentages
- Survival rate comparisons

## 🤖 Agent Capabilities

The LangChain agent is equipped with several tools:
- **Passenger Percentage Calculator**: Calculate percentages of specific passenger groups
- **Passenger Counter**: Count passengers with specific characteristics
- **Average Calculator**: Calculate average values for numeric columns
- **Age Histogram Generator**: Generate age distribution histograms
- **Column Analyzer**: Analyze any column in the dataset

## 🎯 Supported Queries

The system understands various types of queries:
- Percentage calculations ("What percentage were...")
- Count queries ("How many passengers...")
- Average calculations ("What was the average...")
- Visualization requests ("Show me a histogram...")
- General analysis ("Tell me about...")

## 🚨 Troubleshooting

If you encounter issues:
1. Make sure all dependencies are installed
2. Ensure the `titanic.csv` file is in the `data/` directory
3. Verify the backend server is running before starting the frontend

## 📄 License

This project is licensed under the MIT License.