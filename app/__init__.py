import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('settings')
if 'GREBEL_MENU_SETTINGS' in os.environ:
    app.config.from_envvar('GREBEL_MENU_SETTINGS')

sa = SQLAlchemy(app)
