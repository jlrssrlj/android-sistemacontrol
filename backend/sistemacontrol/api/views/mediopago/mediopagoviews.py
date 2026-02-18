from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from dashboard.models import MedioPago
from .mediopagoserializer import MedioPagoSerializer


class MedioPagoListView(APIView):

    def get(self, request):
        medios = MedioPago.objects.all()
        serializer = MedioPagoSerializer(medios, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MedioPagoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
