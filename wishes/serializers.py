from rest_framework import serializers
from .models import Wish


class WishListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wish
        fields = ('id', 'name', 'image', 'liked_by')


class WishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wish
        fields = ('name', 'description', 'image')


class WishRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wish
        fields = ('id', 'name', 'description', 'image', 'liked_by')
