import os

SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False  # Log SQL statements
DEBUG = True
SECRET_KEY = 'This is a dummy string'

# Recaptcha keys - need to sign up to get them so this validates

RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''

# OAuth2
GOOGLE = {
    'consumer_key': os.environ.get('GOOGLE_CLIENT_ID'),
    'consumer_secret': os.environ.get('GOOGLE_CLIENT_SECRET'),
}
