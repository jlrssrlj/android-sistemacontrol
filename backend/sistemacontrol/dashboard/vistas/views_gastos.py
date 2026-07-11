from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.models import Proveedor, Empleado, Arqueo
from django.contrib import auth, messages
from ..services.listar_gastos import GastosService
from django.contrib.auth.decorators import login_required
from dashboard.empresa import obtener_empresa_requerida

class Gastos_views:

    @login_required
    def listar_gatos(request):
        empresa = obtener_empresa_requerida(request.user)
        gastos = GastosService.listar_gastos(empresa)
        return render(request, 'gastos/listar_gastos.html', {'gastos': gastos})


    @login_required
    def crear_gasto(request):
        if request.method == 'POST':
            empresa = obtener_empresa_requerida(request.user)
            empleado = Empleado.objects.get(user=request.user)

            arqueo_abierto = Arqueo.objects.filter(empresa=empresa, empleado=empleado, fecha_fin__isnull=True).first()
            if not arqueo_abierto:
                
                return redirect('listar_arqueos')

            data = {
                'empresa': empresa,
                'empleado': empleado,
                'proveedor': Proveedor.objects.get(id=request.POST['proveedor'], empresa=empresa),
                'concepto': request.POST['concepto'],
                'monto': request.POST['monto'],
                'arqueo': arqueo_abierto
            }

            GastosService.crear_gastos(data)
            
            return redirect('listar_gastos')

        empresa = obtener_empresa_requerida(request.user)
        proveedores = Proveedor.objects.filter(empresa=empresa)
        return render(request, 'gastos/crear_gastos.html', {
            'proveedores': proveedores
        })


    @login_required
    def editar_gasto(request, id):
        empresa = obtener_empresa_requerida(request.user)
        gasto = GastosService.obtener_gasto(id, empresa)

        if request.method == 'POST':
            data = {
                'empresa': empresa,
                'empleado': Empleado.objects.get(id=request.POST['empleado'], empresa=empresa),
                'proveedor': Proveedor.objects.get(id=request.POST['proveedor'], empresa=empresa),
                'concepto': request.POST['concepto'],
                'monto': request.POST['monto'],
                'arqueo': Arqueo.objects.get(id=request.POST['arqueo'], empresa=empresa),
            }
            GastosService.editar_gasto(id, data, empresa)
            messages.success(request, "Gasto editado correctamente.")
            return redirect('listar_gastos')

        empleados = Empleado.objects.filter(empresa=empresa)
        proveedores = Proveedor.objects.filter(empresa=empresa)
        arqueos = Arqueo.objects.filter(empresa=empresa)

        return render(request, 'gastos/editar_gasto.html', {
            'gasto': gasto,
            'empleados': empleados,
            'proveedores': proveedores,
            'arqueos': arqueos,
        })


    @login_required
    def eliminar_gasto(request, id):
        if request.method == 'POST':
            empresa = obtener_empresa_requerida(request.user)
            GastosService.eliminar_gasto(id, empresa)
            messages.success(request, "Gasto eliminado correctamente.")
        return redirect('listar_gastos')
