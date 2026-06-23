from domains.github.tools import create_github_issue_tool, get_repo_activity_tool
from domains.github.schemas import CreateIssueInput, RepoActivityInput
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MCP_Center")

@mcp.tool()
def create_github_issue(repo: str, title: str, body: str = "") -> dict:
    result = create_github_issue_tool(CreateIssueInput(repo=repo, title=title, body=body))
    return result.model_dump()

@mcp.tool()
def get_repo_activity(repo: str, per_page: int = 5) -> list[dict]:
    result = get_repo_activity_tool(RepoActivityInput(repo=repo, per_page=per_page))
    return [r.model_dump() for r in result]