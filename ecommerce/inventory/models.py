from django.db import models
# from order.models import OrderItem
# from product.models import Product





class InventoryManagement(models.Model):
    product = models.OneToOneField('product.Product', on_delete=models.CASCADE, related_name='inventory_product')
    sku = models.CharField(max_length=255, default='', null=True, blank=True)
    stock = models.IntegerField(default=0,null=True, blank=True)
    sold = models.IntegerField(default=0,null=True, blank=True)  

    # def save(self, *args, **kwargs):
    #     total_sold = OrderItem.objects.filter(product=self.product).aggregate(total_sold=models.Sum('quantity'))['total_sold']
    #     total_sold = total_sold or 0

    #     self.stock = self.product.totalstock()
    #     self.sold = total_sold

    #     self.sku = self.product.prod_slug

    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} - SKU: {self.sku}, Stock: {self.stock}, Sold: {self.sold}"
