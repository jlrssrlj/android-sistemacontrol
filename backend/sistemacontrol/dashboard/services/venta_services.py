from django.db import transaction
from decimal import Decimal
from dashboard.models import Venta, DetalleVenta, Producto

class VentaService:
    def __init__(self, empleado, arqueo):
        self.empleado = empleado
        self.arqueo = arqueo
        self.empresa = empleado.empresa

    @transaction.atomic
    def crear_venta(self, productos):  
        total = Decimal(0)
        detalles = []

        for item in productos:
            producto = Producto.objects.get(id=item['producto_id'], empresa=self.empresa)
            cantidad = item['cantidad']
            subtotal = producto.precio * cantidad
            total += subtotal
            detalles.append((producto, cantidad, producto.precio))

        venta = Venta.objects.create(
            empresa=self.empresa,
            empleado=self.empleado,
            arqueo=self.arqueo,
            total=total
        )

        for producto, cantidad, precio in detalles:
            DetalleVenta.objects.create(
                venta=venta,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=precio
            )
            producto.stock -= cantidad
            producto.save()

        return venta
