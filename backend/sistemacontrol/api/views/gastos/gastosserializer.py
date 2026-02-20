from rest_framework import serializers
from dashboard.models import Gasto

class GastoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gasto
        fields = '__all__'