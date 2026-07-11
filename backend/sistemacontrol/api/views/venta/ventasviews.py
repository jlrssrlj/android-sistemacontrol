from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from dashboard.models import Venta
from dashboard.empresa import obtener_empresa_requerida
from ..venta.ventaserializers  import VentaSerializer

class VentaListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        empresa = obtener_empresa_requerida(request.user)
        ventas = Venta.objects.filter(empresa=empresa).order_by("-fecha")
        serializer = VentaSerializer(ventas, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = VentaSerializer(data=request.data)
        if serializer.is_valid():
            empresa = obtener_empresa_requerida(request.user)
            serializer.save(empresa=empresa)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VentaDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, empresa):
        try:
            return Venta.objects.get(pk=pk, empresa=empresa)
        except Venta.DoesNotExist:
            return None
        
    def get(self, request, pk):
        empresa = obtener_empresa_requerida(request.user)
        venta = self.get_object(pk, empresa)
        if not venta:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = VentaSerializer(venta)
        return Response(serializer.data)
    
    def delete(self, request, pk):
        empresa = obtener_empresa_requerida(request.user)
        venta = self.get_object(pk, empresa)
        if not venta:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        venta.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
