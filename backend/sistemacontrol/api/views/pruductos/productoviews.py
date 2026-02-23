from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from dashboard.models import Producto
from .productoserializer import ProductoSerializer


def es_admin(user):
    try:
        return user.empleado.rol.nombre == "Administrador"
    except Exception:
        return False


class ProductoView(APIView):
    permission_classes = [IsAuthenticated]

    # 🔹 LISTAR (ADMIN Y CAJERO)
    def get(self, request):
        productos = Producto.objects.all()
        serializer = ProductoSerializer(productos, many=True)  # ✅ CORREGIDO
        return Response(serializer.data)

    # 🔹 CREAR (SOLO ADMIN)
    def post(self, request):
        if not es_admin(request.user):
            return Response(
                {"error": "Solo el administrador puede crear un Producto"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 🔹 EDITAR (SOLO ADMIN)
    def put(self, request, pk):
        if not es_admin(request.user):
            return Response(
                {"error": "Solo el administrador puede editar un producto"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            producto = Producto.objects.get(pk=pk)  # ✅ renombrado
        except Producto.DoesNotExist:
            return Response(
                {"error": "Producto no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductoSerializer(producto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 🔹 ELIMINAR (SOLO ADMIN)
    def delete(self, request, pk):
        if not es_admin(request.user):
            return Response(
                {"error": "Solo el administrador puede eliminar un producto"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            producto = Producto.objects.get(pk=pk)  # ✅ renombrado
        except Producto.DoesNotExist:
            return Response(
                {"error": "Producto no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        producto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)