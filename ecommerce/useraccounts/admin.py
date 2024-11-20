from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import mark_safe
from useraccounts.models import User, UserOTP
class UserModelAdmin(BaseUserAdmin):
    list_display = ('id', 'email', 'name', 'avatar', 'phone_No', 'is_user', 'is_admin','is_staff')
    # list_editable=('is_staff')
    list_filter = ('is_admin','is_user')
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'phone_No', 'avatar')}),
        ('Permissions', {'fields': ('is_admin','is_delivery_agent','is_user','is_vendor','is_verified')}),  # Exclude groups and user_permissions
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email', 'id')
    filter_horizontal = ()
    def image_tag(self, obj):
        return mark_safe(f'<img src="{obj.avatar.url}" width="100" height="100">')
    image_tag.short_description = 'Avatar'
admin.site.register(User, UserModelAdmin)
admin.site.register(UserOTP)



class VendorDataAdmin(admin.ModelAdmin):
    model = VendorData
    list_display =['user','address']
admin.site.register(VendorData,VendorDataAdmin)
