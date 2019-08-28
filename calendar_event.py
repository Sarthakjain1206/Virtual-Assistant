from apiclient.discovery import build
from datetime import *#timedelta
import pickle
import datefinder

credentials = pickle.load(open(r"C:/Users/Asus/Downloads/token.pkl","rb"))

service = build("calendar","v3",credentials=credentials)  # v3 is the version currently being used. you can get that by opening  
#Google Calendar API Reference and in its url you will find the version


def create_event(start_time_str, summary, duration=1, description=None, location=None):
    matches = list(datefinder.find_dates(start_time_str))
    if len(matches):
        start_time = matches[0]
        end_time = start_time + timedelta(hours=duration)
        
        event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
                'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': 'Asia/Kolkata',
                },
        'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60}, # i want a reminder before 24hrs through email.
                    {'method': 'popup', 'minutes': 10}, # message pop up before the 10 mins of the event
                ],
             },
        }
        return service.events().insert(calendarId='primary',body=event).execute() # adding an event
    else:
        return 'None'


def update_event(updated_summary):
    
    calendar = service.calendars().get(calendarId='primary').execute()
    
    calendar['summary'] = updated_summary

    updated_calendar = service.calendars().update(calendarId=calendar['id'], body=calendar).execute()
    
    return updated_calendar


def get_event():
    result = service.events().list(calendarId='primary').execute()
    final_list=[]
    for i in range(len(result['items'])):
        
        summary_str = result['items'][i]['summary']
        
        y = result['items'][0]['start']['dateTime']
        matches = list(datefinder.find_dates(y))[0]
        time_str = datetime.strftime(matches,"on %B %d,%Y at %H %M")
        print(time_str)
        final_str = f"event is {summary_str}... and it is {time_str}.."
        final_list.append(final_str)

    return final_list

def clear_events():
    clear = service.calendars().clear(calendarId='primary').execute()
    return clear





