from django.urls import path
from .views import *

urlpatterns = [
    path('bannars/', BannarListView.as_view(), name='bannar-list'),


    path('categories/', CategorysListView.as_view(), name='category-list'),
    path('all/categories/', CategoryListView.as_view(), name='categories-list'),
    path('main/categories/', CategoriesListAPIView.as_view(), name='all-category-list'),


    path('sub/categories/', SubCategoriesListAPIView.as_view(), name='all-sub-category-list'),
    path('child/categories/', ChildCategoriesListAPIView.as_view(), name='all-child-category-list'),

    
    path('categories/<slug:category_slug>/', CategoryProductsView.as_view(), name='category-products'),
    path('sub-categories/<slug:sub_category_slug>/', SubCategoryProductsView.as_view(), name='sub-category-products'),
    path('products/child-category/<slug:child_category_slug>/', ChildCategoryProductsView.as_view(), name='child-category-products'),
    path('details/<slug:prod_slug>/', ProductDetailView.as_view(), name='product-detail'),

    path('popular-products/', PopularProductListAPIView.as_view(), name='popular-products'),

    path('all/product/list', AllProductsListView.as_view(), name='all-product-list'),


    path('flashsells/', FlashSellListView.as_view(), name='flashsell-list'),
    path('flashsells/<int:id>/', FlashSellDetailView.as_view(), name='flashsell-detail'),

    path('search/', ProductSearchAPIView.as_view(), name='product-search'),

    path('filtered-stocks/', FilteredStockListAPIView.as_view(), name='filtered-stocks'),

    # path('bannars/<int:pk>/', BannarDetailView.as_view(), name='bannar-detail'),
]
