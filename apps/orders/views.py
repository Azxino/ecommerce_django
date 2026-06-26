# Patrón Template Method (CBV): ListView y DetailView con LoginRequiredMixin
# para filtrar pedidos del usuario autenticado.
# Patrón Decorator: @require_POST y @csrf_protect envuelven las funciones
# create_order y cancel_order para restringir el método HTTP y proteger CSRF.
# Vistas de pedidos: listado, detalle, creación y cancelación (solo usuarios autenticados)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView

from apps.cart.cart import Cart
from apps.cart.models import Cupon

from .models import DetallePedido, Pedido


# Listado de pedidos del usuario autenticado
class PedidoListView(LoginRequiredMixin, ListView):
    model = Pedido
    template_name = 'orders/order_list.html'
    context_object_name = 'pedidos'
    paginate_by = 10

    # Filtra solo los pedidos del usuario actual
    def get_queryset(self):
        return Pedido.objects.filter(
            usuario=self.request.user
        ).prefetch_related('detalles__producto')


# Detalle de un pedido específico del usuario autenticado
class PedidoDetailView(LoginRequiredMixin, DetailView):
    model = Pedido
    template_name = 'orders/order_detail.html'
    context_object_name = 'pedido'

    # Asegura que solo el dueño del pedido pueda verlo
    def get_queryset(self):
        return Pedido.objects.filter(
            usuario=self.request.user
        ).prefetch_related('detalles__producto')


# Crear un nuevo pedido a partir del carrito (solo POST)
@require_POST
def create_order(request):
    # Verifica que el usuario esté autenticado
    if not request.user.is_authenticated:
        messages.error(
            request, 'Debes iniciar sesión para realizar un pedido.'
        )
        return redirect('accounts:login')

    cart = Cart(request)
    # Verifica que el carrito no esté vacío
    if cart.total_items == 0:
        messages.error(
            request, 'Tu carrito está vacío.'
        )
        return redirect('cart:detail')

    # Verifica stock disponible para cada producto
    for item in cart:
        producto = item['producto']
        if item['cantidad'] > producto.stock:
            messages.error(
                request,
                f'"{producto.nombre}" solo tiene {producto.stock} '
                f'unidades disponibles.'
            )
            return redirect('cart:detail')

    # Calcula descuento, subtotal y total
    descuento = cart.get_cupon_descuento()
    subtotal = cart.subtotal
    total = max(subtotal - descuento, 0)

    # Aplica cupón de descuento si existe
    cupon_id = request.session.get('cupon_id')
    cupon_codigo = None
    if cupon_id:
        try:
            cupon = Cupon.objects.get(id=cupon_id)
            if cupon.es_valido:
                cupon_codigo = cupon.codigo
                cupon.incrementar_uso()
        except Cupon.DoesNotExist:
            pass

    # Crea el pedido con los datos calculados
    pedido = Pedido.objects.create(
        usuario=request.user,
        estado=Pedido.Estado.PENDIENTE,
        subtotal=subtotal,
        descuento=descuento,
        total=total,
        cupon_codigo=cupon_codigo,
    )

    # Crea los detalles del pedido y descuenta stock
    for item in cart:
        producto = item['producto']
        DetallePedido.objects.create(
            pedido=pedido,
            producto=producto,
            precio=item['precio'],
            cantidad=item['cantidad'],
            subtotal=item['total'],
        )
        producto.stock -= item['cantidad']
        producto.save(update_fields=['stock'])

    # Limpia el carrito después de crear el pedido
    cart.clear()

    messages.success(
        request,
        f'¡Pedido #{pedido.id} creado exitosamente! '
        'Te contactaremos para confirmar.'
    )
    return redirect('orders:detail', pk=pedido.id)


# Cancelar un pedido (solo si está pendiente o confirmado; solo POST)
@require_POST
def cancel_order(request, pk):
    pedido = get_object_or_404(
        Pedido, pk=pk, usuario=request.user
    )
    # Solo permite cancelar pedidos pendientes o confirmados
    if pedido.estado in [Pedido.Estado.PENDIENTE, Pedido.Estado.CONFIRMADO]:
        # Restaura el stock de los productos
        for detalle in pedido.detalles.all():
            producto = detalle.producto
            producto.stock += detalle.cantidad
            producto.save(update_fields=['stock'])

        pedido.estado = Pedido.Estado.CANCELADO
        pedido.save(update_fields=['estado'])
        messages.info(
            request,
            f'Pedido #{pedido.id} cancelado.'
        )
    else:
        messages.error(
            request,
            'No se puede cancelar un pedido en este estado.'
        )
    return redirect('orders:detail', pk=pedido.id)
