from django.shortcuts import render, redirect, get_object_or_404
from ..services.listar_producto import ProductoService
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from dashboard.models import Categoria, Producto, Proveedor
from dashboard.decorators import rol_requerido
from dashboard.empresa import obtener_empresa_requerida
from django.http import HttpResponse
from decimal import Decimal, InvalidOperation
import csv
import io

class Producto_views:


    @login_required
    def crear_producto(request):
        empresa = obtener_empresa_requerida(request.user)
        if request.method == 'POST':
            categoria_id = request.POST.get('categoria_id')
            proveedor_id = request.POST.get('proveedor_id')  # Corregido el typo

            data = {
                'nombre': request.POST.get('nombre'),
                'descripcion': request.POST.get('descripcion'),
                'precio': request.POST.get('precio'),
                'stock': request.POST.get('stock'),
                'categoria_id': categoria_id,
                'proveedor_id': proveedor_id
            }

            ProductoService.crear_producto(data, empresa)
            return redirect('listar_producto')

        categorias = Categoria.objects.filter(empresa=empresa)
        proveedores = Proveedor.objects.filter(empresa=empresa)
        return render(request, 'productos/crear_producto.html', {
            'categorias': categorias,
            'proveedores': proveedores
        })

    @rol_requerido("administrador")
    @login_required
    def listar_producto(request):
        empresa = obtener_empresa_requerida(request.user)
        productos = ProductoService.listar_producto(empresa)
        return render(request, 'productos/listar_producto.html', {'producto': productos})

    @login_required
    @rol_requerido("administrador")
    def descargar_plantilla_productos(request):
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="plantilla_productos.csv"'
        response.write('\ufeff')

        writer = csv.writer(response)
        writer.writerow(['nombre', 'descripcion', 'precio', 'stock', 'categoria', 'proveedor'])
        writer.writerow(['Arroz 500g', 'Arroz blanco libra', '3500', '20', 'Granos', 'Proveedor Ejemplo'])
        writer.writerow(['Jabon liquido', 'Producto de aseo', '7800', '10', 'Aseo', 'Proveedor Ejemplo'])
        return response

    @login_required
    @rol_requerido("administrador")
    def carga_masiva_productos(request):
        if request.method == 'POST':
            empresa = obtener_empresa_requerida(request.user)
            archivo = request.FILES.get('archivo')

            if not archivo:
                messages.error(request, 'Selecciona un archivo CSV.')
                return redirect('carga_masiva_productos')

            if not archivo.name.lower().endswith('.csv'):
                messages.error(request, 'El archivo debe tener formato CSV.')
                return redirect('carga_masiva_productos')

            try:
                contenido = archivo.read().decode('utf-8-sig')
                lector = csv.DictReader(io.StringIO(contenido))
            except UnicodeDecodeError:
                messages.error(request, 'No se pudo leer el archivo. Guarda el CSV en formato UTF-8.')
                return redirect('carga_masiva_productos')

            campos = {campo.strip().lower(): campo for campo in lector.fieldnames or []}
            requeridos = ['nombre', 'precio', 'stock', 'categoria', 'proveedor']
            faltantes = [campo for campo in requeridos if campo not in campos]
            if faltantes:
                messages.error(request, f'Faltan columnas obligatorias: {", ".join(faltantes)}.')
                return redirect('carga_masiva_productos')

            creados = 0
            omitidos = 0
            errores = []
            vistos = set()

            for numero_fila, fila in enumerate(lector, start=2):
                nombre = (fila.get(campos['nombre']) or '').strip()
                descripcion = (fila.get(campos.get('descripcion', '')) or '').strip()
                categoria_nombre = (fila.get(campos['categoria']) or '').strip()
                proveedor_nombre = (fila.get(campos.get('proveedor', '')) or '').strip()
                clave = nombre.lower()

                if not nombre or clave in vistos:
                    omitidos += 1
                    continue

                vistos.add(clave)

                try:
                    precio = Decimal((fila.get(campos['precio']) or '').strip())
                    stock = int((fila.get(campos['stock']) or '').strip())
                except (InvalidOperation, ValueError):
                    omitidos += 1
                    errores.append(f'Fila {numero_fila}: precio o stock inválido.')
                    continue

                if precio < 0 or stock < 0:
                    omitidos += 1
                    errores.append(f'Fila {numero_fila}: precio y stock no pueden ser negativos.')
                    continue

                categoria = Categoria.objects.filter(
                    empresa=empresa,
                    nombre__iexact=categoria_nombre,
                ).first()
                if not categoria:
                    omitidos += 1
                    errores.append(f'Fila {numero_fila}: categoría "{categoria_nombre}" no existe.')
                    continue

                proveedor = Proveedor.objects.filter(
                    empresa=empresa,
                    nombre__iexact=proveedor_nombre,
                ).first()
                if not proveedor:
                    omitidos += 1
                    errores.append(f'Fila {numero_fila}: proveedor "{proveedor_nombre}" no existe.')
                    continue

                if Producto.objects.filter(empresa=empresa, nombre__iexact=nombre).exists():
                    omitidos += 1
                    continue

                Producto.objects.create(
                    empresa=empresa,
                    nombre=nombre,
                    descripcion=descripcion,
                    precio=precio,
                    stock=stock,
                    categoria=categoria,
                    proveedor=proveedor,
                )
                creados += 1

            messages.success(request, f'Carga completada. Creados: {creados}. Omitidos: {omitidos}.')
            for error in errores[:5]:
                messages.warning(request, error)
            if len(errores) > 5:
                messages.warning(request, f'Hay {len(errores) - 5} errores adicionales no mostrados.')

            return redirect('listar_producto')

        return render(request, 'productos/carga_masiva_productos.html')

    @login_required
    def editar_producto(request, id):
        empresa = obtener_empresa_requerida(request.user)
        producto = get_object_or_404(Producto, id=id, empresa=empresa)

        if request.method == 'POST':
            data = {
                'nombre': request.POST.get('nombre'),
                'descripcion': request.POST.get('descripcion'),
                'precio': request.POST.get('precio'),
                'stock': request.POST.get('stock'),
                'categoria_id': request.POST.get('categoria_id'),
                'proveedor_id': request.POST.get('proveedor_id')
            }
            ProductoService.actualizar_producto(producto.id, data, empresa)
            return redirect('listar_producto')

        categorias = Categoria.objects.filter(empresa=empresa)
        proveedores = Proveedor.objects.filter(empresa=empresa)
        return render(request, 'productos/editar_producto.html', {
            'producto': producto,
            'categorias': categorias,
            'proveedores': proveedores
        })

    @login_required
    def eliminar_producto(request, id):
        empresa = obtener_empresa_requerida(request.user)
        producto = get_object_or_404(Producto, id=id, empresa=empresa)

        if request.method == 'POST':
            ProductoService.eliminar_producto(id, empresa)
            return redirect('listar_producto')

        return render(request, 'productos/confirmar_eliminacion_producto.html', {'producto': producto})
