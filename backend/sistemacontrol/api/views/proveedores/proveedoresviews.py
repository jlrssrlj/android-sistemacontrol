from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from dashboard.models import Proveedor
from dashboard.empresa import obtener_empresa_requerida
from .proveedoresserializer import ProveedorSerializer

class ProveedorAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        empresa = obtener_empresa_requerida(request.user)
        proveedores = Proveedor.objects.filter(empresa=empresa)
        serializer = ProveedorSerializer(proveedores, many=True)
        return Response(serializer.data)
