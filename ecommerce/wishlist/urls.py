from django.urls import path
from .views import *

urlpatterns = [
    # Other URL patterns
    path('add/', AddToWishListView.as_view(), name='add-to-wishlist'),
    path('items/', WishListItemsView.as_view(), name='wishlist-items'),
]
