from rest_framework import serializers
from .models import *
from product.models import *

from product.serializers import *



class WishListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishListItem
        fields = ['id', 'product']

class WishListSerializer(serializers.ModelSerializer):
    items = WishListItemSerializer(many=True, read_only=True)

    class Meta:
        model = WishList
        fields = ['id', 'user', 'items']



class WishListItemsSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = WishListItem
        fields = ['id', 'product']
