from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # Add this import
from django.contrib.auth.mixins import LoginRequiredMixin  # Add this import
from .models import *
from .serializers import *

class AddToWishListView(LoginRequiredMixin, APIView):  # Add LoginRequiredMixin
    permission_classes = [IsAuthenticated]  # Add this line to require authentication

    def post(self, request):
        user = request.user
        product_id = request.data.get('product_id')
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        wishlist, created = WishList.objects.get_or_create(user=user)
        
        wishlist_item, created = WishListItem.objects.get_or_create(wishlist=wishlist, product=product)
        
        if created:
            return Response({"message": "Product added to wishlist"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Product already in wishlist"}, status=status.HTTP_200_OK)



class WishListItemsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlist = WishList.objects.filter(user=request.user).first()
        if not wishlist:
            return Response({"message": "Wishlist is empty"}, status=200)

        items = wishlist.items.all()
        serializer = WishListItemsSerializer(items, many=True)
        return Response(serializer.data)