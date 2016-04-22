from collections import namedtuple
from datetime import date, timedelta

from app.scraper import menu, convert_daily_to_dict

UpcomingMeal = namedtuple('UpcomingMeal', 'day meal food')

def get_upcoming_meals(days=7):
    upcoming = []
    for day in [date.today() + timedelta(d) for d in range(days)]:
        daily_menu = menu.get(day)
        if daily_menu is not None:
            upcoming.append(convert_daily_to_dict(menu.get(day)))
    return upcoming

def get_upcoming_meals_for_user(user, days=7):
    meals_by_day = get_upcoming_meals(days)
    preferences = [pref.food for pref in user.preferences]
    # Using third for loop to get a reference to the key with the matching value
    # Cutting last 2 characters ': ' as taken from the original raw calendar table
    upcoming = [UpcomingMeal(day['day'][:-2], meal, day[meal])
                for day in meals_by_day 
                for meal in day 
                for food in preferences 
                if food.lower() in day[meal].lower()]
    return upcoming
