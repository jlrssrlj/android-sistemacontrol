from django.db.models import Sum
from decimal import Decimal
from dashboard.models import Arqueo, Venta, Gasto
from django.utils import timezone
from django.shortcuts import get_object_or_404            

class ArqueoService:

    @staticmethod
    def crear_arqueo(data):
        arqueo = Arqueo.objects.create(
            empresa=data['empresa'],
            empleado=data['empleado'],
            fecha_inicio=timezone.now(),
            monto_inicial=data['monto_inicial']
        )
        return arqueo

    @staticmethod
    def cerrar_arqueo(arqueo_id, monto_final, empresa):
        arqueo = get_object_or_404(Arqueo, id=arqueo_id, empresa=empresa)
        arqueo.fecha_fin = timezone.now()
        arqueo.monto_final = Decimal(monto_final)

        #
        total_ventas = Venta.objects.filter(
            arqueo=arqueo,
            empresa=empresa,
            empleado=arqueo.empleado
        ).aggregate(total=Sum('total'))['total'] or Decimal('0')

        
        total_gastos = Gasto.objects.filter(
            arqueo=arqueo,
            empresa=empresa
        ).aggregate(total=Sum('monto'))['total'] or Decimal('0')

        calculado = arqueo.monto_inicial + total_ventas - total_gastos
        arqueo.diferencia = calculado - arqueo.monto_final

        arqueo.save()
        return arqueo

    @staticmethod
    def listar_arqueos(empresa):
        arqueos = Arqueo.objects.filter(empresa=empresa).select_related('empleado__user').order_by('-fecha_inicio')
        for arqueo in arqueos:
            arqueo.total_ventas = Venta.objects.filter(
                arqueo=arqueo,
                empresa=empresa,
                empleado=arqueo.empleado
            ).aggregate(total=Sum('total'))['total'] or 0

            arqueo.total_gastos = Gasto.objects.filter(
                arqueo=arqueo,
                empresa=empresa
            ).aggregate(total=Sum('monto'))['total'] or 0
        return arqueos

    @staticmethod
    def obtener_arqueo(id, empresa):
        return get_object_or_404(Arqueo, id=id, empresa=empresa)

    @staticmethod
    def eliminar_arqueo(id, empresa):
        arqueo = get_object_or_404(Arqueo, id=id, empresa=empresa)
        arqueo.delete()
