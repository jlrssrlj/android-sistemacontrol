from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from dashboard.models import MedioPago
from dashboard.empresa import obtener_empresa_requerida
from .mediopagoserializer import MedioPagoSerializer


def es_admin(user):
    try:
        return user.empleado.rol.nombre == "Administrador"
    except:
        return False


class MedioPagoView(APIView):
    permission_classes = [IsAuthenticated]

    # 🔹 LISTAR (ADMIN Y CAJERO)
    def get(self, request):
        empresa = obtener_empresa_requerida(request.user)
        medios = MedioPago.objects.filter(empresa=empresa)
        serializer = MedioPagoSerializer(medios, many=True)
        return Response(serializer.data)

    # 🔹 CREAR (SOLO ADMIN)
    def post(self, request):
        if not es_admin(request.user):
            return Response(
                {"error": "Solo el administrador puede crear medios de pago"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = MedioPagoSerializer(data=request.data)
        if serializer.is_valid():
            empresa = obtener_empresa_requerida(request.user)
            serializer.save(empresa=empresa)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 🔹 EDITAR (SOLO ADMIN)
    def put(self, request, pk):
        if not es_admin(request.user):
            return Response(
                {"error": "Solo el administrador puede editar medios de pago"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            empresa = obtener_empresa_requerida(request.user)
            medio = MedioPago.objects.get(pk=pk, empresa=empresa)
        except MedioPago.DoesNotExist:
            return Response(
                {"error": "Medio de pago no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = MedioPagoSerializer(medio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 🔹 ELIMINAR (SOLO ADMIN)
    def delete(self, request, pk):
        if not es_admin(request.user):
            return Response(
                {"error": "Solo el administrador puede eliminar medios de pago"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            empresa = obtener_empresa_requerida(request.user)
            medio = MedioPago.objects.get(pk=pk, empresa=empresa)
        except MedioPago.DoesNotExist:
            return Response(
                {"error": "Medio de pago no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        medio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
