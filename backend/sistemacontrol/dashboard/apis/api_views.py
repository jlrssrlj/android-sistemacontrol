from rest_framework.views import APIView
from rest_framework.response import Response
from dashboard.models import Proveedor
from dashboard.serializers import ProveedorSerializer

class ProveedorAPI(APIView):
    def get(self, request):
        proveedores = Proveedor.objects.all()
        serializer = ProveedorSerializer(proveedores, many=True)
        return Response(serializer.data)
