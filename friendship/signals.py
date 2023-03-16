from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FriendRequest


@receiver(post_save, sender=FriendRequest)
def create_notification(sender, instance, created, **kwargs):
    if instance.is_active:
        instance.notifications.create(
            target=instance.receiver,
            from_user=instance.sender,
            message=f'{instance.sender.username} отправил вам заявку в друзья',
            content_type=instance,
        )
