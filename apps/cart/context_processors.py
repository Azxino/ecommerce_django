from .cart import Cart


def cart_items_count(request):
    if request.user.is_authenticated:
        cart = Cart(request)
        return {'cart_items_count': cart.total_items}
    return {'cart_items_count': 0}
