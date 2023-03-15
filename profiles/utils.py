from rest_framework.response import Response
from rest_framework import status
from . import serializers
from friendship.models import FriendRequest, FriendList


def send_or_cancel_request(user, other_user, request):

    serializer = serializers.FriendRequestSerializer(data=request.data)

    if serializer.is_valid():
        try:
            friends_request = FriendRequest.objects.get(sender=request.user, receiver=other_user)
        except:
            serializer.validated_data['sender'] = request.user
            serializer.validated_data['receiver'] = other_user
            serializer.save()
            return Response({'Friend request': 'Sent'})
        if not friends_request.is_active:
            friends_request.is_active = True
            friends_request.message = serializer.validated_data['message']
            friends_request.save()
            return Response({'Friend request': 'Sent'})
        friends_request.cancel()
        return Response({'Friend request': 'Canceled'})


def remove_friend(other_user, request):
    own_friend_list = FriendList.objects.get(user=request.user)
    own_friend_list.unfriend(other_user)
