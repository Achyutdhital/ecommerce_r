from django.shortcuts import render, redirect

from django.contrib.auth import login,logout
from rest_framework import status


from useraccounts.serializers import  (UserLoginSerializer, 
                                  UserRegistrationSerializer,
                                  UserProfileSerializer,
                                  UserChangePasswordSerializer,
                                  SendPasswordResetEmailSerializer,
                                  UserPasswordResetSerializer,
                                  UserSerializer,
                                  OTPValidationSerializer
                                )
from django.contrib.auth import authenticate
from useraccounts.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from . models import User,UserOTP
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView

from rest_framework import serializers

from rest_framework.response import Response

from .serializers import SendPasswordResetEmailSerializer
from .models import UserOTP
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils import timezone
import random
import datetime

from django.db import IntegrityError
from .serializers import UserRegistrationSerializer

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import User

import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .utils import *

from django.core.mail import send_mail
from django.conf import settings




def send_otp_email(email, otp):
    subject = 'Your OTP Code'
    message = f'Your OTP code is {otp}.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)

# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }


class UserRegistrationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data, context={'request': request})
        
        # Check if the file is present in the request
        avatar_file = request.FILES.get('avatar', None)

        if serializer.is_valid():
            # Generate OTP and send email
            otp = ''.join([str(random.randint(0, 9)) for _ in range(4)])  # Generate 4-digit OTP
            
            # Assuming `send_otp_email` is a method in your serializer
            serializer.send_otp_email(serializer.validated_data['email'], otp)
            
            # Store OTP in session (for validation later)
            request.session['otp'] = otp
            
            # Convert dateofbirth to string for JSON serialization if it exists
            user_data = serializer.validated_data.copy()
            if 'dateofbirth' in user_data:
                user_data['dateofbirth'] = user_data['dateofbirth'].strftime('%Y-%m-%d')
            
            # Store validated data (without OTP) for later use in VerifyOTPAPIView
            request.session['user_data'] = user_data
            
            # Handle the file upload using Django's default storage
            if avatar_file:
                file_path = handle_uploaded_file(avatar_file)
                user_data['avatar'] = file_path
                # Update session with the file path for avatar
                request.session['avatar_file'] = file_path
            
            # Return response to prompt OTP verification
            return Response({"message": "OTP sent to your email. Please verify to complete registration."}, status=status.HTTP_200_OK)
        
        # Format the validation errors to show under the "message" key without field names
        # errors = serializer.errors if serializer.errors else "Unknown error"
        errors = list(serializer.errors.values())[0][0] if serializer.errors else "Unknown error"
        return Response({"message": "Otp Validation failed.", "error": errors}, status=status.HTTP_400_BAD_REQUEST)






class VerifyOTPAPIView(APIView):
    def post(self, request, *args, **kwargs):
        otp_received = request.data.get('otp')
        if 'otp' in request.session and request.session['otp'] == otp_received:
            user_data = request.session.get('user_data')
            avatar_file_name = request.session.get('avatar_file')

            if not user_data:
                return Response({"message": "No user data found in session."}, status=status.HTTP_400_BAD_REQUEST)

            if avatar_file_name:
                # Retrieve the file content from the saved file
                avatar_file_path = default_storage.path(avatar_file_name)
                with open(avatar_file_path, 'rb') as avatar_file:
                    user_data['avatar'] = ContentFile(avatar_file.read(), name=avatar_file_name)

            serializer = UserRegistrationSerializer(data=user_data, context={'request': request})
            if serializer.is_valid():
                try:
                    user = serializer.save()  # Save the user
                    # Clear OTP and user data from session after successful registration
                    del request.session['otp']
                    del request.session['user_data']
                    if 'avatar_file' in request.session:
                        del request.session['avatar_file']
                    
                    # Generate tokens for the user
                    tokens = get_tokens_for_user(user)
                    
                    return Response({
                        "message": "User registered successfully",
                        "tokens": tokens
                    }, status=status.HTTP_201_CREATED)
                except IntegrityError as e:
                    return Response({"message": f"IntegrityError: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    "message": "Otp Validation failed.",
                    "error": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

from django.shortcuts import get_object_or_404
from django.http import Http404

class UserLoginView(APIView):
    # renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        
        # Check if the user exists
        try:
            user = get_object_or_404(User, email=email)
        except Http404:
            return Response({
                'message': 'User not found!',
                'success': False
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Authenticate user
        authenticated_user = authenticate(email=email, password=password)
        if authenticated_user is not None:
            token = get_tokens_for_user(authenticated_user)
            login(request, authenticated_user)
            return Response({
                'user': UserSerializer(authenticated_user).data,
                'token': token,
                'message': 'Login Successfully!',
                'success': True
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'Password Invalid!',
                'success': False
            }, status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
  # renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response({'user':UserSerializer(request.user).data,'message':'User get successfully', 'success':True}, status=status.HTTP_200_OK)



  def put(self, request, formate = None):
    profile = request.user
    serializer = UserProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'user':UserSerializer(request.user).data,'message':'Update  successfully !', 'success':True}, status=status.HTTP_200_OK)




class UserChangePasswordView(APIView):
  # renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    oldpassword = serializer.validated_data['oldPassword']
    password = serializer.validated_data['newPassword']
    password2 = serializer.validated_data['confirmPassword']
    user = request.user
    if user.check_password(oldpassword):
      if password != password2:
        return Response({'message':"Password doesn't match !",'success':False}, status = status.HTTP_400_BAD_REQUEST)
      user.set_password(password)
      user.save()
      return Response({'message':'Password Change Successfully !','success':True}, status=status.HTTP_200_OK)
    return Response({'message':"Old Password does not match !",'success':False}, status=status.HTTP_400_BAD_REQUEST)
    
class SendPasswordResetEmailView(APIView):
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']

            # Custom validation logic
            if not User.objects.filter(email=email).exists():
                return Response({'message': 'You are not a Registered User'}, status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))

            otp_code = str(random.randint(1000, 9999))

            expiration_time = timezone.now() + datetime.timedelta(minutes=5)

            userotp = UserOTP.objects.filter(user=user).first()
            if userotp:
                userotp.otp_code = otp_code
                userotp.otp_code_expiration = expiration_time
                userotp.save()
            else:
                userotp = UserOTP.objects.create(user=user, otp_code=otp_code, otp_code_expiration=expiration_time)

            # Send the email with the OTP
            body = f'Your OTP code for password reset is: {otp_code}'
            data = {
                'subject': 'Reset Your Password',
                'body': body,
                'to_email': user.email
            }

            # Send email using your Util class
            Util.send_email(data)

            return Response({'message': 'An OTP code has been sent to your email. Please check your email and use the code to reset your password'}, status=status.HTTP_200_OK)
        
        # If serializer is not valid, return validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OTPValidation(APIView):
    def post(self, request, format=None):
        serializer = OTPValidationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            response_data = {'message': 'OTP code validated successfully!', 'success': True, 'user_id': user.id}
            return Response(response_data, status=status.HTTP_200_OK)

        else:
            return Response({'message': 'OTP code validation failed!', 'success': False}, status=status.HTTP_400_BAD_REQUEST)



class ResendOTPAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Retrieve the email from the request data
        email = request.data.get('email')

        if email:
            # Generate a new OTP
            otp = ''.join([str(random.randint(0, 9)) for _ in range(4)])  # Generate 4-digit OTP
            
            # Assuming you have a method to send the OTP email
            send_otp_email(email, otp)
            
            # Store the new OTP in session (for validation later)
            request.session['otp'] = otp
            
            return Response({"message": "New OTP sent to your email."}, status=status.HTTP_200_OK)
        
        return Response({"message": "Email is required to resend OTP."}, status=status.HTTP_400_BAD_REQUEST)

from django.utils import timezone
class UserPasswordResetView(APIView):
    def post(self, request, format=None):
        user_id = request.data.get('user_id')  
        user = User.objects.get(id=user_id)
        password_reset_serializer = UserPasswordResetSerializer(data=request.data, context={'user': user})
        
        if password_reset_serializer.is_valid():
            new_password = password_reset_serializer.validated_data['newPassword']
            confirm_password = password_reset_serializer.validated_data['confirmPassword']

            if new_password != confirm_password:
                return Response({'message': 'New password and confirm password do not match.', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

            userotp = UserOTP.objects.get(user=user)
            if userotp.otp_code_expiration is not None and userotp.otp_code_expiration < timezone.now():
                return Response({'message': 'OTP code has expired.', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

            # Reset the password for the user
            user.set_password(new_password)
            user.save()

            return Response({'message': 'Password reset successfully!', 'success': True}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Failed to reset the password!', 'success': False}, status=status.HTTP_400_BAD_REQUEST)



# logout User
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        print("Received refresh token:", refresh_token)

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                print("Successfully logged out.")
                return Response({"message": "Successfully logged out."})
            except Exception as e:
                print("Error during logout:", e)
                return Response({"message": "Invalid token or token expired."}, status=400)
        else:
            print("Refresh token not provided.")
            return Response({"message": "Refresh token not provided."}, status=400)
            



# # views.py
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# from dj_rest_auth.registration.views import SocialLoginView
import requests
# your_app/views.py



import requests
# from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

# class ExchangeCodeForTokenView(APIView):
#     def post(self, request, *args, **kwargs):
#         code = request.data.get('code')
#         if not code:
#             return Response({"message": "Authorization code is required"}, status=status.HTTP_400_BAD_REQUEST)

#         # Exchange code for access_token and id_token
#         token_url = 'https://oauth2.googleapis.com/access_token'
#         data = {
#             'code': code,
#             'client_id': 'YOUR_GOOGLE_CLIENT_ID',
#             'client_secret': 'YOUR_GOOGLE_CLIENT_SECRET',
#             'redirect_uri': 'http://localhost:3000',  # This should match your frontend's redirect URI
#             'grant_type': 'authorization_code'
#         }
#         token_response = requests.post(token_url, data=data)
#         token_data = token_response.json()

#         access_token = token_data.get('access_token')
#         id_token = token_data.get('id_token')

#         if not access_token or not id_token:
#             return Response({"message": "Failed to obtain access token and ID token"}, status=status.HTTP_400_BAD_REQUEST)

#         # Now send the id_token to the SocialLoginView for further processing
#         request.data['access_token'] = access_token
#         request.data['id_token'] = id_token

#         google_login_view = GoogleLogin.as_view()(request._request, *args, **kwargs)
#         return google_login_view

# class GoogleLogin(SocialLoginView):
#     adapter_class = GoogleOAuth2Adapter




# your_app/views.py



import requests

class FacebookExchangeCodeForTokenView(APIView):
    def post(self, request, *args, **kwargs):
        code = request.data.get('code')
        if not code:
            return Response({"message": "Authorization code is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Exchange code for access_token
        token_url = 'https://graph.facebook.com/v12.0/oauth/access_token'
        data = {
            'client_id': 'YOUR_FACEBOOK_APP_ID',
            'redirect_uri': 'http://localhost:8000/auth/facebook/callback/',  # This should match your frontend's redirect URI
            'client_secret': 'YOUR_FACEBOOK_APP_SECRET',
            'code': code
        }
        token_response = requests.get(token_url, params=data)
        token_data = token_response.json()

        access_token = token_data.get('access_token')
        if not access_token:
            return Response({"message": "Failed to obtain access token"}, status=status.HTTP_400_BAD_REQUEST)

        # Optionally, get user info
        user_info_url = 'https://graph.facebook.com/me'
        user_info_params = {
            'fields': 'id,name,email',
            'access_token': access_token
        }
        user_info_response = requests.get(user_info_url, params=user_info_params)
        user_info = user_info_response.json()

        # Handle the user info and tokens as needed (e.g., create user, store tokens)
        return Response({"access_token": access_token, "user_info": user_info}, status=status.HTTP_200_OK)




# facebookmight helop


# class FacebookExchangeCodeForTokenView(APIView):
#     def post(self, request, *args, **kwargs):
#         code = request.data.get('code')
#         if not code:
#             return Response({"message": "Authorization code is required"}, status=status.HTTP_400_BAD_REQUEST)

#         # Exchange code for access_token
#         token_url = 'https://graph.facebook.com/v12.0/oauth/access_token'
#         data = {
#             'client_id': 'YOUR_FACEBOOK_APP_ID',
#             'redirect_uri': 'http://localhost:8000/auth/facebook/callback/',  # This should match your frontend's redirect URI
#             'client_secret': 'YOUR_FACEBOOK_APP_SECRET',
#             'code': code
#         }
#         token_response = requests.get(token_url, params=data)
#         token_data = token_response.json()

#         access_token = token_data.get('access_token')
#         if not access_token:
#             return Response({"message": "Failed to obtain access token"}, status=status.HTTP_400_BAD_REQUEST)

#         # Optionally, get user info
#         user_info_url = 'https://graph.facebook.com/me'
#         user_info_params = {
#             'fields': 'id,name,email',
#             'access_token': access_token
#         }
#         user_info_response = requests.get(user_info_url, params=user_info_params)
#         user_info = user_info_response.json()

#         # Handle the user info and tokens as needed (e.g., create user, store tokens)
#         return Response({"access_token": access_token, "user_info": user_info}, status=status.HTTP_200_OK)


# goolgle may be help 
class ExchangeCodeForTokenView(APIView):
    def post(self, request, *args, **kwargs):
        code = request.data.get('code')
        if not code:
            return Response({"message": "Authorization code is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Exchange code for access_token and id_token
        token_url = 'https://oauth2.googleapis.com/access_token'
        data = {
            'code': code,
            'client_id': 'YOUR_GOOGLE_CLIENT_ID',
            'client_secret': 'YOUR_GOOGLE_CLIENT_SECRET',
            'redirect_uri': 'http://localhost:3000',  # This should match your frontend's redirect URI
            'grant_type': 'authorization_code'
        }
        token_response = requests.post(token_url, data=data)
        token_data = token_response.json()

        access_token = token_data.get('access_token')
        id_token = token_data.get('id_token')

        if not access_token or not id_token:
            return Response({"message": "Failed to obtain access token and ID token"}, status=status.HTTP_400_BAD_REQUEST)

        # Handle the tokens as needed (e.g., store in database, return to frontend)
        return Response({"access_token": access_token, "id_token": id_token}, status=status.HTTP_200_OK)


from rest_framework import generics, status

from rest_framework.permissions import IsAuthenticated
from .serializers import UserDeleteSerializer

class UserDeleteAPIView(generics.DestroyAPIView):
    serializer_class = UserDeleteSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
