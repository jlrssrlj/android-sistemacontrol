from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from ..services.categoria_service import CategoriaService 
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from dashboard.empresa import obtener_empresa_requerida
from dashboard.models import Categoria
from django.http import HttpResponse
import csv
import io

class Categorias_views:
    @login_required
    def listar_categoria(request):
        empresa = obtener_empresa_requerida(request.user)
        categorias = CategoriaService.listar_categoria(empresa)
        print("Categorias en vista:", categorias)
        return render(request, 'categoria/listar_categoria.html', {'categorias': categorias})

    @login_required
    def crear_categoria(request):
        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            if nombre:
                empresa = obtener_empresa_requerida(request.user)
                CategoriaService.crear_categoria({'nombre': nombre}, empresa)
                return redirect('listar_categoria')
        return render(request,'categoria/crear_categoria.html')

    @login_required
    def descargar_plantilla_categorias(request):
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="plantilla_categorias.csv"'
        response.write('\ufeff')

        writer = csv.writer(response)
        writer.writerow(['nombre'])
        writer.writerow(['Bebidas'])
        writer.writerow(['Aseo'])
        writer.writerow(['Granos'])
        return response

    @login_required
    def carga_masiva_categorias(request):
        if request.method == 'POST':
            empresa = obtener_empresa_requerida(request.user)
            archivo = request.FILES.get('archivo')

            if not archivo:
                messages.error(request, 'Selecciona un archivo CSV.')
                return redirect('carga_masiva_categorias')

            if not archivo.name.lower().endswith('.csv'):
                messages.error(request, 'El archivo debe tener formato CSV.')
                return redirect('carga_masiva_categorias')

            try:
                contenido = archivo.read().decode('utf-8-sig')
                lector = csv.DictReader(io.StringIO(contenido))
            except UnicodeDecodeError:
                messages.error(request, 'No se pudo leer el archivo. Guarda el CSV en formato UTF-8.')
                return redirect('carga_masiva_categorias')

            campos = {campo.strip().lower(): campo for campo in lector.fieldnames or []}
            campo_nombre = campos.get('nombre')

            if not campo_nombre:
                messages.error(request, 'El CSV debe tener una columna llamada nombre.')
                return redirect('carga_masiva_categorias')

            creadas = 0
            omitidas = 0
            vistas = set()

            for fila in lector:
                nombre = (fila.get(campo_nombre) or '').strip()
                clave = nombre.lower()

                if not nombre or clave in vistas:
                    omitidas += 1
                    continue

                vistas.add(clave)

                if Categoria.objects.filter(empresa=empresa, nombre__iexact=nombre).exists():
                    omitidas += 1
                    continue

                Categoria.objects.create(empresa=empresa, nombre=nombre)
                creadas += 1

            messages.success(request, f'Carga completada. Creadas: {creadas}. Omitidas: {omitidas}.')
            return redirect('listar_categoria')

        return render(request, 'categoria/carga_masiva_categorias.html')

    @login_required
    def editar_categoria(request, categoria_id):
        empresa = obtener_empresa_requerida(request.user)
        categoria = CategoriaService.obtener_categoria(categoria_id, empresa)

        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            if nombre:
                
                CategoriaService.editar_categoria(categoria_id, {'nombre': nombre}, empresa)
                return redirect('listar_categoria')

        return render(request, 'categoria/editar_categoria.html', {'categoria': categoria})



    @login_required
    @require_POST
    def eliminar_categoria(request, categoria_id):
        try:
            empresa = obtener_empresa_requerida(request.user)
            CategoriaService.eliminar_categoria(categoria_id, empresa)
            
        except Exception:
            messages.error(request, 'Error al eliminar la categoría.')
        return redirect('listar_categoria')
