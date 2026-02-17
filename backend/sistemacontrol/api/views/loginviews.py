# dashboard/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from dashboard.models import Empleado

class EmpleadoLoginAPI(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Usuario o contraseña incorrectos'}, status=401)

        try:
            empleado = Empleado.objects.get(user=user)
        except Empleado.DoesNotExist:
            return Response({'error': 'Empleado no registrado'}, status=401)

        if not empleado.activo:
            return Response({'error': 'Empleado inactivo'}, status=403)

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'empleado_id': empleado.id,
            'rol': empleado.rol.nombre if empleado.rol else None,
        })