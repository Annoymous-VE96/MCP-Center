from mcp.server.fastmcp import FastMCP
from domains.github.tools import create_github_issue_tool, get_repo_activity_tool
from domains.discord.tools import send_discord_notification_tool
from domains.calendar.tools import create_calendar_event_tool, get_upcoming_events_tool
from domains.weather.tools import get_weather_tool
from domains.news.tools import get_news_feed_tool

mcp = FastMCP("MCP_Center")

mcp.tool()(create_github_issue_tool)
mcp.tool()(get_repo_activity_tool)
mcp.tool()(send_discord_notification_tool)
mcp.tool()(create_calendar_event_tool)
mcp.tool()(get_upcoming_events_tool)
mcp.tool()(get_news_feed_tool)
mcp.tool()(get_weather_tool)


if __name__ == "__main__":
    mcp.run(transport="stdio")