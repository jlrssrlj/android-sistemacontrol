from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from dashboard.models import Empleado


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user

        try:
            empleado = Empleado.objects.get(user=user)
            data['empleado_id'] = empleado.id
            data['rol'] = empleado.rol.nombre if empleado.rol else None
        except Empleado.DoesNotExist:
            data['empleado_id'] = None
            data['rol'] = None

        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
