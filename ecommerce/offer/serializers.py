# serializers.py

from rest_framework import serializers
from .models import Coupon
from cart.models import*


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'  # or specify fields explicitly if needed


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

