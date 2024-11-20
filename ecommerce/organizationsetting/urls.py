from django.urls import path
from .views import OrganizationSettingList

urlpatterns = [
    path('settings/', OrganizationSettingList.as_view(), name='organization-setting-list'),
]
