from domains.calendar.client import create_event, get_upcoming_events
from domains.calendar.schemas import (
    CreateEventInput, CreateEventOutput,
    GetUpcomingEventsInput, CalendarEventItem,
)


def create_calendar_event_tool(input: CreateEventInput) -> CreateEventOutput:
    """
    Creates a real event in the google calendar.
    input: date, start & end time, title and description of the event
    output: event id, link of the event on calendar
    """
    event = create_event(
        input.title, input.start_time, input.end_time,
        input.description, input.timezone
    )
    return CreateEventOutput(
        event_id=event["id"],
        html_link=event["htmlLink"]
    )


def get_upcoming_events_tool(input: GetUpcomingEventsInput) -> list[CalendarEventItem]:
    """
    Gets the list of event from the google calendar used to check availability
    input: number of events to fetch
    output: event id, date, start and end time, title
    """
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