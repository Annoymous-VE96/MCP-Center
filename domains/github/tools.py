from domains.github.client import create_issue, get_repo_activity
from domains.github.schemas import (
    CreateIssueInput, CreateIssueOutput,
    RepoActivityInput, RepoActivityItem,
)
from mcp.server.fastmcp import FastMCP 

mcp = FastMCP('MCP_Center')

@mcp.tool()
def create_github_issue_tool(input: CreateIssueInput) -> CreateIssueOutput:
    data = create_issue(input.repo, input.title, input.body)
    return CreateIssueOutput(
        issue_number=data["number"],
        url=data["html_url"]
    )

@mcp.tool()
def get_repo_activity_tool(input: RepoActivityInput) -> list[RepoActivityItem]:
    data = get_repo_activity(input.repo, input.per_page, input.page)
    return [
        RepoActivityItem(**item)
        for item in data
    ]