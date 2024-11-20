from django.contrib import admin
from . models import InventoryManagement

class InventoryManagementAdmin(admin.ModelAdmin):
    model = InventoryManagement
    list_display =['product','sku','stock','sold']
admin.site.register(InventoryManagement,InventoryManagementAdmin)