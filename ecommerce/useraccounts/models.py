from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import Permission
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, password2=None,**extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        return self.create_user(email, name, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female')
   
]

    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=200)
    dateofbirth = models.DateField(blank=True, null=True) 
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    username = models.CharField(max_length=200,null=True, blank=True)
    is_user = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_delivery_agent = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  
    phone_No = models.CharField(max_length=150)
    avatar = models.FileField(upload_to="avatarimage/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_No']

    def __str__(self):
      return self.name
    
    # def has_perm(self, perm, obj=None):
    #     return self.is_admin
    
    # def has_module_perms(self, app_label):
    #     return True
    
    # @property
    # def is_staff(self):
    #     return self.is_admin +self.is_vendor+self.is_user
    
   
    
# @receiver(pre_save, sender=User)
# def create_user_permissions(sender, instance, **kwargs):
#     if instance.pk is None and instance.is_delivery_agent:
#         change_order_status_permission = Permission.objects.get(codename='can_change_order')
#         print(change_order_status_permission)
#         instance.user_permissions.add(change_order_status_permission)
  
class UserOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_otp')
    otp_code = models.CharField(max_length=50)
    otp_code_expiration = models.DateTimeField()
    def __str__(self):
        return str(self.user.name) + str(self.otp_code)
    
    
class VendorData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,limit_choices_to={'is_vendor': True},related_name='vendor')
    phoneNo= models.PositiveBigIntegerField()
    logo=  models.ImageField(upload_to='logo/')
    address = models.CharField(max_length =50)
    business = models.CharField(max_length =30)
    national_id_image = models.ImageField(upload_to="verification_images/",null=True,blank=True)
    about_company = models.TextField()
    def __str__(self):
        return f"Verification for {self.user.name}"



