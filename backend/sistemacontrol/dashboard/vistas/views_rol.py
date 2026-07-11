from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.models import Rol
from ..services.rol_service import Rolservice
from django.contrib.auth.decorators import login_required
from dashboard.empresa import obtener_empresa_requerida

class Rol_views:
    def listar_rol(request):
        empresa = obtener_empresa_requerida(request.user)
        rol = Rolservice.listar_rol(empresa)
        return render(request, 'rol/listar_rol.html',{'rol': rol})

    @login_required
    def crear_rol(request):
        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            if nombre:
                empresa = obtener_empresa_requerida(request.user)
                Rolservice.crear_rol({'nombre': nombre}, empresa)
                return redirect('listar_rol')
            else:
                return render(request, 'rol/crear_rol.html',{'error': 'El nombre es obligatorio'})
        
        return render(request, 'rol/crear_rol.html')


    def editar_rol(request, id):
        empresa = obtener_empresa_requerida(request.user)
        rol = get_object_or_404(Rolservice.listar_rol(empresa), id=id)

        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            if nombre:
                Rolservice.editar_rol(id, {'nombre': nombre}, empresa)
                return redirect('listar_rol')  
            else:
                return render(request, 'rol/editar_rol.html', {
                    'rol': rol,
                    'error': 'El nombre es obligatorio'
                })

        return render(request, 'rol/editar_rol.html', {'rol': rol})

    def eliminar_rol(request,id):
        if request.method == 'POST':
            empresa = obtener_empresa_requerida(request.user)
            Rolservice.eliminar_rol(id, empresa)
            return redirect('listar_rol')
        empresa = obtener_empresa_requerida(request.user)
        rol = get_object_or_404(Rolservice.listar_rol(empresa), id=id)
        return render(request, 'rol/eliminar_rol.html',{'rol':rol})
   
