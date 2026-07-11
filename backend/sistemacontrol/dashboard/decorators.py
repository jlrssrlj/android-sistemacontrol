from functools import wraps
from django.shortcuts import redirect


def normalizar_rol(nombre):
    rol = (nombre or "").strip().lower()
    if rol == "admin":
        return "administrador"
    return rol


def rol_requerido(*roles_permitidos):
    def decorador(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')

            # Permitir acceso al superusuario
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            try:
                rol = normalizar_rol(request.user.empleado.rol.nombre)
            except AttributeError:
                return redirect('no_autorizado')

            if rol in [normalizar_rol(r) for r in roles_permitidos]:
                return view_func(request, *args, **kwargs)
            
            return redirect('no_autorizado')
        return _wrapped_view
    return decorador
