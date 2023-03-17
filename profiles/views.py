from users.models import Account
from rest_framework.viewsets import ViewSet
from django.shortcuts import get_object_or_404
from . import serializers
from rest_framework.response import Response
from friendship.models import FriendList
from rest_framework import status
from . import utils
from wishes.models import Wish
from rest_framework.pagination import PageNumberPagination
from wishes.serializers import WishListSerializer


class ProfilePagination(PageNumberPagination):
    page_size = 8
    page_query_param = 'page'
    max_page_size = 100


class ProfileViewSet(ViewSet, ProfilePagination):

    def update(self, request, pk):
        wish = Wish.objects.get(pk=pk)
        if not wish.liked_by:
            wish.liked_by = request.user
            wish.save()
        elif wish.liked_by == request.user:
            wish.liked_by = None
            wish.save()
            return Response({'message': 'like removed'})
        return Response({'message': 'wish liked'})

    def list(self, request):
        profiles = Account.objects.all()
        serializer = serializers.ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        queryset = Account.objects.all()
        account = get_object_or_404(queryset, pk=pk)
        wishes = Wish.objects.filter(owner=account)
        are_friends = False

        if request.user == account:
            serializer = serializers.OwnProfileSerializer(account)
            return Response(serializer.data)
        if request.user.is_authenticated:
            friend_list = FriendList.objects.get(user=request.user)
            are_friends = FriendList.are_friends(friend_list, account)

        serializer = serializers.ProfileSerializer(account)
        page = self.paginate_queryset(wishes, request)
        serializer_paginated = WishListSerializer(page, many=True)

        return Response(serializer.data | {'are_friends': are_friends} | {'wishes': serializer_paginated.data})

    def partial_update(self, request, pk):

        other_user = Account.objects.get(pk=pk)
        friend_list = FriendList.objects.get(user=request.user)
        if other_user == request.user:
            return Response({'Error': 'Operation is not allowed'}, status=status.HTTP_403_FORBIDDEN)
        if other_user not in friend_list.friends.all():
            return utils.send_or_cancel_request(request.user, other_user, request)
        return utils.remove_friend(other_user, request)
