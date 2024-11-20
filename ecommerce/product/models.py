from django.db import models
from autoslug import AutoSlugField
from django.core.validators import MaxValueValidator, MinValueValidator
from useraccounts.models import User
from datetime import date
from datetime import timedelta
from django.utils import timezone
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from ckeditor.fields import RichTextField


class Bannar(models.Model):
    title=models.CharField(max_length=300)
    image = models.ImageField(upload_to='Bannarimage/')

    class Meta:
        ordering  =['-id']

    def __str__(self):
        return str(self.image)


class Category(models.Model):
    category_name = models.CharField(max_length=150)
    category_image = models.ImageField(upload_to='categoryimage/', null=True, blank=True)
    category_slug = AutoSlugField(populate_from='category_name', unique=True, default=None)
    ordering =models.PositiveIntegerField()


    class Meta:
        ordering =['-ordering','-id']

    def __str__(self):
        return self.category_name
    


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='mainCategory')
    sub_category_name = models.CharField(max_length=150, verbose_name='sub-category')
    image = models.ImageField(upload_to='subcategoryimage/')
    ordering =models.PositiveIntegerField()
    sub_category_slug = AutoSlugField(sub_category_name, unique=True, default=None, editable=False)
    class Meta:
        ordering =['-ordering','-id']
    
    def __str__(self):
        return self.sub_category_name


class ChildCategory(models.Model):
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='subCategories')
    child_category_name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='childcategoryimage/')
    ordering =models.PositiveIntegerField()
    child_category_slug = AutoSlugField(child_category_name, unique=True, default=None, editable=False)
    class Meta:
        ordering =['-ordering','-id']
    
    def __str__(self):
        return self.child_category_name




# @receiver(pre_delete, sender=Category)
# def prevent_delete_category(sender, instance, **kwargs):
#     if instance.mainCategory.exists():
#         subcategories = list(instance.mainCategory.all())
#         subcategory_names = ', '.join(str(subcategory) for subcategory in subcategories)
#         raise models.ProtectedError(
#             f"Cannot delete Category '{instance.category_name}' with related SubCategories: {subcategory_names}.",
#             []
#         )


''' attribute '''
class Attribute(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name



# AttributeValue model
class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='values')
    value = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.attribute.name}: {self.value}"



''' product models '''
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_ctg')
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='subcategory',null=True,blank=True)
    child_sub_category = models.ForeignKey(ChildCategory, on_delete=models.CASCADE, related_name='childcategory', null=True, blank=True)
    product_name = models.CharField(max_length=150)
    previous_price = models.DecimalField(
        max_digits=10,  
        decimal_places=2,
        null=True,
        blank=True
    )
    current_price = models.DecimalField(
        max_digits=10,  
        decimal_places=2 
    )
    image = models.ImageField(upload_to='productimages/')
    description= RichTextField()
    product_views =models.PositiveIntegerField(default=1, editable=False)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    prod_slug = AutoSlugField(populate_from='product_name', unique=True, default=None, null=True, blank=True)
    product_owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                 limit_choices_to={'is_vendor': True})
    is_featured = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False) 

    class Meta:
        ordering =['-id',]
    
    def __str__(self):
        return self.product_name


'''stock '''
class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name ='product_stock')
    attributes = models.ManyToManyField(AttributeValue, related_name='products', blank=True)
    addprice = models.PositiveIntegerField(null=True, blank=True)
    file = models.FileField(upload_to='productimages/', null =True, blank=True)
    quantity = models.PositiveIntegerField(default =1)

    def __str__(self):
        return self.product.product_name[:10] + " " + str(self.id)+ " " +str(self.quantity)
    



''' product related images '''
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='product', on_delete=models.CASCADE)
    file = models.FileField(upload_to='productimages/')

    class Meta:
        ordering = ['-id']


class Comment(models.Model):
    user =models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                 limit_choices_to={'is_user': True})
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveIntegerField( validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ])
    
 
    class Meta:
        ordering =['-id']


def default_end_date():
    return date.today() + timedelta(days=1)



class FlashSell(models.Model):
    name = models.CharField(max_length= 300)
    start_date = models.DateField(default= date.today)
    end_date = models.DateField(default=default_end_date)

    class Meta:
        ordering =['-id']


    def __str__(self):
        return self.name + " " +str(self.start_date)+"  "+str(self.end_date)
    



class FlashItem(models.Model):
    flash = models.ForeignKey(FlashSell, on_delete= models.CASCADE, related_name = 'flashid')
    product =models.ForeignKey(Product, on_delete = models.CASCADE, related_name ="flash_product")
    discount_percentage = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.product.product_name+str(self.discount_percentage)
        
        
class Offer(models.Model):
    offer_image_first = models.ImageField(upload_to='offerimage/')
    offer_image_second= models.ImageField(upload_to='offerimage/')
    offer_image_third= models.ImageField(upload_to='offerimage/', null= True, blank=True)
    start_date = models.DateField(default= date.today)
    end_date = models.DateField(default=default_end_date)
    price= models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.id)
    

class OfferItem(models.Model):
    offer_id = models.ForeignKey(Offer, on_delete= models.CASCADE, related_name ='offer_id')
    product = models.ForeignKey(Product, on_delete= models.CASCADE, related_name ='offer_product')
    discount_percentage = models.FloatField()

    def __str__(self):
        return str(self.offer_id) + self.product.product_name
        
        
        
