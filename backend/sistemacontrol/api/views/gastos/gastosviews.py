from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from dashboard.models import Gasto
from dashboard.empresa import obtener_empresa_requerida
from .gastosserializer import GastoSerializer

class GastoAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        empresa = obtener_empresa_requerida(request.user)
        gastos = Gasto.objects.filter(empresa=empresa)
        serializer = GastoSerializer(gastos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = GastoSerializer(data=request.data)
        if serializer.is_valid():
            empresa = obtener_empresa_requerida(request.user)
            for campo in ("empleado", "proveedor", "arqueo"):
                valor = serializer.validated_data.get(campo)
                if valor and valor.empresa_id != empresa.id:
                    return Response(
                        {"error": f"{campo} no pertenece a tu empresa."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            serializer.save(empresa=empresa)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
