from django.contrib import admin
from . models import (Category, Product,SubCategory,
                      ProductImage,Comment,Bannar,Attribute,
                         AttributeValue,
                        Stock,FlashSell, FlashItem,
                        Offer,OfferItem,ChildCategory
                    )


from django.utils.html import format_html
from django.conf import settings

class BannarAdmin(admin.ModelAdmin):
    model  = Bannar
    list_display =['id','image', 'title']
    list_editable=['image']
    # def has_add_permission(self, request):
    #     return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
admin.site.register(Bannar,BannarAdmin)
admin.site.register(AttributeValue)
admin.site.register(Attribute)


class ChildCategoryAdmin(admin.TabularInline):
    model = ChildCategory

class SubCategoryAdmin(admin.ModelAdmin):
    inlines =[ChildCategoryAdmin]
admin.site.register(SubCategory,SubCategoryAdmin)



admin.site.register(Category)


class ProductStockAdmin(admin.TabularInline):
    model = Stock



class ProductImageAdmin(admin.TabularInline):
    model = ProductImage

class CommentAdmin(admin.TabularInline):
    model =Comment

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin,ProductStockAdmin, CommentAdmin]
    # class Media:
    #     js = ('product/js/product_admin.js',)

admin.site.register(Product, ProductAdmin)


# admin.site.register(ProductAttribute)

class FlashItemAdmin(admin.TabularInline):
    model  = FlashItem
    

class FlashSellAdmin(admin.ModelAdmin):
    inlines =[FlashItemAdmin]
admin.site.register(FlashSell, FlashSellAdmin)


# admin.site.register(Color)



#offer items
class OfferProductAdmin(admin.TabularInline):
    model =OfferItem

# offer 
class OfferAdmin(admin.ModelAdmin):
    model = Offer
    inlines =[OfferProductAdmin]
    list_display = ['display_offer_image_first','display_offer_image_second','display_offer_image_third','start_date','end_date','price']

    def display_offer_image_first(self, obj):
        offer_image_first_url = obj.offer_image_first.url if obj.offer_image_first else settings.DEFAULT_UNKNOWN_PERSON_IMAGE_URL
        return format_html('<img src="{}" width="50" height="50" />', offer_image_first_url)

    display_offer_image_first.short_description = 'offer_image_first'


    def display_offer_image_second(self, obj):
        offer_image_second_url = obj.offer_image_second.url if obj.offer_image_second else settings.DEFAULT_UNKNOWN_PERSON_IMAGE_URL
        return format_html('<img src="{}" width="50" height="50" />', offer_image_second_url)

    display_offer_image_second.short_description = 'offer_image_second'

    def display_offer_image_third(self, obj):
        offer_image_third_url = obj.offer_image_third.url if obj.offer_image_third else settings.DEFAULT_UNKNOWN_PERSON_IMAGE_URL
        return format_html('<img src="{}" width="50" height="50" />', offer_image_third_url)

    display_offer_image_third.short_description = 'offer_image_third'
admin.site.register(Offer, OfferAdmin)


