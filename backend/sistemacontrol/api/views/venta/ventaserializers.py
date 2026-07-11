from rest_framework import serializers
from dashboard.models import Venta, DetalleVenta


class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = '__all__'


class VentaSerializer(serializers.ModelSerializer):
    detalles = DetalleVentaSerializer(many=True)

    class Meta:
        model = Venta
        fields = [
            "id",
            "empresa",
            "empleado",
            "arqueo",
            "cliente",
            "medio_pago",
            "fecha",
            "total",
            "detalles",
        ]
        read_only_fields = ["empresa", "total", "fecha"]

    def create(self, validated_data):
        detalles_data = validated_data.pop("detalles")
        empresa = validated_data["empresa"]
        for campo in ("empleado", "arqueo", "cliente", "medio_pago"):
            valor = validated_data.get(campo)
            if valor and valor.empresa_id != empresa.id:
                raise serializers.ValidationError(f"{campo} no pertenece a la empresa del usuario.")

        for detalle_data in detalles_data:
            producto = detalle_data.get("producto")
            if producto and producto.empresa_id != empresa.id:
                raise serializers.ValidationError("El producto no pertenece a la empresa del usuario.")

        venta = Venta.objects.create(**validated_data)

        total = 0

        for detalle_data in detalles_data:
            detalle = DetalleVenta.objects.create(
                venta=venta,
                **detalle_data
            )
            total += detalle.subtotal()

        venta.total = total
        venta.save()

        return venta
