from users.models import Account
from rest_framework.viewsets import ViewSet
from django.shortcuts import get_object_or_404
from . import serializers
from rest_framework.response import Response
from friendship.models import FriendList
from rest_framework import status
from . import utils


class ProfileViewSet(ViewSet):
    def list(self, request):
        profiles = Account.objects.all()
        serializer = serializers.ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        queryset = Account.objects.all()
        account = get_object_or_404(queryset, pk=pk)
        friend_list = FriendList.objects.get(user=request.user)
        are_friends = FriendList.are_friends(friend_list, account)
        if request.user == account:
            serializer = serializers.OwnProfileSerializer(account)
            return Response(serializer.data)
        # elif are_friends is False:

        serializer = serializers.ProfileSerializer(account)
        return Response(serializer.data | {'are_friends': are_friends})

    def partial_update(self, request, pk):

        other_user = Account.objects.get(pk=pk)
        friend_list = FriendList.objects.get(user=request.user)
        if other_user == request.user:
            return Response({'Error': 'Operation is not allowed'}, status=status.HTTP_403_FORBIDDEN)
        if other_user not in friend_list.friends.all():
            return utils.send_or_cancel_request(request.user, other_user, request)
        return utils.remove_friend(other_user, request)
