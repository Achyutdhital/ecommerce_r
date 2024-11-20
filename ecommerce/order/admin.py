from django.contrib import admin

from .models import Order, OrderItem,ReturnOrderItem,Coupon,DeliveryAddress,State,City,ShippingManagement


class CouponAdmin(admin.ModelAdmin):
    model  = Coupon

admin.site.register(Coupon, CouponAdmin)



class DeliveryAddressAdmin(admin.ModelAdmin):
    model  = DeliveryAddress
    list_display = ['id','first_name','last_name']
admin.site.register(DeliveryAddress,DeliveryAddressAdmin)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
   


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_filter = ['payment_method', 'order_status']
    
admin.site.register(Order, OrderAdmin)


class ReturnOrderItemAdmin(admin.ModelAdmin):
    model = ReturnOrderItem
    list_display = ['id','order_item','return_quantity','retun_item_status','return_status','return_date']
admin.site.register(ReturnOrderItem,ReturnOrderItemAdmin)


class StateAdmin(admin.ModelAdmin):
    model = State
    list_display =['id','state_name']
admin.site.register(State,StateAdmin)


class CityAdmin(admin.ModelAdmin):
    model  = City
    list_display =['id','state','city_name']
admin.site.register(City,CityAdmin)

class ShippingManagementAdmin(admin.ModelAdmin):
    model = ShippingManagement
    list_display =['id','zone_name','state']
admin.site.register(ShippingManagement,ShippingManagementAdmin)

