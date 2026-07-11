from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.models import Proveedor
from ..forms import UsuarioEmpleadoForm
from ..forms import ProveedorForm
from ..services.listar_proveedores import ProveedorService
from django.contrib.auth.decorators import login_required
from dashboard.empresa import obtener_empresa_requerida


class Proveedores_views:
    @login_required
    def listar_proveedores(request):
        empresa = obtener_empresa_requerida(request.user)
        proveedores = ProveedorService.obtener_proveedores(empresa)
        return render(request, 'proveedor/listar_proveedores.html', {'proveedores': proveedores})

    @login_required
    def crear_proveedor(request):
        empresa = obtener_empresa_requerida(request.user)
        if request.method == 'POST':
            form = ProveedorForm(request.POST)
            if form.is_valid():
                proveedor = form.save(commit=False)
                proveedor.empresa = empresa
                proveedor.save()
                return redirect('listar_proveedores')
        else:
            form = ProveedorForm()
        return render(request, 'proveedor/crear_proveedor.html', {'form': form})

    @login_required
    def editar_proveedor(request, pk):
        empresa = obtener_empresa_requerida(request.user)
        proveedor = get_object_or_404(Proveedor, pk=pk, empresa=empresa)
        if request.method == 'POST':
            form = ProveedorForm(request.POST, instance=proveedor)
            if form.is_valid():
                form.save()
                return redirect('listar_proveedores')
        else:
            form = ProveedorForm(instance=proveedor)
        return render(request, 'proveedor/crear_proveedor.html', {'form': form})

    @login_required
    def eliminar_proveedor(request, pk):
        empresa = obtener_empresa_requerida(request.user)
        proveedor = get_object_or_404(Proveedor, pk=pk, empresa=empresa)
        proveedor.delete()
        return redirect('listar_proveedores')
