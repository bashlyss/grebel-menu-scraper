import os

SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False  # Log SQL statements
DEBUG = True
ALL_EMAILS_GROUP = 543

SECRET_KEY = os.environ.get('SECRET_KEY', 'non-secret test key')

# Default ReCaptcha keys to Google's testing keys
RECAPTCHA_PUBLIC_KEY = os.environ.get(
    'RECAPTCHA_PUBLIC_KEY',
    '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI')
RECAPTCHA_PRIVATE_KEY = os.environ.get(
    'RECAPTCHA_PRIVATE_KEY',
    '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe')

SENDGRID_CLIENT_SECRET = os.environ.get('SENDGRID_CLIENT_SECRET', '')

# OAuth2
GOOGLE = {
    'consumer_key': os.environ.get('GOOGLE_CLIENT_ID'),
    'consumer_secret': os.environ.get('GOOGLE_CLIENT_SECRET'),
}
