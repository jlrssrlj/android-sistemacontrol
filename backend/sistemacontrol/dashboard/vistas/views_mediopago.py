from django.shortcuts import render, redirect, get_object_or_404
from dashboard.decorators import rol_requerido
from ..services.mediopago_service import MediopagoService


class Mediopago_views:

    @rol_requerido("Administrador")
    def listar_mediopago(request):
        pagos = MediopagoService.listar_mediopago()
        return render(request, 'mediopago/listar_mediopago.html', {'pagos': pagos})

    @rol_requerido("Administrador")
    def crear_mediopago(request):
        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            if nombre:
                MediopagoService.crear_mediopago({'nombre': nombre})
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
        pago = get_object_or_404(MediopagoService.listar_mediopago(), id=id)

        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            if nombre:
                MediopagoService.editar_mediopago(id, {'nombre': nombre})
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
            MediopagoService.eliminar_mediopago(id)
            return redirect('listar_medio_pago')

        pago = get_object_or_404(MediopagoService.listar_mediopago(), id=id)
        return render(request, 'mediopago/eliminar_mediopago.html', {'pago': pago})