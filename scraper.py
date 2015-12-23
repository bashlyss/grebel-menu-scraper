import requests
import re

# separate by | if adding more
search_flags = re.DOTALL | re.MULTILINE

def clean_col(col_text):
    clean_whitespace = " ".join(col_text.split()).strip()
    clean_multi = re.subn("</p> <p>", ",", clean_whitespace, flags=search_flags)[0]
    clean_p = re.subn("</?p>", "", clean_multi, flags=search_flags)[0]
    clean_br = re.subn("<br ?/?>", "", clean_p, flags=search_flags)[0]
    clean_strong = re.subn("</?strong>", "", clean_br, flags=search_flags)[0]
    return clean_strong

def scrape_menu():
    url = "https://uwaterloo.ca/grebel/current-students/general-information/kitchen/weekly-menu"
    single_week_regex = ".*?(<p>.*?</p>)\n\n(<table width=\"...\">.*?</table>)"
    raw = requests.get(url).text
    regex = re.compile(single_week_regex, search_flags)

    raw_weekly_list = regex.findall(raw)

    all_weeks = {}
    for week in raw_weekly_list:
        # because this is scraped, the format of the spacing on this string is inconsistent
        # approximately resembles "January 4th - January 10th/2016" most of the time
        dates = re.search("<p>.*<strong>(.*?)</strong>.*</p>$", week[0]).group(1).strip()
        rows = re.findall("<tr>(.*?)</tr>", week[1], search_flags)
        cleaned_table = []
        for row in rows:
            cols = re.findall("<t[hd].*?>(.*?)</t[hd]>", row, search_flags)
            cols = map(clean_col, cols)
            
            cleaned_table.append(cols)
        all_weeks[dates] = cleaned_table

    return all_weeks
