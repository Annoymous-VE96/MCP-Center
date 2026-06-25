from domains.github.tools import create_github_issue_tool, get_repo_activity_tool
from domains.calendar.tools import create_calendar_event_tool, get_upcoming_events
from domains.weather.tools import get_weather_tool
from domains.github.schemas import CreateIssueInput, RepoActivityInput
from domains.weather.schemas import WeatherBriefInput, WeatherBriefOutput
from domains.calendar.schemas import (
    CreateEventInput, CreateEventOutput,
    GetUpcomingEventsInput, CalendarEventItem,
)
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MCP_Center")

@mcp.tool()
def create_github_issue(input: CreateIssueInput) -> dict:
    return create_github_issue_tool(input).model_dump()

@mcp.tool()
def get_repo_activity(input: RepoActivityInput) -> list[dict]:
    return [r.model_dump() for r in get_repo_activity_tool(input)]

@mcp.tool()
def create_calendar_event(input: CreateEventInput) -> dict:
    return create_calendar_event_tool(input).model_dump()

@mcp.tool()
def get_weather(input: WeatherBriefInput) -> dict: 
    return get_weather_tool(input).model_dump()
