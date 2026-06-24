from domains.calendar.client import create_event, get_upcoming_events
from domains.calendar.schemas import (
    CreateEventInput, CreateEventOutput,
    GetUpcomingEventsInput, CalendarEventItem,
)


def create_calendar_event_tool(input: CreateEventInput) -> CreateEventOutput:
    event = create_event(
        input.title, input.start_time, input.end_time,
        input.description, input.timezone
    )
    return CreateEventOutput(
        event_id=event["id"],
        html_link=event["htmlLink"]
    )


def get_upcoming_events_tool(input: GetUpcomingEventsInput) -> list[CalendarEventItem]:
    events = get_upcoming_events(input.max_results)
    return [
        CalendarEventItem(
            event_id=e["id"],
            title=e.get("summary", "(no title)"),
            start_time=e["start"].get("dateTime", e["start"].get("date")),
            end_time=e["end"].get("dateTime", e["end"].get("date")),
        )
        for e in events
    ]