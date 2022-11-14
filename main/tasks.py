from django.core.mail import mail_managers, send_mail

from shop.celery import app
from config.models import Config


# @app.task
# def send_contact_form(email, text):
#     mail_managers('Contact form', f'From: {email}\n{text}')

@app.task
def send_contact_form(email, text):
    contact_mail = Config.load().contact_form_email
    send_mail(
        'Contact form',
        f'From: {email}\n{text}',
        email,
        [contact_mail]
    )
