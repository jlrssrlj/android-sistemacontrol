from dashboard.models import Proveedor
from django.shortcuts import get_object_or_404

class ProveedorService:

    @staticmethod
    def crear_proveedor(data, empresa):
        proveedor = Proveedor.objects.create(
            empresa=empresa,
            nombre=data['nombre'],
            nit=data['nit'],
            direccion=data['direccion'],
            telefono=data['telefono']
        )
        return proveedor

    @staticmethod
    def actualizar_proveedor(proveedor, data):
        proveedor.nombre = data.get('nombre', proveedor.nombre)
        proveedor.nit = data.get('nit', proveedor.nit)
        proveedor.direccion = data.get('direccion', proveedor.direccion)
        proveedor.telefono = data.get('telefono', proveedor.telefono)
        proveedor.save()
        return proveedor

    @staticmethod
    def eliminar_proveedor(id, empresa):
        proveedor = get_object_or_404(Proveedor, id=id, empresa=empresa)
        proveedor.delete()
        return True

    @staticmethod
    def obtener_proveedores(empresa):
        return Proveedor.objects.filter(empresa=empresa)

    @staticmethod
    def obtener_proveedor(id, empresa):
        return get_object_or_404(Proveedor, id=id, empresa=empresa)
