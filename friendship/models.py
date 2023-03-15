from django.db import models
from django.conf import settings


class FriendList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='friends')

    def __str__(self):
        return self.user.username

    def add_friend(self, account):
        if account not in self.friends.all():
            self.friends.add(account)

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


class FriendRequest(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

    def accept(self):
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        sender_friend_list = FriendList.objects.get(user=self.sender)

        receiver_friend_list.unfriend(self.sender)
        sender_friend_list.unfriend(self.receiver)

    def decline(self):
        self.is_active = False

    def cancel(self):
        self.is_active = False
        self.save()
