import logging
from time import time

import flask
from flask import session, flash, url_for, redirect, request
from flask.ext.login import LoginManager, login_user, login_required, logout_user
from flask_oauthlib.client import OAuth, OAuthException

from app import db, app
from app.models import User

logger = logging.getLogger(__name__)

login_manager = LoginManager(app)
# can't use url_for here since we are install initializing the app
login_manager.login_view = '/login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    app_key='GOOGLE',
    base_url='https://www.googleapis.com/',
    authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
    request_token_params={
        'scope': ' '.join([
            'openid',
            'email',
            'profile',  # required for OpenId Connect compliance
            'https://www.googleapis.com/auth/calendar',
        ])
    },
    access_token_url='/oauth2/v4/token')

@google.tokengetter
def get_access_token():
    return session.get('google_token')

@app.route('/login/google')
def login_google():
    callback = url_for('google_authorized', _external=True, _scheme='https')
    return google.authorize(callback=callback)

@app.route('/authorize/google')
def google_authorized():
    next_url = request.args.get('next') or url_for('index')
    data = google.authorized_response()
    if data is None:
        flash('You denied the request to sign in.')
        logger.log('User denied login request')
        return redirect(url_for('login'))
    elif isinstance(data, OAuthException):
        flash('An error occured during authentication')
        logger.exception('Received exception during google authorization %s', data)
        return redirect(url_for('login'))

    session['google_token'] = (data['access_token'], '')

    valid_id = _verify_google_id(data['id_token'])
    if valid_id is None:
        flash('An error occured during authentication')
        return redirect(url_for('login'))

    user = db.get_user_by_google(valid_id)

    if user is None:
        userdata = google.get('/oauth2/v3/userinfo').data
        user = db.add_user(
            name=userdata['name'],
            email=userdata['email'],
            google_id=valid_id)

    login_user(user, True)
    if not next_is_valid(next_url):
        flask.abort(404)
    return redirect(next_url)

def _verify_google_id(id_token):
    """
    Verifies that ``id_token`` was indeeed issued by Google to us and is not
    expired. This method is not strictly necessary currently but if we ever
    get the token from somewhere else (like the client side) this is
    important.
    """

    resp = google.get('/oauth2/v3/tokeninfo', {'id_token': id_token})
    data = resp.data
    if data['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        logger.error('Got id token from unexpected issuer %s', data['iss'])
        return None
    if float(data['exp']) <= time():
        logger.log('Login token expired')
        return None
    if data['aud'] != app.config['GOOGLE']['consumer_key']:
        logger.error("id_token's authentication domain is %s", data['aud'])
        return None
    return data['sub']


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

def next_is_valid(path):
    return not path or path.startswith('/')
