from pydantic import BaseModel, Field


class CreateEventInput(BaseModel):
    title: str
    start_time: str = Field(..., description="ISO 8601, e.g. 2026-06-25T10:00:00")
    end_time: str = Field(..., description="ISO 8601, e.g. 2026-06-25T11:00:00")
    description: str = ""
    timezone: str = "UTC"


class CreateEventOutput(BaseModel):
    event_id: str
    html_link: str


class GetUpcomingEventsInput(BaseModel):
    max_results: int = 5


class CalendarEventItem(BaseModel):
    event_id: str
    title: str
    start_time: str
    end_time: str