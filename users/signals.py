from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Account
from friendship.models import FriendList


@receiver(post_save, sender=Account)
def post_save_create_list(sender, instance, created, **kwargs):
    try:
        friend_list = FriendList.objects.get(user=instance)
    except:
        FriendList.objects.create(user=instance)

