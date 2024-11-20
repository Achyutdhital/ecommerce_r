from rest_framework import serializers
from .models import OrganizationSetting

class OrganizationSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationSetting
        fields = '__all__'
