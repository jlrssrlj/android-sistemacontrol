from dashboard.models import Venta
from dashboard.decorators import rol_requerido

@rol_requerido("administrador")
def listar_ventas(empresa):
    """
    Retorna un queryset con las ventas ordenadas por fecha descendente,
    con select_related para optimizar consultas.
    """
    return Venta.objects.filter(empresa=empresa).select_related('empleado', 'cliente').order_by('-fecha')
