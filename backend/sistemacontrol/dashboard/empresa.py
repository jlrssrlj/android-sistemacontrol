from django.core.exceptions import PermissionDenied


def obtener_empresa_usuario(user):
    if not user.is_authenticated:
        return None

    try:
        return user.empleado.empresa
    except Exception:
        return None


def obtener_empresa_requerida(user):
    empresa = obtener_empresa_usuario(user)
    if empresa:
        return empresa
    raise PermissionDenied("El usuario no tiene empresa asignada.")


def filtrar_por_empresa(queryset, user):
    empresa = obtener_empresa_usuario(user)
    if empresa:
        return queryset.filter(empresa=empresa)
    if user.is_superuser:
        return queryset
    return queryset.none()
