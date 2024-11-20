from django.contrib import admin
from .models import WishListItem, WishList


# class WishListItemAdmin(admin.ModelAdmin):
#     model = WishListItem
#     list_display=['user','product','id']
# admin.site.register(WishListItem,WishListItemAdmin)

class WishListItemAdmin(admin.TabularInline):
    model  = WishListItem

class WishListAdmin(admin.ModelAdmin):
    inlines = [WishListItemAdmin]
    list_display = ['user']
admin.site.register(WishList, WishListAdmin)