from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from dashboard.models import Venta
from ..venta.ventaserializers  import VentaSerializer

class VentaListCreateView(APIView):

    def get(self, request):
        ventas = Venta.objects.all().order_by("-fecha")
        serializer = VentaSerializer(ventas, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = VentaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VentaDetailView(APIView):

    def get_object(self, pk):
        try:
            return Venta.objects.get(pk=pk)
        except Venta.DoesNotExist:
            return None
        
    def get(self, request, pk):
        venta = self.get_object(pk)
        if not venta:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = VentaSerializer(venta)
        return Response(serializer.data)
    
    def delete(self, request, pk):
        venta = self.get_object(pk)
        if not venta:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        venta.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        