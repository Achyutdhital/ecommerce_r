# urls.py
from django.urls import path
from .views import StripePaymentIntentView

urlpatterns = [
    path('create_payment_intent/', StripePaymentIntentView.as_view(), name='create_payment_intent'),

]
