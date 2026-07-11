from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.models import Empleado,Producto, Venta, DetalleVenta, MedioPago,Rol
from .services.listar_ventas import listar_ventas
from .services.usuario_service import UsuarioService
from .forms import UsuarioEmpleadoForm
from django.contrib.auth.models import User
from dashboard.decorators import rol_requerido
from dashboard.decorators import normalizar_rol
from django.utils.decorators import method_decorator
from functools import wraps
from .vistas.views_rol import Rol_views
from .vistas.views_mediopago import Mediopago_views
from .vistas.views_proveedor import Proveedores_views
from .vistas.views_gastos import Gastos_views
from .vistas.views_categoria import Categorias_views
from .vistas.views_arqueo import Arqueo_views
from .vistas.views_productos import Producto_views
from django.utils import timezone
from dashboard.models import Empleado, Venta, DetalleVenta, Producto, MedioPago, Arqueo
from django.contrib import messages
from dashboard.empresa import filtrar_por_empresa, obtener_empresa_requerida
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.db import IntegrityError, transaction
from django.utils.crypto import get_random_string
from django.conf import settings
from dashboard.models import Empresa
from django.utils.text import slugify
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.http import HttpResponse
import csv
import logging

logger = logging.getLogger(__name__)



@require_http_methods(["GET","POST"])
def principal(request):
    return render(request,'index.html')


@require_http_methods(["POST"])
def registrar_empresa(request):
    nombre = request.POST.get('nombreempleado', '').strip()
    apellido = request.POST.get('apellido', '').strip()
    correo = request.POST.get('correo', '').strip().lower()
    usuario = request.POST.get('usuario', '').strip()
    empresa_nombre = request.POST.get('empresa_nombre', '').strip()
    nit = request.POST.get('nit', '').strip()
    telefono = request.POST.get('telefono', '').strip()
    direccion = request.POST.get('direccion', '').strip()

    if not all([nombre, apellido, correo, empresa_nombre, nit]):
        messages.error(request, 'Completa los datos obligatorios del registro.')
        return redirect('home')

    if not usuario:
        usuario = correo.split('@')[0]
    usuario = slugify(usuario).replace('-', '_') or f"empresa_{get_random_string(6).lower()}"

    username_base = usuario
    contador = 1
    while User.objects.filter(username=usuario).exists():
        usuario = f"{username_base}{contador}"
        contador += 1

    password = get_random_string(12)

    try:
        with transaction.atomic():
            empresa = Empresa.objects.create(
                nombre=empresa_nombre,
                nit=nit,
                telefono=telefono,
                direccion=direccion,
                email=correo,
            )
            rol = Rol.objects.create(
                empresa=empresa,
                nombre='Administrador',
            )
            user = User.objects.create(
                username=usuario,
                first_name=nombre,
                last_name=apellido,
                email=correo,
                password=make_password(password),
                is_staff=False,
                is_superuser=False,
            )
            Empleado.objects.create(
                empresa=empresa,
                user=user,
                rol=rol,
                activo=True,
            )
    except IntegrityError:
        messages.error(request, 'Ya existe una empresa registrada con ese NIT.')
        return redirect('home')

    login_url = request.build_absolute_uri('/login/')
    mensaje = (
        f'Hola {nombre},\n\n'
        f'Tu empresa "{empresa_nombre}" fue registrada correctamente en BusinessControl.\n\n'
        f'URL de acceso: {login_url}\n'
        f'Usuario: {usuario}\n'
        f'Contraseña temporal: {password}\n\n'
        'Por seguridad, cambia esta contraseña después del primer ingreso.\n'
    )

    try:
        send_mail(
            subject='Credenciales de acceso a BusinessControl',
            message=mensaje,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[correo],
            fail_silently=False,
        )
        messages.success(request, 'Registro exitoso. Enviamos las credenciales al correo indicado.')
    except Exception:
        logger.exception('No se pudo enviar el correo de credenciales.')
        if settings.DEBUG:
            print('\n--- CREDENCIALES GENERADAS ---')
            print(mensaje)
            print('------------------------------\n')
        messages.warning(
            request,
            'Registro exitoso, pero no se pudo enviar el correo. Revisa la consola del servidor.'
        )

    return redirect('home')

@login_required
def no_autorizado(request):
    return render(request, 'no_autorizado.html')


def admin(user):
    return user.is_superuser or user.is_staff

def solo_admin(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect('login')

        # Permitir acceso a superusuarios y usuarios con is_staff
        if user.is_superuser or user.is_staff:
            return view_func(request, *args, **kwargs)

        try:
            empleado = Empleado.objects.get(user=user)
            if normalizar_rol(empleado.rol.nombre) == 'administrador':
                return view_func(request, *args, **kwargs)
        except Empleado.DoesNotExist:
            pass  # Continuamos a redirección

        return redirect('no_autorizado')
    return _wrapped_view

@login_required
@solo_admin
def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioEmpleadoForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                messages.error(request, "El usuario ya existe")
            else:
                user = UsuarioService.crear_usuario_empleado(form.cleaned_data)
                messages.success(request, f"Empleado {user.get_full_name()} creado correctamente")
                return redirect('listar_empleado')
    else:
        form = UsuarioEmpleadoForm()

    return render(request, 'crear_usuario.html', {'form': form})

@login_required
def listar_empleado(request):
    empleados = UsuarioService.obtener_empleados(request.user)
    return render(request, "listar_empleados.html", {'empleados': empleados})

@login_required
def editar_empleado(request, id):
    empleado = get_object_or_404(filtrar_por_empresa(Empleado.objects.all(), request.user), id=id)

    if request.method == 'POST':
        roles = UsuarioService.obtener_roles(request.user)
        data = {
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'activo': request.POST.get('activo') == 'on',
            'rol': get_object_or_404(roles, id=request.POST.get('rol')) if request.POST.get('rol') else None,
            'empresa': empleado.empresa,
            'is_staff': request.POST.get('is_staff') == 'on'
        }
        UsuarioService.actualizar_usuario_empleado(empleado, data, request.user.is_superuser)
        messages.success(request, 'Empleado actualizado correctamente.')
        return redirect('listar_empleado')

    roles = UsuarioService.obtener_roles(request.user)
    return render(request, 'editar_empleado.html', {'empleado': empleado, 'roles': roles})

@login_required
def eliminar_empleado(request, id):
    if request.method == 'POST':
        UsuarioService.eliminar_empleado(id, request.user)
        messages.success(request, 'Empleado eliminado correctamente.')
        return redirect('listar_empleado')

    empleado = get_object_or_404(filtrar_por_empresa(Empleado.objects.all(), request.user), id=id)
    return render(request, 'confirmar_eliminacion.html', {'empleado': empleado})

@require_http_methods(["GET","POST"])
def login_view(request):
    error = None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user= authenticate(request, username=username, password= password)
        if user is not None:
            login(request, user)
            return redirect('ventas')
        else:
            error = "usuairo o contraseña incorrecto"
    return render(request, 'login.html',{'error':error})


@require_http_methods(["GET", "POST"])
def solicitar_recuperacion_password(request):
    if request.method == "POST":
        correo = request.POST.get("correo", "").strip().lower()
        user = User.objects.filter(email__iexact=correo, is_active=True).first()

        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = request.build_absolute_uri(
                f"/recuperar-password/{uid}/{token}/"
            )
            mensaje = (
                f"Hola {user.get_full_name() or user.username},\n\n"
                "Recibimos una solicitud para recuperar tu contraseña en BusinessControl.\n\n"
                f"Ingresa a este enlace para crear una nueva contraseña:\n{reset_url}\n\n"
                "Si no solicitaste este cambio, ignora este mensaje.\n"
            )

            try:
                send_mail(
                    subject="Recuperación de contraseña - BusinessControl",
                    message=mensaje,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[correo],
                    fail_silently=False,
                )
            except Exception:
                logger.exception("No se pudo enviar el correo de recuperación.")
                if settings.DEBUG:
                    print("\n--- RECUPERACION DE CONTRASENA ---")
                    print(mensaje)
                    print("----------------------------------\n")

        messages.success(
            request,
            "Si el correo está registrado, enviaremos un enlace para recuperar la contraseña.",
        )
        return redirect("login")

    return render(request, "recuperar_password.html")


@require_http_methods(["GET", "POST"])
def cambiar_password_recuperacion(request, uidb64, token):
    UserModel = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserModel.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    token_valido = user is not None and default_token_generator.check_token(user, token)
    if not token_valido:
        return render(request, "cambiar_password_recuperacion.html", {"token_valido": False})

    if request.method == "POST":
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")

        if len(password1) < 8:
            messages.error(request, "La contraseña debe tener al menos 8 caracteres.")
        elif password1 != password2:
            messages.error(request, "Las contraseñas no coinciden.")
        else:
            user.set_password(password1)
            user.save()
            messages.success(request, "Contraseña actualizada correctamente. Ya puedes iniciar sesión.")
            return redirect("login")

    return render(request, "cambiar_password_recuperacion.html", {"token_valido": True})

@login_required
def logout_view(request):
    auth.logout(request)
    return redirect('home')


@login_required
@rol_requerido('admin', 'cajero')
def crear_venta(request):
    empresa = obtener_empresa_requerida(request.user)
    productos = Producto.objects.filter(empresa=empresa, stock__gt=0).order_by('nombre')
    medios_pago = MedioPago.objects.filter(empresa=empresa)

    if request.method == 'POST':
        medio_pago_id = request.POST.get('medio_pago')
        if not medio_pago_id:
            messages.error(request, "Por favor selecciona un medio de pago.")
            return render(request, 'ventas.html', {'productos': productos, 'medios_pago': medios_pago})

        try:
            medio_pago = MedioPago.objects.get(id=medio_pago_id, empresa=empresa)
        except MedioPago.DoesNotExist:
            messages.error(request, "Medio de pago inválido.")
            return render(request, 'ventas.html', {'productos': productos, 'medios_pago': medios_pago})

        productos_venta = []
        total = 0
        for key in request.POST.keys():
            if key.startswith('producto_id_'):
                prod_id = request.POST[key]
                cantidad_key = f'cantidad_{prod_id}'
                try:
                    cantidad = int(request.POST.get(cantidad_key, 1))
                    producto = Producto.objects.get(id=prod_id, empresa=empresa)
                    if cantidad > producto.stock:
                        messages.error(request, f"No hay suficiente stock para {producto.nombre}.")
                        return render(request, 'ventas.html', {'productos': productos, 'medios_pago': medios_pago})
                    subtotal = producto.precio * cantidad
                    total += subtotal
                    productos_venta.append({'producto': producto, 'cantidad': cantidad, 'subtotal': subtotal})
                except (Producto.DoesNotExist, ValueError):
                    messages.error(request, "Datos de producto inválidos.")
                    return render(request, 'ventas.html', {'productos': productos, 'medios_pago': medios_pago})

        if not productos_venta:
            messages.error(request, "No has agregado productos a la venta.")
            return render(request, 'ventas.html', {'productos': productos, 'medios_pago': medios_pago})

        empleado = Empleado.objects.get(user=request.user, empresa=empresa)

        # Obtener arqueo abierto del empleado
        arqueo_abierto = Arqueo.objects.filter(empresa=empresa, empleado=empleado, fecha_fin__isnull=True).first()
        if not arqueo_abierto:
            messages.error(request, "No tienes un arqueo abierto. Debes abrir un arqueo antes de registrar ventas.")
            return render(request, 'ventas.html', {'productos': productos, 'medios_pago': medios_pago})

        # Crear la venta con arqueo y medio de pago
        venta = Venta.objects.create(
            empresa=empresa,
            empleado=empleado,
            arqueo=arqueo_abierto,
            total=total,
            medio_pago=medio_pago,
            fecha=timezone.now(),
        )

        for item in productos_venta:
            DetalleVenta.objects.create(
                venta=venta,
                producto=item['producto'],
                cantidad=item['cantidad'],
                precio_unitario=item['producto'].precio
            )
            # Actualiza stock
            item['producto'].stock -= item['cantidad']
            item['producto'].save()

        messages.success(request, f"Venta registrada exitosamente. Total: ${total:.2f}")
        return redirect('ventas')

    return render(request, 'ventas.html', {'productos': productos, 'medios_pago': medios_pago})


@method_decorator(rol_requerido('admin'), name='dispatch')
class historial_ventas(LoginRequiredMixin, ListView):
    template_name = 'historial_ventas.html'
    context_object_name = 'ventas'
    paginate_by = 10

    def get_queryset(self):
        empresa = obtener_empresa_requerida(self.request.user)
        return Venta.objects.filter(empresa=empresa).select_related('empleado__user', 'cliente', 'medio_pago') \
                            .prefetch_related('detalles__producto') \
                            .order_by('-fecha')


@login_required
@rol_requerido('admin')
def descargar_historial_ventas(request):
    empresa = obtener_empresa_requerida(request.user)
    ventas = Venta.objects.filter(empresa=empresa).select_related(
        'empleado__user',
        'cliente',
        'medio_pago',
    ).prefetch_related('detalles__producto').order_by('-fecha')

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="historial_ventas.csv"'
    response.write('\ufeff')

    writer = csv.writer(response)
    writer.writerow(['ID venta', 'Empleado', 'Medio de pago', 'Fecha', 'Total', 'Productos'])

    for venta in ventas:
        productos = []
        for detalle in venta.detalles.all():
            producto = detalle.producto.nombre if detalle.producto else 'Producto eliminado'
            productos.append(f'{detalle.cantidad} x {producto} (${detalle.precio_unitario})')

        fecha = timezone.localtime(venta.fecha).strftime('%d/%m/%Y %H:%M')
        empleado = venta.empleado.user.get_full_name() if venta.empleado else 'Sin empleado'
        medio_pago = venta.medio_pago.nombre if venta.medio_pago else 'No especificado'

        writer.writerow([
            venta.id,
            empleado,
            medio_pago,
            fecha,
            venta.total,
            ' | '.join(productos),
        ])

    return response
    


Arqueo_views.listar_arqueo
Arqueo_views.eliminar_arqueo
Arqueo_views.crear_arqueo
Arqueo_views.cerrar_arqueo

Categorias_views.listar_categoria
Categorias_views.editar_categoria
Categorias_views.eliminar_categoria
Categorias_views.crear_categoria


Gastos_views.listar_gatos
Gastos_views.crear_gasto
Gastos_views.eliminar_gasto
Gastos_views.editar_gasto



Proveedores_views.listar_proveedores
Proveedores_views.editar_proveedor
Proveedores_views.crear_proveedor
Proveedores_views.eliminar_proveedor



Mediopago_views.listar_mediopago
Mediopago_views.editar_mediopago
Mediopago_views.crear_mediopago
Mediopago_views.eliminar_mediopago
 
Rol_views.listar_rol
Rol_views.crear_rol
Rol_views.editar_rol
Rol_views.editar_rol
