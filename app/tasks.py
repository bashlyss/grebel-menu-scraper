import json
import logging

from flask import render_template
import sendgrid

from app import app, sa
from app.models import User

logger = logging.getLogger(__name__)

sg = sendgrid.SendGridClient(app.config['SENDGRID_CLIENT_SECRET'])
sg_api = sendgrid.SendGridAPIClient(apikey=app.config['SENDGRID_CLIENT_SECRET'])

def notify_users(menu):
    for user in User.query.all():
        favs = _get_favs_for_week(user, menu)
        if not favs:
            return

        message = sendgrid.Mail()
        message.add_to('{} <{}>'.format(user.name, user.email))

        num_favs = len(favs)
        meal_text = 'meal' if num_favs == 1 else 'meals'
        message.set_subject(
            '{} upcoming favourite {} this week'.format(
                num_favs,
                meal_text))
        contents = render_template('email.html', user=user, favs=favs, meal_text=meal_text)
        message.set_html(contents)
        message.set_from('Grebel Menu <grebelmenu@gmail.com>')
        message.smtpapi.set_asm_group_id(app.config['ALL_EMAILS_GROUP'])
        status, msg = sg.send(message)

        logger.info('Send email with status %s containing %s', status, msg)

def _get_favs_for_week(user, menu):
    # TODO unimplemented
    return [{
        'day': 'Monday',
        'meal': 'Pesto Mozzerella Grilled Cheese',
    }]

def get_unsubscribes():
    resp = sg_api.client.asm.groups._(app.config['ALL_EMAILS_GROUP']).suppressions.get()
    emails = json.loads(resp.response_body.decode('utf-8'))

    resp = sg_api.client.suppression.unsubscribes.get()
    emails.extend(json.loads(resp.response_body.decode('utf-8')))

    subscribed = True
    if emails:
        subscribed = User.email.notin_(emails)
    User.query\
        .update({User.subscribed: subscribed}, synchronize_session=False)
    sa.session.commit()

def run_daily():
    get_unsubscribes()

def run_weekly():
    notify_users()
