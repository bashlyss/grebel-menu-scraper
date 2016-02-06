import re
from HTMLParser import HTMLParser
from datetime import date, timedelta

import requests
from dateutil import parser

class MLStripper(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

# separate by | if adding more
search_flags = re.DOTALL | re.MULTILINE
MEAL_ORDER = ['day','breakfast','lunch','lunch_vegetarian','supper','supper_vegetarian','snack']

def clean_col(col_text):
    clean_whitespace = " ".join(col_text.split()).strip()
    clean_multi = re.subn("</p> <p>", ", ", clean_whitespace, flags=search_flags)[0]

    # TODO strong, em and texting ending in an exclamation mark indicate titles
    # we should probably deal with those differently
    return strip_tags(clean_multi)

def get_date(date_range):
    MONTH = 'January|February|March|April|May|June|July|August|September|October|November|December'
    [day_str, year_str] = date_range.split('/')

    # We don't have to worry about straddling two years since the menu will never include the end of December/
    # start of January
    year = int(year_str.strip())

    [start_str, end_str] = day_str.split('-')

    # Use the default to parse in the context of the appropriate year (important for leap years)
    start = parser.parse(start_str, fuzzy=True, default=date(year, 1, 1))
    if re.search(MONTH, end_str):
        end = parser.parse(end_str, fuzzy=True, default=date(year, 1, 1))
    else:
        end_day = int(re.search(r'\d+', end_str).group(0))
        end = date(year, start.month, end_day)

    return start, end

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)+1):
        yield start_date + timedelta(n), n

def scrape_menu():
    url = "https://uwaterloo.ca/grebel/current-students/general-information/kitchen/weekly-menu"
    single_week_regex = ".*?(<p>.*?</p>)(\n)*(<table width=\"...\">.*?</table>)"
    raw = requests.get(url).text
    regex = re.compile(single_week_regex, search_flags)

    raw_weekly_list = regex.findall(raw)

    daily_menu = {}
    weekly_menu_by_meal = {}
    for week in raw_weekly_list:
        # because this is scraped, the format of the spacing on this string is inconsistent
        # approximately resembles "January 4th - January 10th/2016" most of the time
        raw_dates = re.search("<p>.*<strong>(.*?)</strong>.*</p>$", week[0]).group(1).strip()
        dates = get_date(raw_dates)

        rows = re.findall("<tr>(.*?)</tr>", week[2], search_flags)
        cleaned_table = []
        for row in rows:
            cols = re.findall("<t[hd].*?>(.*?)</t[hd]>", row, search_flags)
            cols = map(clean_col, cols)

            cleaned_table.append(cols)

        weekly_menu_by_meal[dates] = {}
        for meal in zip(MEAL_ORDER, cleaned_table):
            weekly_menu_by_meal[dates][meal[0]] = meal[1][1:]

        weekly_menu = zip(*cleaned_table)
        for day, index in daterange(dates[0], dates[1]):
            daily_menu[day] = weekly_menu[index + 1]

    return daily_menu, weekly_menu_by_meal

def convert_daily_to_dict(menu_day):
    daily_dict = {}
    for meal in zip(menu_day, MEAL_ORDER):
        daily_dict[meal[1]] = meal[0]
    return daily_dict

def get_todays_menu(menu_dict):
    return menu_dict[date.today()]

menu, weekly_meals = scrape_menu()
today = get_todays_menu(menu)
