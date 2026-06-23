from pydantic import BaseModel, Field

class CreateIssueInput(BaseModel):
    repo: str = Field(..., description="Format: owner/repo")
    title: str
    body: str = ""

class CreateIssueOutput(BaseModel):
    issue_number: int
    url: str

class RepoActivityInput(BaseModel):
    repo: str
    per_page: int = 5
    page : int = 2

class RepoActivityItem(BaseModel):
    type: str
    actor: str
    created_at: str