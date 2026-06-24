import datetime 
from domains.calendar.tools import create_calendar_event_tool, get_upcoming_events_tool
from domains.calendar.schemas import CreateEventInput, GetUpcomingEventsInput

def test_create():
    start = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    end = start + datetime.timedelta(hours=1)

    result  = create_calendar_event_tool(CreateEventInput(
        title='MCP Test Event',
        start_time=start.strftime("%Y-%m-%dT%H:%M:%S"),
        end_time=end.strftime("%Y-%m-%dT%H:%M:%S"),
        description='Created by test_manual.py',
        timezone='UTC'
    ))
    print('Created Event')
    print('event id: ', result.event_id)    
    print('link : ', result.html_link)


def test_list():
    results = get_upcoming_events_tool(GetUpcomingEventsInput(max_results=5))
    print(f'\nUpcoming events  ({len(results)})')
    for e in results: 
        print(f'- {e.title} | {e.start_time} -> {e.end_time} | id={e.event_id}')    


if __name__ == '__main__':
    test_create()
    test_list()