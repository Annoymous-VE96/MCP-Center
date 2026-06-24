from googleapiclient.discovery import build
from domains.calendar.auth import get_credentials

CALENDAR_ID = "primary"


def _get_service():
    creds = get_credentials()
    return build("calendar", "v3", credentials=creds)


def create_event(title: str, start_time: str, end_time: str,
                  description: str = "", timezone: str = "UTC") -> dict:
    service = _get_service()
    body = {
        "summary": title,
        "description": description,
        "start": {"dateTime": start_time, "timeZone": timezone},
        "end": {"dateTime": end_time, "timeZone": timezone},
    }
    event = service.events().insert(calendarId=CALENDAR_ID, body=body).execute()
    return event


def get_upcoming_events(max_results: int = 5) -> list[dict]:
    import datetime
    service = _get_service()
    now = datetime.datetime.utcnow().isoformat() + "Z"
    result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=now,
        maxResults=max_results,
        singleEvents=True,
        orderBy="startTime",
    ).execute()
    return result.get("items", [])