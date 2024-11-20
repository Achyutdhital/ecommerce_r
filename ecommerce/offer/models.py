from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from product.models import *
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

COUPON_STATUS = [
    ('active', 'Active'),
    ('inactive', 'Inactive')
]

DISCOUNT_ON = [
    ('all_product', 'All Product'),
    ('category', 'Category'),
    ('sub_category', 'Sub Category'),
    ('product', 'Product')
]

class Coupon(models.Model):
    coupontitle = models.CharField(max_length=150, verbose_name='Coupon Title')
    coupon_code = models.CharField(max_length=50, verbose_name='Coupon Code', unique=True)
    discount_on = models.CharField(
        choices=DISCOUNT_ON,
        max_length=50,
        verbose_name='Discount On'
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="offer_category")
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="offer_sub_category")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="offer_item")
    discount = models.FloatField(verbose_name='Discount')
    coupon_type = models.CharField(choices=COUPON_TYPE, max_length=50, verbose_name='Coupon Type')
    start_date = models.DateField(verbose_name='Start Date')
    expired_date = models.DateField(verbose_name='Expired Date')
    coupon_status = models.CharField(choices=COUPON_STATUS, max_length=50, verbose_name='Coupon Status')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'

    def __str__(self):
        return f"{self.coupontitle} ({self.coupon_code})"
