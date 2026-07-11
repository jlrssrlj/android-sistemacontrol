from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from dashboard.models import Arqueo
from dashboard.empresa import obtener_empresa_requerida
from .arqueoserializer import ArqueoSerializer

def es_admin(user):
    try:
        return user.empleado.rol.nombre == "Administrador"
    except: 
        return False
    
def es_cajero(user):
    try:
        return user.empleado.rol.nombre == "Cajero"
    except: 
        return False
    
class Arqueoview(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        empresa = obtener_empresa_requerida(request.user)
        arqueo = Arqueo.objects.filter(empresa=empresa)
        serializer = ArqueoSerializer(arqueo, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        if not (es_admin(request.user) or es_cajero(request.user)):
            return Response(
                {"error": "Solo administrador o cajero"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ArqueoSerializer(data=request.data)

        if serializer.is_valid():
            empresa = obtener_empresa_requerida(request.user)
            serializer.save(empresa=empresa, empleado=request.user.empleado)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # 👇 MUESTRA EL ERROR REAL
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
