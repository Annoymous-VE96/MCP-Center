from mcp.server.fastmcp import FastMCP
from domains.github.tools import create_github_issue_tool, get_repo_activity_tool
from domains.discord.tools import send_discord_notification_tool




mcp = FastMCP("MCP_Center")

mcp.tool()(create_github_issue_tool)
mcp.tool()(get_repo_activity_tool)
mcp.tool()(send_discord_notification_tool)

if __name__ == "__main__":
    mcp.run(transport="stdio")