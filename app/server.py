import flask
from flask.ext.login import login_required, login_user

from app import app, writer, db, forms
# Import auth to register the routes
# pylint disable=unused-import
from app import auth

@app.route('/refresh', methods=['POST'])
def refresh():
    writer.update_calendars()
    return '', 200

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = db.get_user_by_email(email=form.email.data)
        if user is None:
            return flask.redirect(flask.url_for('login'))
        login_user(user, remember=form.remember.data)

        next_url = flask.request.args.get('next')
        if not auth.next_is_valid(next_url):
            return flask.abort(404)

        return flask.redirect(next_url or '/')
    return flask.render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegistrationForm()
    if form.submit.data and form.validate():
        db.add_user(
            name=form.name.data,
            email=form.email.data)
        flask.flash('Thanks for registering')
        return flask.redirect(flask.url_for('login'))
    return flask.render_template('register.html', form=form)

@app.route('/')
@login_required
def index():
    return flask.render_template('index.html')

def set_calendar_headers(resp):
    if resp.headers['Content-Type'].startswith('text/calendar'):
        resp.headers['Content-Type'] = 'text/calendar; charset=UTF-8; method=PUBLISH'
    return resp

app.after_request(set_calendar_headers)
