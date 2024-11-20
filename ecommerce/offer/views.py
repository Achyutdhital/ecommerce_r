# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Coupon, Product
from cart.models import *
from .serializers import CouponSerializer

class ApplyCouponAPIView(generics.GenericAPIView):
    serializer_class = CouponSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            coupon_code = serializer.validated_data['coupon_code']
            now = timezone.now()
            coupon = get_object_or_404(Coupon, coupon_code=coupon_code, start_date__lte=now, expired_date__gte=now, coupon_status='active')
            
            cart, created = Cart.objects.get_or_create(customer=request.user)  # Assuming Cart has customer field instead of user

            # Apply discount based on coupon type
            if coupon.discount_on == 'all_product':
                if coupon.coupon_type == 'percentage':
                    cart.total_price -= cart.total_price * (coupon.discount / 100)
                elif coupon.coupon_type == 'fixed_amount':
                    cart.total_price -= coupon.discount
            elif coupon.discount_on == 'category':
                products = Product.objects.filter(category=coupon.category)
                total_discount = 0
                for product in products:
                    # Adjust according to your product and discount structure
                    if coupon.coupon_type == 'percentage':
                        total_discount += product.current_price * (coupon.discount / 100)
                    elif coupon.coupon_type == 'fixed_amount':
                        total_discount += coupon.discount
                cart.total_price -= total_discount
            elif coupon.discount_on == 'sub_category':
                products = Product.objects.filter(sub_category=coupon.sub_category)
                total_discount = 0
                for product in products:
                    # Adjust according to your product and discount structure
                    if coupon.coupon_type == 'percentage':
                        total_discount += product.current_price * (coupon.discount / 100)
                    elif coupon.coupon_type == 'fixed_amount':
                        total_discount += coupon.discount
                cart.total_price -= total_discount
            elif coupon.discount_on == 'product':
                if coupon.product:
                    if coupon.coupon_type == 'percentage':
                        cart.total_price -= coupon.product.current_price * (coupon.discount / 100)
                    elif coupon.coupon_type == 'fixed_amount':
                        cart.total_price -= coupon.discount

            cart.coupon = coupon
            cart.save()

            return Response({'message': 'Coupon applied successfully!', 'cart_id': cart.cart_id}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
