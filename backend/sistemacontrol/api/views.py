from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.contrib.auth.models import User
from api.views.iniciologin import UserSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def perfil(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)
