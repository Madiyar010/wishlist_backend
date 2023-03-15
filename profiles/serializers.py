from rest_framework.serializers import ModelSerializer
from users.models import Account
from friendship.models import FriendList, FriendRequest


class ProfileSerializer(ModelSerializer):

    class Meta:
        model = Account
        fields = ('id', 'username', 'first_name')


class OwnProfileSerializer(ModelSerializer):

    class Meta:
        model = Account
        fields = ('id', 'email', 'username', 'first_name')


class FriendRequestSerializer(ModelSerializer):

    class Meta:
        model = FriendRequest
        fields = ('message',)
