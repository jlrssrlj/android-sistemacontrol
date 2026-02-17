from django.urls import path
from .views.proveedoresviews import ProveedorAPI
from .views.loginviews import EmpleadoLoginAPI

urlpatterns = [
    path('proveedores/', ProveedorAPI.as_view(), name='proveedores'),
    path('login/', EmpleadoLoginAPI.as_view(), name='empleado_login')
]
