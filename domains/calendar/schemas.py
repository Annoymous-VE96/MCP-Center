from pydantic import BaseModel, Field


class CreateEventInput(BaseModel):
    title: str
    start_time: str = Field(..., description="IST, e.g. 2026-06-27T10:00:00+05:30")
    end_time: str = Field(..., description="IST, e.g. 2026-06-27T10:00:00+05:30")
    description: str = ""
    timezone: str = "IST"

class CreateEventOutput(BaseModel):
    event_id: str
    html_link: str

class CheckAvailabilityInput(BaseModel):
    start_time: str
    end_time: str

class CheckAvailabilityOutput(BaseModel):
    available: bool
    conflicting_events: list[dict]

class GetUpcomingEventsInput(BaseModel):
    start_time: str
    end_time: str

class CalendarEventItem(BaseModel):
    event_id: str
    title: str
    date: str
    start_time: str
    end_time: str