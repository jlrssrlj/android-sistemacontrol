from django.shortcuts import render, redirect, get_object_or_404
from dashboard.decorators import rol_requerido
from ..services.mediopago_service import MediopagoService
from dashboard.empresa import obtener_empresa_requerida


class Mediopago_views:

    @rol_requerido("Administrador")
    def listar_mediopago(request):
        empresa = obtener_empresa_requerida(request.user)
        pagos = MediopagoService.listar_mediopago(empresa)
        return render(request, 'mediopago/listar_mediopago.html', {'pagos': pagos})

    @rol_requerido("Administrador")
    def crear_mediopago(request):
        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            if nombre:
                empresa = obtener_empresa_requerida(request.user)
                MediopagoService.crear_mediopago({'nombre': nombre}, empresa)
                return redirect('listar_medio_pago')
            else:
                return render(
                    request,
                    'mediopago/crear_mediopago.html',
                    {'error': 'El nombre es obligatorio'}
                )

        return render(request, 'mediopago/crear_mediopago.html')

    @rol_requerido("Administrador")
    def editar_mediopago(request, id):
        empresa = obtener_empresa_requerida(request.user)
        pago = get_object_or_404(MediopagoService.listar_mediopago(empresa), id=id)

        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            if nombre:
                MediopagoService.editar_mediopago(id, {'nombre': nombre}, empresa)
                return redirect('listar_medio_pago')
            else:
                return render(
                    request,
                    'mediopago/editar_mediopago.html',
                    {
                        'pago': pago,
                        'error': 'El nombre es obligatorio'
                    }
                )

        return render(request, 'mediopago/editar_mediopago.html', {'pago': pago})

    @rol_requerido("Administrador")
    def eliminar_mediopago(request, id):
        if request.method == 'POST':
            empresa = obtener_empresa_requerida(request.user)
            MediopagoService.eliminar_mediopago(id, empresa)
            return redirect('listar_medio_pago')

        empresa = obtener_empresa_requerida(request.user)
        pago = get_object_or_404(MediopagoService.listar_mediopago(empresa), id=id)
        return render(request, 'mediopago/eliminar_mediopago.html', {'pago': pago})
