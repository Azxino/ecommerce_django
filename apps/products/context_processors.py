# Patrón Observer / Template Method: Django ejecuta automáticamente este
# context processor en cada request. El framework "notifica" a todos los
# context processors registrados, y cada uno inyecta datos en el contexto
# global de todas las plantillas sin que las vistas lo soliciten explícitamente.
from .models import Categoria


def categorias_globales(request):
    return {'categorias': Categoria.objects.filter(activo=True)}
