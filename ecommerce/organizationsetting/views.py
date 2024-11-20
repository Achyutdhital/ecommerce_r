from rest_framework import generics
from .models import OrganizationSetting
from .serializers import OrganizationSettingSerializer

class OrganizationSettingList(generics.ListAPIView):
    queryset = OrganizationSetting.objects.all()[:1]
    serializer_class = OrganizationSettingSerializer

