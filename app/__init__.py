import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('settings')
if 'GREBEL_MENU_SETTINGS' in os.environ:
    app.config.from_envvar('GREBEL_MENU_SETTINGS')
app.config['SECRET_KEY'] = 'This is a dummy string'

# Recaptcha keys - need to sign up to get them so this validates

app.config['RECAPTCHA_PUBLIC_KEY'] = ''
app.config['RECAPTCHA_PRIVATE_KEY'] = ''

db = SQLAlchemy(app)
