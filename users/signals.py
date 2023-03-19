from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Account
from friendship.models import FriendList
from django_rest_passwordreset.signals import reset_password_token_created
from django.urls import reverse
from users.tasks import send_forgot_password_message


@receiver(post_save, sender=Account)
def post_save_create_list(sender, instance, created, **kwargs):
    try:
        friend_list = FriendList.objects.get(user=instance)
    except:
        FriendList.objects.create(user=instance)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = f'http://127.0.0.1:8000{(reverse("password_reset:reset-password-request"))}?token={reset_password_token.key}'
    send_forgot_password_message.delay(email_plaintext_message, reset_password_token.user.email)
