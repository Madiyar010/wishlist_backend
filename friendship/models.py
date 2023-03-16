from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification
from django.utils import timezone


class FriendList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='friends')
    notifications = GenericRelation(Notification)

    def __str__(self):
        return self.user.username

    def add_friend(self, account):
        if account not in self.friends.all():
            self.friends.add(account)

            content_type = ContentType.objects.get_for_model(self)
            self.notifications.create(
                target=self.user,
                from_user=account,
                message=f'Вы теперь дружите с {account.username}',
                content_type=content_type,
            )

    def remove_friend(self, account):
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, friend):
        self.remove_friend(friend)
        friend_list = FriendList.objects.get(user=friend)
        friend_list.remove_friend(self.user)
        try:
            friend_request = FriendRequest.objects.get(sender=friend, receiver=self.user)
        except:
            friend_request = FriendRequest.objects.create(sender=friend, receiver=self.user)
        friend_request.is_active = True

    def are_friends(self, friend):
        if friend in self.friends.all():
            return True
        return False

    @property
    def get_cname(self):
        return 'FriendList'


class FriendRequest(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    notifications = GenericRelation(Notification)

    def __str__(self):
        return self.sender.username

    def accept(self):
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        sender_friend_list = FriendList.objects.get(user=self.sender)

        content_type = ContentType.objects.get_for_model(self)
        receiver_notification = Notification.objects.get(target=self.receiver,
                                                         content_type=content_type,
                                                         object_id=self.id)
        receiver_notification.is_active = False
        receiver_notification.message = f'Вы приняли {self.sender.username} заявку в друзья!'
        receiver_notification.timestamp = timezone.now()
        receiver_notification.save()

        receiver_friend_list.add_friend(self.sender)

        self.notifications.create(
            target=self.sender,
            from_user=self.receiver,
            message=f'{self.receiver.username} принял вашу заявку в друзья!',
            content_type=content_type,
        )
        sender_friend_list.add_friend(self.receiver)
        self.is_active = False
        self.save()
        return receiver_notification

    def decline(self):
        self.is_active = False
        self.save()

    def cancel(self):
        self.is_active = False
        self.save()

    @property
    def get_cname(self):
        return 'FriendRequest'
