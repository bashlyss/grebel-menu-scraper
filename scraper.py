import requests
import re
from dateutil import parser
from datetime import date, datetime, timedelta

# separate by | if adding more
search_flags = re.DOTALL | re.MULTILINE

def clean_col(col_text):
    clean_whitespace = " ".join(col_text.split()).strip()
    clean_multi = re.subn("</p> <p>", ",", clean_whitespace, flags=search_flags)[0]
    clean_p = re.subn("</?p>", "", clean_multi, flags=search_flags)[0]
    clean_br = re.subn("<br ?/?>", "", clean_p, flags=search_flags)[0]
    clean_strong = re.subn("</?strong>", "", clean_br, flags=search_flags)[0]
    return clean_strong

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
    single_week_regex = ".*?(<p>.*?</p>)\n\n(<table width=\"...\">.*?</table>)"
    raw = requests.get(url).text
    regex = re.compile(single_week_regex, search_flags)

    raw_weekly_list = regex.findall(raw)

    daily_menu = {}
    for week in raw_weekly_list:
        # because this is scraped, the format of the spacing on this string is inconsistent
        # approximately resembles "January 4th - January 10th/2016" most of the time
        raw_dates = re.search("<p>.*<strong>(.*?)</strong>.*</p>$", week[0]).group(1).strip()
        dates = get_date(raw_dates)

        rows = re.findall("<tr>(.*?)</tr>", week[1], search_flags)
        cleaned_table = []
        for row in rows:
            cols = re.findall("<t[hd].*?>(.*?)</t[hd]>", row, search_flags)
            cols = map(clean_col, cols)

            cleaned_table.append(cols)

        weekly_menu = zip(*cleaned_table)
        for day, index in daterange(dates[0], dates[1]):
            daily_menu[day] = weekly_menu[index + 1]

    return daily_menu

def get_todays_menu(menu_dict):
    return menu_dict[date.today()]

result = scrape_menu()
