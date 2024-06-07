from datetime import datetime, timedelta

import pytz
from icalendar import Calendar, Event


def create_icalendar_file(game_details) -> bytes:
    cal = Calendar()
    event = Event()

    event.add('summary', game_details['name'])
    event.add('dtstart', game_details['datetime'])
    event.add('dtend', game_details['datetime'] + timedelta(hours=2))  # Assume the game lasts 2 hours
    event.add('dtstamp', datetime.now(pytz.utc))
    event.add('location', game_details['place'])
    event.add('description', f"descr")

    cal.add_component(event)
    return cal.to_ical()
