from django.contrib import admin
from warehouse.models import*
# Register your models here.
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('warehousename', 'country', 'state', 'city', 'address', 'streetnumber', 'contact')
    search_fields = ('warehousename', 'country', 'state', 'city', 'address', 'streetnumber', 'contact')

admin.site.register(Warehouse, WarehouseAdmin)