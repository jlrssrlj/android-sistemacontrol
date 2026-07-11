from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from dashboard.models import Empleado


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user

        try:
            empleado = Empleado.objects.get(user=user)
            data["empleado_id"] = empleado.id
            data["empresa_id"] = empleado.empresa_id
            data["empresa"] = empleado.empresa.nombre if empleado.empresa else None
            data["rol"] = empleado.rol.nombre if empleado.rol else None
        except Empleado.DoesNotExist:
            data["empleado_id"] = None
            data["empresa_id"] = None
            data["empresa"] = None
            data["rol"] = None

        return data
