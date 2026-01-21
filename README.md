# AI Powered GitHub Issue Assistant

AI Powered GitHub Issue Assistant is a web application that helps developers quickly understand GitHub issues using Artificial Intelligence. Instead of manually reading long issue descriptions and comments, users can simply enter a GitHub repository URL and issue number to receive a clear summary, priority analysis, suggested labels, and potential impact.

The application uses a FastAPI backend to fetch issue details and comments from the GitHub REST API. The collected data is processed using a Groq AI model to generate structured insights. A professional Streamlit interface allows users to interact with the system easily and view both human-readable summaries and raw JSON outputs.

Key Features:
- Automatically fetches GitHub issue title, description, and comments
- Generates AI-powered structured analysis
- Displays human-readable summary and JSON output
- Clean and responsive user interface
- Friendly error handling for invalid inputs
- Secure API key management using environment variables

Project Structure:
AI POWERED GITHUB ISSUE ASSISTANT/
│
├── Backend/
│   ├── backend.py
│   ├── .env
│   └── __pycache__/
│
├── frontend/
│   └── ui.py
│
├── requirements.txt
└── README.md


Technologies Used:
- Frontend: Streamlit
- Backend: FastAPI
- AI Model: Groq (LLaMA 3.1)
- API Integration: GitHub REST API
- Programming Language: Python

Environment Setup:
Create a .env file inside the Backend folder and add:
GITHUB_TOKEN=your_github_personal_access_token
GROQ_API_KEY=your_groq_api_key

Installation:
pip install -r requirements.txt

How to Run:
Start Backend:
cd Backend
uvicorn backend:app --reload

Start Frontend:
cd frontend
streamlit run ui.py



