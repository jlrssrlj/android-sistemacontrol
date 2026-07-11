from dashboard.models import Gasto, Empleado, Proveedor, Arqueo
from django.shortcuts import get_object_or_404
from django.utils import timezone 

class GastosService:

    @staticmethod
    def listar_gastos(empresa):
        return Gasto.objects.filter(empresa=empresa)
    
    @staticmethod
    def obtener_gasto(id, empresa):
        return get_object_or_404(Gasto, id=id, empresa=empresa)

    @staticmethod
    def crear_gastos(data):
        gasto = Gasto.objects.create(
            empresa=data['empresa'],
            empleado=data['empleado'],
            proveedor=data['proveedor'],
            concepto=data['concepto'],
            monto=data['monto'],
            fecha=timezone.now(),
            arqueo=data['arqueo']
        )
        return gasto
    
    @staticmethod
    def editar_gasto(id, data, empresa):
        gasto = get_object_or_404(Gasto, id=id, empresa=empresa)
        gasto.empleado = data['empleado']
        gasto.proveedor = data['proveedor']
        gasto.concepto = data['concepto']
        gasto.monto = data['monto']
        gasto.arqueo = data['arqueo']
        gasto.save()
        return gasto
    
    @staticmethod
    def eliminar_gasto(id, empresa):
        gasto = get_object_or_404(Gasto, id=id, empresa=empresa)
        gasto.delete()
        return True
