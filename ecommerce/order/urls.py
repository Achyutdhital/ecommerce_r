from django.urls import path
from .views import OrderCreateAPIView,DeliveryAddressListView
from . import views


urlpatterns = [
    path('create/', OrderCreateAPIView.as_view(), name='order-create'),
    # Add more URLs for other operations like retrieving orders, updating, etc.
    path('delivery/list/', DeliveryAddressListView.as_view(), name='delivery-list'),
    path('delivery-address/create/', views.create_delivery_address),
    path('delivery-address/update/<int:pk>/', views.update_delivery_address),
    path('delivery-address/delete/<int:pk>/', views.delete_delivery_address),
]
