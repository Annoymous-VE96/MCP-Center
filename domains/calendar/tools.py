from domains.calendar.client import create_event, get_events_in_range, is_slot_free
from domains.calendar.schemas import (
    CreateEventInput, CreateEventOutput, CheckAvailabilityInput,
    GetUpcomingEventsInput, CalendarEventItem, CheckAvailabilityOutput
)


def create_calendar_event_tool(input: CreateEventInput) -> CreateEventOutput:
    """
    Creates a real event in the google calendar.
    input: title, start_time, end_time (ISO 8601 format "YYYY-MM-DDTHH:MM:SS", e.g. "2026-06-27T10:00:00"), description
    output: event id, link of the event on calendar
    """
    event = create_event(
        input.title, input.start_time, 
        input.end_time, input.description
    )
    return CreateEventOutput(
        event_id=event["id"],
        html_link=event["htmlLink"]
    )


def get_upcoming_events_tool(input: GetUpcomingEventsInput) -> list[CalendarEventItem]:
    """
    Gets the list of event from the google calendar used to check availability
    input: start time, end time (ISO 8601 format "YYYY-MM-DDTHH:MM:SS", e.g. "2026-06-27T10:00:00")
    output: list of event id, date, start and end time, title
    """
    events = get_events_in_range(input.start_time, input.end_time)
    return [
        CalendarEventItem(
            event_id=e["id"],
            title=e.get("summary", "(no title)"),
            start_time=e["start"].get("dateTime", e["start"].get("date")),
            end_time=e["end"].get("dateTime", e["end"].get("date")),
        )
        for e in events
    ]

def check_availability_tool(input: CheckAvailabilityInput) -> CheckAvailabilityOutput:
    """
    Used to check the avialablilty for a particular slot/time range on a particular day 
    input: start time, end time (ISO 8601 format "YYYY-MM-DDTHH:MM:SS", e.g. "2026-06-27T10:00:00")
    output: available(boolean) true means available, conflicting_events a list if empty no event on that slot means free 
    """
    events = get_events_in_range(input.start_time, input.end_time)
    free = is_slot_free(input.start_time, input.end_time, events)
    return CheckAvailabilityOutput(
        available=free,
        conflicting_events=[] if free else events
    )