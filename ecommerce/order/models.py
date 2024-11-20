from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from useraccounts.models import User
from product.models import Stock,Category,SubCategory
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.db.models import Q
import datetime
from django.core.exceptions import ValidationError



phone_validator = RegexValidator(
    r'\d{3}?-?\d{3}?-?\d{4}', 'Only ten numbers and dashes allowed.')


COUPON_TYPE = [
    ('percentage', 'Percentage'),
    ('fixed_amount', 'Fixed Amount'),
]

COUPON_STATUS=(
    ('active',"Active"),
    ('deactive','Deactive')
)


DISOUNT_ON =(
    ("all_product","All Product"),
    ("category","Category"),
    ("sub_category","Sub Category"),
    ("shipping","Shipping")
)

class Coupon(models.Model):
    coupontitle = models.CharField(max_length=150, verbose_name='Coupon Title')
    coupon_code = models.CharField(max_length=50, verbose_name='Coupon Code')
    discount_on = models.CharField(
        choices=DISOUNT_ON,
        max_length=50,
        verbose_name='Discount On'
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="coupon_category")
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="coupon_sub_category")
    discount = models.FloatField(verbose_name='Discount')
    coupon_type = models.CharField(choices=COUPON_TYPE, max_length=50, verbose_name='Coupon Type')
    start_date = models.DateField(verbose_name='Start Date')
    expired_date = models.DateField(verbose_name='Expired Date')
    coupon_status = models.CharField(choices=COUPON_STATUS, max_length=50, verbose_name='Coupon Status')

    class Meta:
        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'

    def __str__(self):
        return f"{self.coupontitle} ({self.coupon_code})"

  
    def clean(self):
        """
        Custom validation method to check if expired_date is greater than start_date.
        """
        if self.start_date and self.expired_date and self.expired_date <= self.start_date:
            raise ValidationError({'expired_date': 'Expired date must be greater than the start date.'})

        if (self.discount_on == "category" and not self.category) or (self.discount_on == "sub_category" and not self.sub_category):
            raise ValidationError({'category': 'Please select a valid category for the "category" discount type.'})

        if self.discount_on == "category" and self.sub_category:
            raise ValidationError({'sub_category': 'You can only select a category for the "category" discount type.'})

        if self.discount_on == "sub_category" and self.category:
            raise ValidationError({'category': 'You can only select a sub-category for the "sub_category" discount type.'})

        # Set category and sub_category to None if discount_on is "all_product" or "shipping"
        if (self.discount_on == "all_product" or self.discount_on == "shipping") and self.category is not None:
            self.category = None

        if (self.discount_on == "all_product" or self.discount_on == "shipping") and self.sub_category is not None:
            self.sub_category = None



class DeliveryAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,limit_choices_to=Q(is_user=True) | Q(is_vendor=True), related_name = 'deliveryAddress', null=True,blank=True)  
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    company_name = models.CharField(max_length=150)
    country_region= models.CharField(max_length=150)
    street_address = models.CharField(max_length=150)
    apartment_number = models.CharField(max_length=150, null=True, blank =True)
    state = models.CharField(max_length=150)
    town_city = models.CharField(max_length=150)
    zip_code = models.CharField(max_length=150)
    phone= models.CharField(max_length=150)
    email = models.EmailField()
    set_default = models.BooleanField(default=False)
    
    def __str__(self):
        return self.first_name + " "+self.last_name

    def save(self, *args, **kwargs):
        if self.set_default:
            DeliveryAddress.objects.filter(user=self.user).exclude(id=self.id).update(set_default=False)
        super().save(*args, **kwargs)

    


class Order(models.Model):
    PAYMENT_CHOICES = [('credit', 'Credit'),('cod', 'Cash on Delivery')]

    ORDER_STATUS_CHOICES = [('pending', 'Pending'),
                            ('accept','Accept'),
                            ('on_delivery', 'On Delivery'), 
                            ('delivered', 'Delivered')
                            ]

    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'orders')
    payment_method = models.CharField(max_length = 50, choices = PAYMENT_CHOICES)
    order_status = models.CharField(max_length = 50, choices = ORDER_STATUS_CHOICES, default="pending")
    delivered_date = models.DateField(null=True, blank=True, editable=False)
    itemsPrice= models.FloatField(null=True, blank=True)
    shippingPrice = models.FloatField(null=True, blank=True)
    taxPrice = models.FloatField(null=True, blank=True)
    totalPrice = models.FloatField(null=True, blank=True)
    isPaid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    devlivery_agent = models.ForeignKey(User, on_delete=models.CASCADE,limit_choices_to={'is_delivery_agent': True}, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    delivery_address = models.ForeignKey(DeliveryAddress, on_delete= models.SET_NULL, null =True, blank=True, related_name= 'deliver_address')

    def __str__(self):
        return f"Order {self.id} - {self.user}"
    
    def get_total_cost(self):
        return sum([item.get_cost() for item in self.items.all()])


    def total_quantity(self):
        return sum([item.quantity for item in self.items.all()])
    
    def clean(self):
        if self.devlivery_agent and not all(item.order_item_status == 'ready_to_pick_up' for item in self.items.all()):
            raise ValidationError({'devlivery_agent': 'Cannot assign delivery agent until all order item statuses are Ready To Pickup'})
    
    def save(self, *args, **kwargs):
        if self.order_status == 'delivered' and not self.delivered_date:
            self.delivered_date = timezone.now().date()
        super().save(*args, **kwargs)

        



class OrderItem(models.Model):
    ORDER_ITEM_STATUS_CHOICES = [('pending', 'Pending'),
                            ('accept','Accept'),
                            ('ready_to_pick_up', 'Ready To Pickup'), 
                            ('picked', 'Picked'),
                            ]
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    product = models.ForeignKey('product.Product', on_delete=models.SET_NULL, null=True, blank=True, related_name="order_product")
    attribute = models.ForeignKey(Stock, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    order_item_status = models.CharField(max_length = 50, choices = ORDER_ITEM_STATUS_CHOICES, default ='pending')
    ordered_date = models.DateTimeField(auto_now=True)
    item_price= models.PositiveIntegerField(default=1)
    def __str__(self):
        return f"{self.product.product_name} - order item id: {self.id} - quantity: {self.quantity}"

    def get_cost(self):
        return self.product.current_price * self.quantity

    
    class Meta:
        ordering = ('-ordered_date',)


class ReturnOrderItem(models.Model):
    RETURN_ITEM_STATUS =[('pending', 'Pending'),
                    ('accept','Accept'),
                    ('picked', 'Picked')
                    ]
    RETURN_STATUS=[
        ('partially_return','Partially Return'),
        ('complte_return','Complete Return')
    ]

    order_item = models.ForeignKey('OrderItem', on_delete=models.CASCADE, related_name='return_order_items')
    return_quantity = models.IntegerField(default=0)
    product_image = models.ImageField(upload_to='returnproduct/', null=True, blank=True)
    retun_item_status = models.CharField(max_length =50, choices=RETURN_ITEM_STATUS, default = "pending")
    return_status = models.CharField(max_length =50, choices =RETURN_STATUS, null=True, blank=True, editable=False)
    return_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Return for OrderItem {self.order_item.id} - Quantity: {self.return_quantity}"
    

    def clean(self):
        super().clean()
        
        if self.return_quantity > self.order_item.quantity:
            raise ValidationError({'return_quantity': 'Return quantity must be less than or equal to order item quantity'})
        
    

class State(models.Model):
    state_name = models.CharField(max_length=150)

    def __str__(self):
        return self.state_name

class City(models.Model):
    state = models.ForeignKey(State, on_delete= models.CASCADE, related_name ='state_cities')
    city_name = models.CharField(max_length=150)

    def __str__(self):
        return self.city_name

class ShippingManagement(models.Model):
    zone_name = models.CharField(max_length=50)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='shipping_management')
    cities = models.ManyToManyField(City, related_name='shipping_management_cities')
    shipping_price = models.CharField(max_length=150, null=True, blank=True)


    def __str__(self):
        city_names = ', '.join(str(city.city_name) for city in self.cities.all())
        return f"{self.zone_name} - {self.state.state_name} - {city_names}"