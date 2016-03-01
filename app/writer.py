from os import path
from datetime import datetime, time
from itertools import takewhile

from icalendar import Calendar, Event
from pytz import timezone

from .scraper import menu

STATIC_DIR = path.join(path.dirname(__file__), 'static')


class UUIDMaker(object):
    """
    Creates universally unique ids using a combination of an app identifier, the current time
    and a counter (for when the time doesn't offer enough resolution)
    """

    def __init__(self):
        self.counter = 0

    def get(self):
        uid = '{}-{}{}'.format(datetime.utcnow().isoformat(), self.counter, '@grebelife-menu')
        self.counter += 1
        return uid


def get_calendar(fname, title, uuid_maker):
    """ Either get the calendar file `fname` or create it """
    cal_path = path.join(STATIC_DIR, fname)
    if path.exists(cal_path):
        with open(cal_path, 'rb') as cal_file:
            return Calendar.from_ical(cal_file.read())

    cal = Calendar()
    cal.add('prodid', '-//{}//grebelife.com//'.format(title))
    cal.add('version', '2.0')
    stamp(cal)
    cal.add('uid', uuid_maker.get())
    return cal

def write_calendar(fname, cal):
    cal_path = path.join(STATIC_DIR, fname)

    with open(cal_path, 'wb') as cal_file:
        cal_file.write(cal.to_ical(True))

def make_datetime(date_part, time_part):
    time_part = time_part.replace(tzinfo=timezone('America/New_York'))
    return datetime.combine(date_part, time_part)


def stamp(component):
    """ Stamps `component` with a 'dtstamp' attribute """
    component.add('dtstamp', datetime.utcnow())


def make_event(cal, uuid_maker):
    """ Creates a new event in `cal` """
    e = Event()
    e.add('uid', uuid_maker.get())
    stamp(e)
    cal.add_component(e)
    return e


def set_times(e, times):
    """ Set the start and end times of event `e` using the tuple of datetimes `times` """
    e.add('dtstart', times[0])
    e.add('dtend', times[1])

def remove_events_on_menu(cal, menu_start):
    """ Removes any events from `cal` that have been "rescraped" """
    cal.subcomponents[:] = takewhile(lambda e: e['DTSTART'].dt < menu_start, cal.subcomponents)

def update_calendars():
    # pylint: disable=no-member

    uuid_maker = UUIDMaker()

    MENU_FILE = 'menu.ics'
    VEG_MENU_FILE = 'veg_menu.ics'
    SNACK_MENU_FILE = 'snack_menu.ics'

    cal = get_calendar(MENU_FILE, 'Grebel Weekly Menu', uuid_maker)
    veg_cal = get_calendar(VEG_MENU_FILE, 'Grebel Weekly Vegetarian Menu', uuid_maker)
    snack_cal = get_calendar(SNACK_MENU_FILE, 'Grebel Weekly Snack Menu', uuid_maker)

    sorted_menu_keys = sorted(menu.keys())
    menu_start = make_datetime(sorted_menu_keys[0], time(0, 0, 0))

    remove_events_on_menu(cal, menu_start)
    remove_events_on_menu(veg_cal, menu_start)
    remove_events_on_menu(snack_cal, menu_start)

    for key in sorted_menu_keys:
        day, breakfast, lunch, lunch_veg, dinner, dinner_veg, snack = menu[key]

        # Can't check breakfast since that's always blank on weekends
        if not lunch:
            continue

        if day in ['Sat', 'Sun']:
            times = {
                'breakfast': (time(8, 0, 0), time(11, 0, 0)),
                'lunch': (time(12, 0, 0), time(13, 30, 0)),
                'dinner': (time(17, 0, 0), time(18, 0, 0)),
                'snack': (time(21, 0, 0), time(22, 0, 0))
            }
        else:
            times = {
                'breakfast': (time(7, 30, 0), time(9, 0, 0)),
                'lunch': (time(11, 30, 0), time(13, 40, 0)),
                'dinner': (time(17, 0, 0), time(18, 30, 0)),
                'snack': (time(22, 10, 0), time(22, 30, 0))
            }

        for meal_key in times.keys():
            start, end = times[meal_key]
            times[meal_key] = (make_datetime(key, start), make_datetime(key, end))

        e = make_event(cal, uuid_maker)
        set_times(e, times['breakfast'])
        e.add('summary', breakfast or 'Cold Breakfast')

        e = make_event(cal, uuid_maker)
        set_times(e, times['lunch'])
        e.add('summary', lunch)

        e = make_event(veg_cal, uuid_maker)
        set_times(e, times['lunch'])
        e.add('summary', lunch_veg)

        e = make_event(cal, uuid_maker)
        set_times(e, times['dinner'])
        e.add('summary', dinner)

        e = make_event(veg_cal, uuid_maker)
        set_times(e, times['dinner'])
        e.add('summary', dinner_veg)

        if snack:
            e = make_event(snack_cal, uuid_maker)
            set_times(e, times['snack'])
            e.add('summary', snack)

    write_calendar(MENU_FILE, cal)
    write_calendar(VEG_MENU_FILE, veg_cal)
    write_calendar(SNACK_MENU_FILE, snack_cal)
