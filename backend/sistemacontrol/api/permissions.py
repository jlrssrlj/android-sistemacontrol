from rest_framework.permissions import BasePermission
from dashboard.models import Empleado

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        try:
            empleado = Empleado.objects.get(user=request.user)
            return empleado.rol and empleado.rol.nombre == "Administrador"
        except Empleado.DoesNotExist:
            return False