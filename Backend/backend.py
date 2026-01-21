from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

app = FastAPI()

# Load Keys
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("❌ GROQ_API_KEY not found in .env file")

if not GITHUB_TOKEN:
    print("⚠️ WARNING: GITHUB_TOKEN not found. Public rate limits apply.")

# Initialize Groq Client
client = Groq(api_key=GROQ_API_KEY)


# -------- Request Schema --------
class IssueRequest(BaseModel):
    repo_url: str
    issue_number: int


# -------- Helper Functions --------
def extract_owner_repo(repo_url: str):
    parts = repo_url.rstrip("/").split("/")
    return parts[-2], parts[-1]


# ✅ Fetch issue details (DICT)
def fetch_github_issue(owner: str, repo: str, issue_number: int):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(url, headers=headers, timeout=30)

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="GitHub issue not found")

    return response.json()


# ✅ Fetch issue comments (LIST)
def fetch_github_comments(owner: str, repo: str, issue_number: int):
    comments_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(comments_url, headers=headers, timeout=30)

    if response.status_code != 200:
        return []

    comments_data = response.json()

    comments = [comment.get("body", "") for comment in comments_data]

    return comments


# ✅ AI Summary Generator
def generate_ai_summary(title: str, body: str, comments: list):
    comments_text = "\n".join(comments[:5])  # limit to first 5 comments

    prompt = f"""
You are an AI assistant that analyzes GitHub issues.

Return ONLY valid JSON exactly in this format:

{{
  "summary": "One sentence summary",
  "type": "bug | feature_request | documentation | question | other",
  "priority_score": "1-5 with short justification",
  "suggested_labels": ["label1", "label2"],
  "potential_impact": "Short sentence"
}}

GitHub Issue Title:
{title}

GitHub Issue Description:
{body}

GitHub Comments:
{comments_text if comments_text else "No comments available"}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        timeout=30
    )

    return response.choices[0].message.content


# -------- API Endpoint --------
@app.post("/analyze-issue")
def analyze_issue(data: IssueRequest):
    try:
        owner, repo = extract_owner_repo(data.repo_url)

        # Fetch issue details
        issue = fetch_github_issue(owner, repo, data.issue_number)

        # Fetch comments
        comments = fetch_github_comments(owner, repo, data.issue_number)

        title = issue.get("title", "")
        body = issue.get("body", "")

        ai_result = generate_ai_summary(title, body, comments)

        return {
            "repo": data.repo_url,
            "issue_number": data.issue_number,
            "analysis": ai_result
        }

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
