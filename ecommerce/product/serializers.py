from rest_framework import serializers
from .models import *

# banner serializer
class BannarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bannar
        fields = '__all__'


# for childcategory + Product 

class ChildCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildCategory
        fields = ['id', 'child_category_name', 'image', 'child_category_slug', 'ordering']

# for subcategory + Product 
class SubCategorySerializer(serializers.ModelSerializer):
    subCategories = ChildCategorySerializer(many=True, read_only=True)

    class Meta:
        model = SubCategory
        fields = ['id', 'sub_category_name', 'image', 'sub_category_slug', 'ordering', 'subCategories']


# for subcategory without child category + Product 
class SubCategorysSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'sub_category_name', 'image', 'ordering', 'sub_category_slug']


class CategorySerializer(serializers.ModelSerializer):
    mainCategory = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'category_name', 'category_image', 'category_slug', 'ordering', 'mainCategory']


class CategorysSerializer(serializers.ModelSerializer):
    mainCategory = SubCategorysSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'category_name', 'category_image', 'category_slug', 'ordering', 'mainCategory']





class AttributeValueSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(source='attribute.name')

    class Meta:
        model = AttributeValue
        fields = ['id', 'attribute_name', 'value']

class StockSerializer(serializers.ModelSerializer):
    attributes = AttributeValueSerializer(many=True, read_only=True)

    class Meta:
        model = Stock
        fields = ['id', 'quantity', 'addprice', 'file', 'attributes']

        ref_name = 'StockSerializer1'



class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['file']



class ProductSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True, read_only=True, source='product')
    category_name = serializers.CharField(source='category.category_name', read_only=True)
    sub_category_name = serializers.CharField(source='sub_category.sub_category_name', read_only=True)
    product_stock = StockSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'category_name', 'sub_category_name', 'product_name','is_popular','is_featured','previous_price', 'current_price',
            'image', 'description', 'product_views', 'created_date', 'updated_date', 'prod_slug',
            'product_owner', 'product_images','product_stock'
        ]




class CategoriesSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True, source='product_ctg')

    class Meta:
        model = Category
        fields = ['id', 'category_name', 'category_image', 'category_slug', 'ordering', 'products']



class SubCategoriesSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True, source='subcategory')
    class Meta:
        model = SubCategory
        fields = ['id', 'sub_category_name', 'image', 'ordering', 'sub_category_slug','products']




class ChildCategoriesSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True, source='childcategory')
    class Meta:
        model = ChildCategory
        fields = ['id', 'child_category_name', 'image', 'child_category_slug', 'ordering','products']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class ProductDetailSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True, read_only=True, source='product')
    product_stock = StockSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.category_name', read_only=True)
    sub_category_name = serializers.CharField(source='sub_category.sub_category_name', read_only=True)
    comment = CommentSerializer(many=True, read_only=True, source='comments')
    related_products = serializers.SerializerMethodField()


    # image = serializers.ImageField(use_url=True)

    class Meta:
        model = Product
        fields = [
            'id', 'category_name', 'sub_category_name', 'product_name', 'previous_price', 'current_price'
            ,'description', 'product_views', 'created_date', 'updated_date', 'prod_slug',
            'product_owner', 'product_images', 'product_stock','comment','related_products'
        ]
    def get_related_products(self, obj):
        related_products = Product.objects.filter(sub_category=obj.sub_category).exclude(id=obj.id)[:5]  # Get up to 5 related products
        return ProductSerializer(related_products, many=True).data



class FlashItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    

    class Meta:
        model = FlashItem
        fields = ['product', 'discount_percentage']

class FlashSellSerializer(serializers.ModelSerializer):
    flash_items = FlashItemSerializer(many=True, source='flashid')


    class Meta:
        model = FlashSell
        fields = ['id', 'name', 'start_date', 'end_date', 'flash_items']



from rest_framework import serializers
# from .models import Product, Attribute, AttributeValue

class AttributeValuessSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = ['attribute', 'value']

class ProducttSerializer(serializers.ModelSerializer):
    attributes = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_attributes(self, obj):
        return AttributeValuessSerializer(obj.attributevalue_set.all(), many=True).data


class StockSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    attributes = AttributeValueSerializer(many=True)

    class Meta:
        model = Stock
        fields = '__all__'
        ref_name = 'StockSerializer2'