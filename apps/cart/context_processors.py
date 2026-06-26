# Patrón Observer / Template Method: mismo esquema que categorias_globales.
# Se ejecuta automáticamente en cada request para inyectar el contador
# de items del carrito en todas las plantillas.
from .cart import Cart


def cart_items_count(request):
    if request.user.is_authenticated:
        cart = Cart(request)
        return {'cart_items_count': cart.total_items}
    return {'cart_items_count': 0}
