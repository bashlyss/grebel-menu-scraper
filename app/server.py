from flask import Flask

from . import writer

app = Flask(__name__)

@app.route('/refresh', methods=['POST'])
def refresh():
    writer.update_calendars()
    return '', 200

def set_calendar_headers(resp):
    if resp.headers['Content-Type'].startswith('text/calendar'):
        resp.headers['Content-Type'] = 'text/calendar; charset=UTF-8; method=PUBLISH'
    return resp

app.after_request(set_calendar_headers)
