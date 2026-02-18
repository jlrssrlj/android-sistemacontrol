from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from api.views.iniciologin.loginviews import CustomTokenObtainPairView
from .views.venta.ventasviews import VentaListCreateView, VentaDetailView
from .views.mediopago.mediopagoviews import MedioPagoListView

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('ventas/', VentaListCreateView.as_view(), name='venta'),
    path('ventas/<int:pk>/', VentaDetailView.as_view(), name='venta'),
    path("medios-pago/", MedioPagoListView.as_view()),
]
