from dashboard.models import MedioPago
from django.shortcuts import get_object_or_404

class MediopagoService:

    @staticmethod
    def crear_mediopago(data, empresa):
        pago = MedioPago.objects.create(
            empresa=empresa,
            nombre = data['nombre']
        )
        return pago
    
    @staticmethod
    def listar_mediopago(empresa):
        pago = MedioPago.objects.filter(empresa=empresa)
        return pago
    
    @staticmethod
    def eliminar_mediopago(id, empresa):
        pago = get_object_or_404(MedioPago, id=id, empresa=empresa)
        pago.delete()

    @staticmethod
    def editar_mediopago(id, data, empresa):
        pago = get_object_or_404(MedioPago, id=id, empresa=empresa)
        pago.nombre = data['nombre']
        pago.save()
        return pago
