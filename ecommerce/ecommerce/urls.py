"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static



from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="E-Commerce API",
        default_version='v1',
        description="E-Commerce API",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="abcd@gmail.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),

    path('',include('dashboard.urls')),


    path('api/v1/user/',include('useraccounts.urls')),
    path('',include('dashboard.urls')),

    path('admin/', admin.site.urls),
    path('api/v1/product/',include('product.urls')),
    path('api/v1/cart/',include('cart.urls')),
    path('api/v1/wishlist/',include('wishlist.urls')),
    path('api/v1/order/',include('order.urls')),
    path('api/v1/payment/',include('payment.urls')),
    path('api/v1/organization/',include('organizationsetting.urls')),


    #auth
  
    # path('accounts/', include('allauth.urls')),
    # path('auth/', include('dj_rest_auth.urls')),
    # path('auth/registration/', include('dj_rest_auth.registration.urls')),
    

    #documentation
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
  

]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
