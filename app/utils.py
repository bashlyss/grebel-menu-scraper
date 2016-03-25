from datetime import date, timedelta

from app.scraper import menu, convert_daily_to_dict

def get_upcoming_meals(days=7):
    upcoming = []
    for day in [date.today() + timedelta(d) for d in range(days)]:
        upcoming.append(convert_daily_to_dict(menu[day]))
    return upcoming

def get_upcoming_meals_for_user(user, days=7):
    meals_by_day = get_upcoming_meals(days)
    preferences = [pref.food for pref in user.preferences]
    upcoming = [(day['day'][:-2], meal, day[meal]) for day in meals_by_day 
                for meal in day if day[meal] in preferences]
    return upcoming
