from rest_framework_simplejwt.views import TokenObtainPairView
from .serializerslogin import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer