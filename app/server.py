import flask
from flask import redirect, url_for
from flask.ext.login import login_required, login_user, current_user

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
    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    form = forms.LoginForm()
    if form.validate_on_submit():
        user = db.get_user_by_email(email=form.email.data)
        if user is None or not user.check_password(form.password.data):
            return flask.render_template('login.html', form=form, invalid_login=True)
        login_user(user, remember=form.remember.data)

        next_url = flask.request.args.get('next')
        if not auth.next_is_valid(next_url):
            return flask.abort(404)

        return redirect(next_url or '/')

    return flask.render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('index.html')

    form = forms.RegistrationForm()

    if form.submit.data and form.validate():
        # User must pass recaptcha validation to get this far, so
        # this shouldn't be abusable in terms of phishing for email addresses
        if db.get_user_by_email(form.email.data) is not None:
            return flask.abort(400)

        user = db.add_user(
            name=form.name.data,
            email=form.email.data,
            password=form.password.data)
        flask.flash('Thanks for registering')

        login_user(user)
        return redirect(url_for('index'))

    return flask.render_template('register.html', form=form)

@app.route('/')
@login_required
def index():
    preferences = db.get_preferences_by_userid(current_user.id)
    return flask.render_template(
        'index.html',
        form=forms.FoodPreferenceForm(),
        preferences=preferences)

@app.route('/preference/delete/<int:pref_id>', methods=['DELETE'])
@login_required
def delete_preference(pref_id):
    preference = db.get_preference_by_id(pref_id=pref_id)
    if preference is None:
        return flask.jsonify(success=True)
    db.delete_preference(preference)
    return flask.jsonify(success=True)

@app.route('/preference/add', methods=['POST'])
@login_required
def add_preference():
    form = forms.FoodPreferenceForm()

    if form.submit.data and form.validate():
        preference = db.add_preference(
            food=form.food.data,
            user_id=current_user.id)
    return redirect(url_for('index'))

def set_calendar_headers(resp):
    if resp.headers['Content-Type'].startswith('text/calendar'):
        resp.headers['Content-Type'] = 'text/calendar; charset=UTF-8; method=PUBLISH'
    return resp

app.after_request(set_calendar_headers)
