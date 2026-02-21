from rest_framework.views import APIView
from rest_framework.response import Response
from dashboard.models import Proveedor
from .productoserializer import ProductoSerializer

class ProductoAPI(APIView):
    def get(self, request):
        producto = Producto.objects.all()
        serializer = ProductoSerializer(producto, many=True)
        return Response(serializer.data)
