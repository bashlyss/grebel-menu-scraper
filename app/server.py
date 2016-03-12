import flask
from flask.ext.login import login_user, logout_user, login_required

from app import app, auth, db, models, forms, writer


@app.route('/refresh', methods=['POST'])
def refresh():
    writer.update_calendars()
    return '', 200

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    flask.flash(form.validate_on_submit())
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        if user is None:
            return flask.redirect('/login')
        login_user(user, remember=form.remember.data)

        flask.flash('Logged in successfully.')

        next_url = flask.request.args.get('next')
        if not auth.next_is_valid(next_url):
            return flask.abort(400)

        return flask.redirect(next_url or '/')
    return flask.render_template('login.html', form=form)

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegistrationForm()
    if form.submit.data and form.validate():
        user = models.User(form.name.data, form.email.data)
        db.session.add(user)
        db.session.commit()
        flask.flash('Thanks for registering')
        return flask.redirect('/login')
    return flask.render_template('register.html', form=form)

@app.route('/', methods=['GET'])
@login_required
def home():
    return flask.render_template('home.html')

def set_calendar_headers(resp):
    if resp.headers['Content-Type'].startswith('text/calendar'):
        resp.headers['Content-Type'] = 'text/calendar; charset=UTF-8; method=PUBLISH'
    return resp

app.after_request(set_calendar_headers)
