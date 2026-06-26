from .models import Categoria


def categorias_globales(request):
    return {'categorias': Categoria.objects.filter(activo=True)}
