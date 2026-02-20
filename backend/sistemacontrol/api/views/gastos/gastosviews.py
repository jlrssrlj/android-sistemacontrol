from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from dashboard.models import Gasto
from .gastosserializer import GastoSerializer

class GastoAPI(APIView):

    def get(self, request):
        gastos = Gasto.objects.all()
        serializer = GastoSerializer(gastos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = GastoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
