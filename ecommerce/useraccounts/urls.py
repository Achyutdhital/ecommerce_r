from django.urls import path
from useraccounts.views import (UserLoginView,
                            UserRegistrationAPIView,
                            UserProfileView,
                            UserChangePasswordView,
                            SendPasswordResetEmailView,
                            UserPasswordResetView,
                            LogoutView,OTPValidation,ExchangeCodeForTokenView,VerifyOTPAPIView,
                            FacebookExchangeCodeForTokenView,UserDeleteAPIView,ResendOTPAPIView
                            )    

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


# from .views import GoogleLogin

urlpatterns = [
    path('register', UserRegistrationAPIView.as_view(), name='register'),
    path('resend-otp/', ResendOTPAPIView.as_view(), name='resend-otp'),
    path('verify-otp/', VerifyOTPAPIView.as_view(), name='verify_otp'),
    path('login', UserLoginView.as_view(), name='login'),
    path('profile', UserProfileView.as_view(), name='profile'),
    path('update/profile', UserProfileView.as_view(), name='profile'),
    path('change/password', UserChangePasswordView.as_view(), name='changepassword'),
    path('forgot/password', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('otp',OTPValidation.as_view(), name="otp"),
    path('reset/password', UserPasswordResetView.as_view(), name='reset-password'),
    path('logout', LogoutView.as_view(), name='logout'),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('delete/', UserDeleteAPIView.as_view(), name='user-delete'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('auth/google/', ExchangeCodeForTokenView.as_view(), name='exchange_code_for_token'),
    path('auth/facebook/', FacebookExchangeCodeForTokenView.as_view(), name='facebook_login'),

    # path('auth/google/', GoogleLogin.as_view(), name='google_login'),
]