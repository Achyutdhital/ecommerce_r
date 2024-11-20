from django.db import models
from product.models import Product, Stock
from useraccounts.models import User
import uuid




class WishList(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE, related_name='userWhichlist', null=True,blank=True)

    class Meta:
        ordering = ['-id']


class WishListItem(models.Model):
    wishlist = models.ForeignKey(WishList, on_delete= models.CASCADE,related_name ='items', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)

    class Meta:
        ordering =['-id']
