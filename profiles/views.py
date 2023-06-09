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
from drf_spectacular.utils import extend_schema, extend_schema_field


class ProfilePagination(PageNumberPagination):
    page_size = 8
    page_query_param = 'page'
    max_page_size = 100


class ProfileViewSet(ViewSet, ProfilePagination):
    serializer_class = serializers.ProfileSerializer

    def update(self, request, pk: int):
        wish = Wish.objects.get(pk=pk)
        if wish.owner == request.user or (wish.liked_by and wish.liked_by != request.user):
            return Response({'message': 'not allowed'}, status=status.HTTP_403_FORBIDDEN)
        elif wish.liked_by == request.user:
            wish.liked_by = None
            wish.save()
            return Response({'message': 'like removed'})
        else:
            wish.liked_by = request.user
            wish.save()
            return Response({'message': 'wish liked'})

    @extend_schema(responses=serializers.ProfileSerializer)
    def list(self, request):
        profiles = Account.objects.all()
        serializer = serializers.ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    @extend_schema(responses=serializers.OwnProfileSerializer, request=int)
    def retrieve(self, request, pk: int):
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

    @extend_schema(request=int)
    def partial_update(self, request, pk: int):

        other_user = Account.objects.get(pk=pk)
        friend_list = FriendList.objects.get(user=request.user)
        if other_user == request.user:
            return Response({'Error': 'Operation is not allowed'}, status=status.HTTP_403_FORBIDDEN)
        if other_user not in friend_list.friends.all():
            return utils.send_or_cancel_request(request.user, other_user, request)
        return utils.remove_friend(other_user, request)
