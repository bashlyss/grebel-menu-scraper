from flask.ext.wtf import Form, RecaptchaField
from wtforms import BooleanField, StringField, SubmitField, validators

class LoginForm(Form):
    email = StringField('Email Address', [
        validators.Length(min=6, max=80),
        validators.Email('Please enter a valid email address')])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Log in")

class RegistrationForm(Form):
    email = StringField('Email Address', [
        validators.Length(min=6, max=80),
        validators.Email('Please enter a valid email address')])
    name = StringField('Name', [validators.Length(min=1, max=80)])
    recaptcha = RecaptchaField()
    submit = SubmitField("Sign up")
