import os
import httpx
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
BASE_URL = "https://api.github.com"

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

def create_issue(repo: str, title: str, body: str = "") -> dict:
    url = f"{BASE_URL}/repos/{repo}/issues"
    resp = httpx.post(url, headers=HEADERS, json={"title": title, "body": body})
    resp.raise_for_status()
    return resp.json()

def get_repo_activity(repo: str, per_page: int = 5, page: int = 2) -> dict:
    url = f"{BASE_URL}/repos/{repo}/events"
    resp = httpx.get(url, headers=HEADERS, params={"per_page": per_page, 'page': page})
    resp.raise_for_status()
    return resp.json()