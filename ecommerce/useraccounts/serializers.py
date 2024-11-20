from rest_framework import serializers
from useraccounts.models import User,UserOTP
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from useraccounts.utils import Util
import random
import datetime
from django.utils import timezone



domain = "http://192.168.1.126:8000"

class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = User
        fields = ['id', 'name','email','phone_No','avatar','dateofbirth','gender']


    def get_image_url(self, obj):
        if obj.avatar:
          return f'{domain}{obj.avatar.url}'


from django.core.mail import send_mail
from django.conf import settings

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    otp = serializers.CharField(write_only=True, required=False)  # OTP field initially not required
    
    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2', 'avatar', 'phone_No', 'dateofbirth', 'gender', 'otp']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        otp = attrs.get('otp')
        
        if password != password2:
            raise serializers.ValidationError("Passwords don't match!")
        
        if otp:
            # Check if OTP matches the one stored in the session
            if not self.context['request'].session.get('otp') == otp:
                raise serializers.ValidationError("Invalid OTP!")
        
        return attrs
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def create(self, validated_data):
        # Remove 'password2' and 'otp' from validated_data before creating the user
        validated_data.pop('password2', None)
        validated_data.pop('otp', None)

        return User.objects.create_user(**validated_data)

    def send_otp_email(self, email, otp):
        subject = 'Verify Your Account'
        message = f'Your OTP for account verification is: {otp}'
        from_email = settings.EMAIL_HOST_USER  # Replace with your sender email
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)
# class UserRegistrationSerializer(serializers.ModelSerializer):
#     password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
#     otp = serializers.CharField(write_only=True, required=False)  # OTP field initially not required
    
#     # dateofbirth = serializers.DateField(format='%Y-%m-%d')  # Ensure dateofbirth is formatted correctly

#     class Meta:
#         model = User
#         fields = ['email', 'name', 'password', 'password2', 'avatar', 'phone_No','dateofbirth', 'gender', 'otp']
#         extra_kwargs = {
#             'password': {'write_only': True},
#         }

#     # def to_representation(self, instance):
#     #     representation = super().to_representation(instance)
#     #     # Convert dateofbirth to ISO format string
#     #     representation['dateofbirth'] = instance.dateofbirth.isoformat() if instance.dateofbirth else None
#     #     return representation



#     def validate(self, attrs):
#       password = attrs.get('password')
#       password2 = attrs.get('password2')
#       otp = attrs.get('otp')
        
#       if password != password2:
#         raise serializers.ValidationError("Password don't match !")
      

#       if otp:
#             # Check if OTP matches the one stored in the session
#             if not self.context['request'].session.get('otp') == otp:
#                 raise serializers.ValidationError("Invalid OTP!")
#       return attrs
    
#     def validate_email(self, value):
#         if User.objects.filter(email=value).exists():
#             raise serializers.ValidationError("This email is already registered.")
#         return value


#     def create(self, validate_data):
#       return User.objects.create_user(**validate_data)


#     def send_otp_email(self, email, otp):
#         subject = 'Verify Your Account'
#         message = f'Your OTP for account verification is: {otp}'
#         from_email = settings.EMAIL_HOST_USER  # Replace with your sender email
#         recipient_list = [email]
#         send_mail(subject, message, from_email, recipient_list)
# class UserRegistrationSerializer(serializers.ModelSerializer):
#   password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
#   class Meta:
#     model = User
#     fields=['email', 'name', 'password', 'password2','avatar', 'phone_No','dateofbirth','gender']
#     extra_kwargs={
#       'password':{'write_only':True}
#     }

  # def validate(self, attrs):
  #   password = attrs.get('password')
  #   password2 = attrs.get('password2')
  #   if password != password2:
  #     raise serializers.ValidationError("Password don't match !")
  #   return attrs

  # def create(self, validate_data):
  #   return User.objects.create_user(**validate_data)



class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = User
    fields = ['email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'name','phone_No','avatar','dateofbirth','gender']


class UserChangePasswordSerializer(serializers.Serializer):
  oldPassword = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  newPassword = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  confirmPassword = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['oldPassword', 'newPassword','confirmPassword']
    

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
# class SendPasswordResetEmailSerializer(serializers.Serializer):
#   email = serializers.EmailField(max_length=255)
#   class Meta:
#     fields = ['email']

#   def validate(self, attrs):
#     email = attrs.get('email')
#     if User.objects.filter(email=email).exists():
#       user = User.objects.get(email = email)
#       uid = urlsafe_base64_encode(force_bytes(user.id))

#       otp_code = str(random.randint(1000, 9999))

#       expiration_time = timezone.now() + datetime.timedelta(minutes=5)

#       userotp =UserOTP.objects.filter(user=user).first()
#       if userotp:
#         userotp.otp_code = otp_code
#         userotp.otp_code_expiration = expiration_time
#         userotp.save()
#       else:
#          userotp = UserOTP.objects.create(user=user,otp_code = otp_code,otp_code_expiration = expiration_time)

#       # Send the email with the OTP
#       body = f'Your OTP code for password reset is: {otp_code}'
#       data = {
#           'subject': 'Reset Your Password',
#           'body': body,
#           'to_email': user.email
#       }

#       # Send email using your Util class
#       Util.send_email(data)

#       return attrs
#     else:
#       raise serializers.ValidationError('You are not a Registered User')




# otp validatin serializer
class OTPValidationSerializer(serializers.Serializer):

  otp_code = serializers.CharField(max_length=150, style={'type': 'number'}, write_only=True)

  class Meta:
      fields = ['otp_code']

  def validate(self, attrs):
      try:
          otp_code = attrs.get('otp_code')
          otp_details = UserOTP.objects.get(otp_code=otp_code)
          userotp = UserOTP.objects.get(user=otp_details.user.id)

          if userotp.otp_code != otp_code:
              raise serializers.ValidationError('Invalid OTP code')

          if userotp.otp_code_expiration is not None and userotp.otp_code_expiration < timezone.now():
              raise serializers.ValidationError('OTP code has expired')

          attrs['user'] = otp_details.user 
          return attrs
      except UserOTP.DoesNotExist:
          raise serializers.ValidationError('Invalid OTP code')
      except Exception as e:
          raise serializers.ValidationError('Failed to validate OTP code')

  



class UserPasswordResetSerializer(serializers.Serializer):
  newPassword = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
  confirmPassword = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

  class Meta:
      fields = ['newPassword', 'confirmPassword']

  def validate(self, attrs):
      try:
          newPassword = attrs.get('newPassword')
          confirmPassword = attrs.get('confirmPassword')

          if newPassword != confirmPassword:
              raise serializers.ValidationError("Password and Confirm Password don't match")
      
          return attrs
      except Exception as e:
          raise serializers.ValidationError('Failed to reset the password')
      




class UserDeleteSerializer(serializers.Serializer):
    password = serializers.CharField()

    def validate(self, attrs):
        user = self.context['request'].user
        if not user.check_password(attrs.get('password')):
            raise serializers.ValidationError('Incorrect password.')
        return attrs