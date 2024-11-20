from django.shortcuts import render

# Create your views here.


# views.py
from django.conf import settings
from django.views import View
from django.http import JsonResponse
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# class StripePaymentIntentView(View):
#     def post(self, request, *args, **kwargs):
#         amount = request.POST.get('amount')  # Amount in cents
#         currency = 'usd'

#         try:
#             payment_intent = stripe.PaymentIntent.create(
#                 amount=amount,
#                 currency=currency
#             )
#             return JsonResponse({
#                 'client_secret': payment_intent.client_secret
#             })
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# @method_decorator(csrf_exempt, name='dispatch')
# class StripePaymentIntentView(View):
#     def post(self, request, *args, **kwargs):
#         amount = request.POST.get('amount')  # Amount in cents
#         currency = 'usd'

#         try:
#             payment_intent = stripe.PaymentIntent.create(
#                 amount=amount,
#                 currency=currency
#             )
#             return JsonResponse({
#                 'client_secret': payment_intent.client_secret
#             })
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
stripe.api_key = settings.STRIPE_SECRET_KEY

# @method_decorator(csrf_exempt, name='dispatch')
# class StripePaymentIntentView(View):
#     def post(self, request, *args, **kwargs):
#         amount = request.POST.get('amount')  # Amount in cents
#         currency = 'usd'

#         if not amount:
#             return JsonResponse({'error': 'Amount parameter is required.'}, status=400)

#         try:
#             payment_intent = stripe.PaymentIntent.create(
#                 amount=int(amount),  # Convert to int if necessary
#                 currency=currency
#             )
#             return JsonResponse({
#                 'client_secret': payment_intent.client_secret
#             })
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class StripePaymentIntentView(View):
    def post(self, request, *args, **kwargs):
        amount = request.POST.get('amount')  # Amount in cents
        currency = 'usd'

        if not amount:
            return JsonResponse({'error': 'Amount parameter is required.'}, status=400)

        try:
            amount = float(amount)  # Convert to float first
            amount = int(amount)  # Convert to int

            payment_intent = stripe.PaymentIntent.create(
                amount=amount,  # Now it is guaranteed to be an int
                currency=currency
            )
            return JsonResponse({
                'client_secret': payment_intent.client_secret
            })
        except ValueError:
            return JsonResponse({'error': 'Invalid amount parameter.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)