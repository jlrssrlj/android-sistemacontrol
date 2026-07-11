from rest_framework import serializers
from dashboard.models import MedioPago


class MedioPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedioPago
        fields = "__all__"
        read_only_fields = ["empresa"]
