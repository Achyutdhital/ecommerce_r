from django.shortcuts import render
# import generic fro restframework
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import status
# SearchFilter
from rest_framework import filters

# models
from .models import *


# serializers
from .serializers import *


import django_filters


from rest_framework import generics

# from .filters import ProductFilter
from django_filters.rest_framework import DjangoFilterBackend




class BannarListView(generics.ListAPIView):
    queryset = Bannar.objects.all()
    serializer_class = BannarSerializer



# for Homepage Navbar display
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class CategorysListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorysSerializer


# for dusplaying in the Homepage without any slug or id display all products according to category, sub category and child categry
class CategoriesListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer




class SubCategoriesListAPIView(generics.ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategoriesSerializer



class ChildCategoriesListAPIView(generics.ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategoriesSerializer



# when click on category slug display related product tothat product
class CategoryProductsView(APIView):
    def get(self, request, category_slug):
        try:
            category = Category.objects.get(category_slug=category_slug)
            # products = Product.objects.filter(category=category).order_by('ordering')
            products = Product.objects.filter(category=category)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=404)
        




# when click on childcategory slug display related product tothat product
class ChildCategoryProductsView(APIView):
    def get(self, request, child_category_slug):
        try:
            child_category = ChildCategory.objects.get(child_category_slug=child_category_slug)
            products = Product.objects.filter(child_sub_category=child_category)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        except ChildCategory.DoesNotExist:
            return Response({"error": "Child Category not found"}, status=status.HTTP_404_NOT_FOUND)


class AllProductsListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer



# when click on product slug display detail
class ProductDetailView(APIView):
    def get(self, request, prod_slug):
        try:
            product = Product.objects.get(prod_slug=prod_slug)
            serializer = ProductDetailSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)
        

# when click on subcategory slug display related product tothat product
class SubCategoryProductsView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        sub_category_slug = self.kwargs['sub_category_slug']
        return Product.objects.filter(sub_category__sub_category_slug=sub_category_slug)
    

# display all the flashsell 
class FlashSellListView(generics.ListAPIView):
    queryset = FlashSell.objects.all()
    serializer_class = FlashSellSerializer

# show detail of flassel by id
class FlashSellDetailView(generics.RetrieveAPIView):
    queryset = FlashSell.objects.all()
    serializer_class = FlashSellSerializer
    lookup_field = 'id'






# search api forthe product using name and description
class ProductSearchAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['product_name', 'description']



class PopularProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(is_popular=True)
    serializer_class = ProductSerializer



class StockFilter(django_filters.FilterSet):
    sub_category = django_filters.CharFilter(field_name='product__sub_category__sub_category_slug', lookup_expr='exact')
    attributes = django_filters.ModelMultipleChoiceFilter(
        field_name='attributes__value',
        queryset=AttributeValue.objects.all(),
        to_field_name='value',
        conjoined=True
    )

    class Meta:
        model = Stock
        fields = ['sub_category', 'attributes']

class FilteredStockListAPIView(generics.ListAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StockFilter