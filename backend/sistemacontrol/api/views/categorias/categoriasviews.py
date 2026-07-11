from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from dashboard.models import Categoria
from dashboard.empresa import obtener_empresa_requerida
from .categoriasserializer import CategoriasSerializer


def es_admin(user):
    try:
        return user.empleado.rol.nombre == "Administrador"
    except:
        return False


class CategoriasView(APIView):
    permission_classes = [IsAuthenticated]

    # 🔹 LISTAR (ADMIN Y CAJERO)
    def get(self, request):
        empresa = obtener_empresa_requerida(request.user)
        categoria = Categoria.objects.filter(empresa=empresa)
        serializer = CategoriasSerializer(categoria, many=True)
        return Response(serializer.data)

    # 🔹 CREAR (SOLO ADMIN)
    def post(self, request):
        if not es_admin(request.user):
            return Response(
                {"error": "Solo el administrador puede crear una Categoria"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = CategoriasSerializer(data=request.data)
        if serializer.is_valid():
            empresa = obtener_empresa_requerida(request.user)
            serializer.save(empresa=empresa)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 🔹 EDITAR (SOLO ADMIN)
    def put(self, request, pk):
        if not es_admin(request.user):
            return Response(
                {"error": "Solo el administrador puede editar una categoria"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            empresa = obtener_empresa_requerida(request.user)
            medio = Categoria.objects.get(pk=pk, empresa=empresa)
        except Categoria.DoesNotExist:
            return Response(
                {"error": "Categoria no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CategoriasSerializer(medio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 🔹 ELIMINAR (SOLO ADMIN)
    def delete(self, request, pk):
        if not es_admin(request.user):
            return Response(
                {"error": "Solo el administrador puede eliminar una Categoria"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            empresa = obtener_empresa_requerida(request.user)
            medio = Categoria.objects.get(pk=pk, empresa=empresa)
        except Categoria.DoesNotExist:
            return Response(
                {"error": "Categoria no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )

        medio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
