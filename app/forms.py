from flask.ext.wtf import Form, RecaptchaField
from wtforms import BooleanField, StringField, SubmitField, PasswordField, validators

class LoginForm(Form):
    email = StringField('Email Address')
    password = PasswordField('Password')
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log in')

def _validate_password(_form, field):
    if any(ord(c) > 127 for c in field.data):
        raise validators.ValidationError('Please use only ASCII characters in your password')

class RegistrationForm(Form):
    email = StringField('Email Address', [
        validators.InputRequired(),
        validators.Length(min=6, max=80),
        validators.Email('Please enter a valid email address')])
    name = StringField('Name', [
        validators.InputRequired(),
        validators.Length(max=80)])
    password = PasswordField('New Password', [
        validators.InputRequired(),
        validators.Length(min=10),
        _validate_password])

    confirm = PasswordField('Confirm Password', [
        validators.InputRequired(),
        validators.EqualTo('password', message='Passwords must match')])
    recaptcha = RecaptchaField()
    submit = SubmitField('Sign up')
