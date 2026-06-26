# Carrito de compras manejado por sesión (no requiere registro para agregar productos)
from decimal import Decimal

from django.conf import settings

from apps.products.models import Producto

# Clave en la sesión para almacenar el carrito
CART_SESSION_ID = getattr(settings, 'CART_SESSION_ID', 'cart')


class Cart:
    # Inicializa el carrito desde la sesión del usuario
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart
        self._cupon_data = None

    # Agrega un producto al carrito (o actualiza cantidad si ya existe)
    def add(self, producto, cantidad=1, update_quantity=False):
        producto_id = str(producto.id)
        if producto_id not in self.cart:
            self.cart[producto_id] = {
                'cantidad': 0,
                'precio': str(producto.precio),
                'nombre': producto.nombre,
            }
        if update_quantity:
            self.cart[producto_id]['cantidad'] = cantidad
        else:
            self.cart[producto_id]['cantidad'] += cantidad
        self.save()

    # Guarda el carrito en la sesión
    def save(self):
        self.session[CART_SESSION_ID] = self.cart
        self.session.modified = True

    # Elimina un producto del carrito
    def remove(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.cart:
            del self.cart[producto_id]
            self.save()

    # Vacía el carrito y elimina el cupón aplicado
    def clear(self):
        del self.session[CART_SESSION_ID]
        self.session.modified = True
        self._cupon_data = None
        if 'cupon_id' in self.session:
            del self.session['cupon_id']

    # Itera sobre los productos del carrito con datos completos (precio, total)
    def __iter__(self):
        product_ids = self.cart.keys()
        productos = Producto.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for producto in productos:
            cart[str(producto.id)]['producto'] = producto
        for item in cart.values():
            item['precio'] = Decimal(item['precio'])
            item['total'] = item['precio'] * item['cantidad']
            yield item

    # Cantidad total de items en el carrito
    def __len__(self):
        return sum(item['cantidad'] for item in self.cart.values())

    # Suma total sin descuento
    @property
    def subtotal(self):
        return sum(
            Decimal(item['precio']) * item['cantidad']
            for item in self.cart.values()
        )

    # Total con descuento aplicado (nunca menor a 0)
    @property
    def total(self):
        return max(self.subtotal - self.descuento, 0)

    # Descuento base (0, se reemplaza si hay cupón)
    @property
    def descuento(self):
        return Decimal(0)

    # Número total de productos en el carrito
    @property
    def total_items(self):
        return sum(item['cantidad'] for item in self.cart.values())

    # Aplica un cupón de descuento al carrito
    def set_cupon(self, cupon):
        if cupon and cupon.es_valido and self.subtotal >= cupon.monto_minimo:
            self.session['cupon_id'] = cupon.id
            self.session.modified = True

    # Calcula el descuento del cupón aplicado (porcentaje o monto fijo)
    def get_cupon_descuento(self):
        from .models import Cupon
        cupon_id = self.session.get('cupon_id')
        if not cupon_id:
            return Decimal(0)
        try:
            cupon = Cupon.objects.get(id=cupon_id, activo=True)
            if not cupon.es_valido:
                return Decimal(0)
            subtotal = self.subtotal
            if subtotal < cupon.monto_minimo:
                return Decimal(0)
            if cupon.tipo == Cupon.TipoDescuento.PORCENTAJE:
                return subtotal * (cupon.valor / 100)
            return cupon.valor
        except Cupon.DoesNotExist:
            return Decimal(0)
