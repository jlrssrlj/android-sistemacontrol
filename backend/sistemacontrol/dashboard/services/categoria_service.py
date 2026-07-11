from dashboard.models import Categoria
from django.shortcuts import get_object_or_404

class CategoriaService:

    @staticmethod
    def crear_categoria(data, empresa):
        categoria = Categoria.objects.create(nombre=data['nombre'], empresa=empresa)
        return categoria

    @staticmethod
    def editar_categoria(categoria_id, data, empresa):
        categoria = get_object_or_404(Categoria, id=categoria_id, empresa=empresa)
        categoria.nombre = data['nombre']
        categoria.save()
        return categoria

    @staticmethod
    def eliminar_categoria(categoria_id, empresa):
        categoria = get_object_or_404(Categoria, id=categoria_id, empresa=empresa)
        categoria.delete()

    @staticmethod
    def obtener_categoria(categoria_id, empresa):
        return get_object_or_404(Categoria, id=categoria_id, empresa=empresa)

    @staticmethod
    def listar_categoria(empresa):
        return Categoria.objects.filter(empresa=empresa).order_by('nombre')
