from .models import Wish
from rest_framework import viewsets, status
from . import serializers
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from .utils import query_search
from drf_spectacular.utils import extend_schema


class WishListPagination(PageNumberPagination):
    page_size = 8
    page_query_param = 'page'
    max_page_size = 10000


class WishViewSet(viewsets.ViewSet, WishListPagination):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.WishSerializer

    @extend_schema(responses=serializers.WishListSerializer)
    def list(self, request):

        wishes = Wish.objects.filter(owner=request.user)
        page = self.paginate_queryset(wishes, request)
        if page:
            serializer_paginated = serializers.WishListSerializer(page, many=True)
            return self.get_paginated_response(serializer_paginated.data)
        serializer = serializers.WishSerializer(wishes, many=True)
        return Response(serializer.data)

    @extend_schema(request=serializers.WishSerializer)
    def create(self, request):
        serializer = serializers.WishSerializer(data=request.data)

        if serializer.is_valid():
            serializer.validated_data['owner'] = request.user
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk: int):
        queryset = Wish.objects.filter(owner=request.user)
        instance = get_object_or_404(queryset, pk=pk)
        if instance.owner == request.user:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)

    @extend_schema(responses=serializers.WishSerializer)
    def retrieve(self, request, pk: int):
        queryset = Wish.objects.filter(owner=request.user)
        wish = get_object_or_404(queryset, pk=pk)
        serializer = serializers.WishRetrieveSerializer(wish)
        return Response(serializer.data)


@api_view(('GET',))
def search_wishes(request, query):
    res = query_search(query)
    return Response(res)
