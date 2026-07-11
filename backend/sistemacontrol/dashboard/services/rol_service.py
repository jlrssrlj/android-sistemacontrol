from dashboard.models import Rol
from django.shortcuts import get_object_or_404

class Rolservice:

    @staticmethod
    def crear_rol(data, empresa):
        pago = Rol.objects.create(
            empresa=empresa,
            nombre = data['nombre']
        )
        return pago
    
    @staticmethod
    def listar_rol(empresa):
        pago = Rol.objects.filter(empresa=empresa)
        return pago
    
    @staticmethod
    def eliminar_rol(id, empresa):
        pago = get_object_or_404(Rol, id=id, empresa=empresa)
        pago.delete()

    @staticmethod
    def editar_rol(id, data, empresa):
        pago = get_object_or_404(Rol, id=id, empresa=empresa)
        pago.nombre = data['nombre']
        pago.save()
        return pago
