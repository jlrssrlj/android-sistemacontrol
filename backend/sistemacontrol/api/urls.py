from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from api.views.iniciologin.loginviews import CustomTokenObtainPairView
from .views.venta.ventasviews import VentaListCreateView, VentaDetailView
from .views.mediopago.mediopagoviews import MedioPagoView
from .views.gastos.gastosviews import GastoAPI
from .views.proveedores.proveedoresviews import ProveedorAPI
from .views.categorias.categoriasviews import CategoriasView
from .views.pruductos.productoviews import ProductoView

urlpatterns = [
    path('loginandroid/', CustomTokenObtainPairView.as_view(), name='loginreact'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('ventas/', VentaListCreateView.as_view(), name='venta'),
    path('ventas/<int:pk>/', VentaDetailView.as_view(), name='venta'),
    path("mediopagos/", MedioPagoView.as_view()),
    path("mediopagos/<int:pk>/", MedioPagoView.as_view()),
    path("gastos/", GastoAPI.as_view(), name='gasto'),
    path("proveedores/", ProveedorAPI.as_view(), name='proveedors'),
    path("categorias/", CategoriasView.as_view(), name='categorias'),
    path("categorias/<int:pk>/", CategoriasView.as_view()),
    path("prductos/", ProductoView.as_view(), name='productos'),
    path("productos/<int:pk>/", ProductoView.as_view()),
]
