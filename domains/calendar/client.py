from googleapiclient.discovery import build
from domains.calendar.auth import get_credentials
from datetime import datetime

CALENDAR_ID = "primary"


def _get_service():
    creds = get_credentials()
    return build("calendar", "v3", credentials=creds)

def ensure_ist(time: str) -> str:
    if not (time.endswith('+05:30')):
        time += '+05:30'
    return time

def create_event(
        title: str, start_time: str, end_time: str,
        description: str = "", timezone: str = "Asia/Kolkata"
) -> dict:
    service = _get_service()
    body = {
        "summary": title,
        "description": description,
        "start": {"dateTime": start_time, "timeZone": timezone},
        "end": {"dateTime": end_time, "timeZone": timezone},
    }
    print("DEBUG body:", body)
    event = service.events().insert(calendarId=CALENDAR_ID, body=body).execute()
    return event


def get_events_in_range(time_min: str, time_max: str) -> list[dict]:
    service = _get_service()
    result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=ensure_ist(time_min),   
        timeMax=ensure_ist(time_max),
        singleEvents=True,
        orderBy="startTime",
    ).execute()
    return result.get("items", [])

def is_slot_free(requested_start: str, requested_end: str, events: list[dict]) -> bool:
    req_start = datetime.fromisoformat(ensure_ist(requested_start))
    req_end = datetime.fromisoformat(ensure_ist(requested_end))

    for e in events:
        ev_start = datetime.fromisoformat(e["start"].get("dateTime", e["start"].get("date")))
        ev_end = datetime.fromisoformat(e["end"].get("dateTime", e["end"].get("date")))
        if ev_start < req_end and ev_end > req_start:
            return False  # overlap found
    return True