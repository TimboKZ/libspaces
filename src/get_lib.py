import json
import requests

from credentials import *

# TODO use dropbox responses to test this
# TODO set up unit tests :)
# TODO write main bot logic
# TODO set up arguments
# TODO set up bot that takes location
# TODO figure out how to get closest room to a location
# TODO deploy on heroku

def get_most_free_desktops(params, limit=3):
    r = requests.get('https://uclapi.com/resources/desktops',
                     params=params).json()
    if not 'ok' in r or not r['ok']:
        return None
    else:
        sorted_by_free_seats = sorted(r['data'],
                                      key=lambda x: -int(x['free_seats']))
        return sorted_by_free_seats[:limit]

def format_desktop_as_str(desktop):
    loc = desktop['location']
    return (
        f"{desktop['free_seats']}/{desktop['total_seats']} free" + "\n"
        f"{loc['roomname']}, {loc['building_name']}" + "\n"
        f"{loc['address']} {loc['postcode']}"
    )

def format_desktop_as_telegram_venue_message(chat_id, desktop):
    loc = desktop['location']
    return {
        'chat_id': chat_id,
        'latitude': loc['latitude'],
        'longitude': loc['longitude'],
        'title': "{loc['building_name']} {loc['roomname']}",
        'address': "{loc['address']} {loc['postcode']}"
    }

def send_telegram_answer(url, chat_id, top_desktops):
    for desktop in top_desktops:
        text_params = {
            'chat_id': chat_id,
            'text': format_desktop_as_str(desktop)
        }
        text_response = requests.post(url + 'sendMessage', data=text_params)
        venue_params = format_desktop_as_telegram_venue_message(chat_id,
                                                                desktop)
        venue_response = requests.post(url + 'sendVenue', data=venue_params)
        # TODO make sure to check responses

print(format_desktop_as_str(get_most_free_desktops({'token': uclapi_token})[0]))
'''        print(json.dumps(sorted_by_free_seats, sort_keys=True,
                         indent=4, separators=(',', ': ')))
                         '''
