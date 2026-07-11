from rest_framework import serializers
from dashboard.models import Proveedor

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model= Proveedor
        fields = '__all__'
        read_only_fields = ["empresa"]
        
