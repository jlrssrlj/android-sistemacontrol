from rest_framework import serializers
from dashboard.models import Arqueo

class ArqueoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arqueo
        fields = "__all__"
        read_only_fields = [
            "empleado",
            "empresa",
            "fecha_inicio",
            "fecha_fin",
            "monto_final",
            "diferencia",
        ]
