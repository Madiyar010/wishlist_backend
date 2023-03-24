from wishlist.celery import app
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings


@app.task
def activate_email(user_username, user_id, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string("activation_email.html", {
        'user': user_username,
        'domain': '127.0.0.1:8000',
        'uid': urlsafe_base64_encode(force_bytes(user_id)),
        'token': account_activation_token.make_token(user_id),
        "protocol": 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()


@app.task
def send_forgot_password_message(text, email_to):

    send_mail(
        'Вы отправили запрос на смену пароля!',
        text,
        settings.EMAIL_FROM,
        [email_to],
    )
