# Vistas del carrito: detalle, agregar, eliminar, actualizar, vaciar y cupones
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from apps.products.models import Producto

from .cart import Cart
from .forms import AgregarAlCarritoForm, CuponForm
from .models import Cupon


# Muestra el contenido del carrito con el formulario de cupón
class CartDetailView(TemplateView):
    template_name = 'cart/cart_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context['cart'] = cart
        context['add_form'] = AgregarAlCarritoForm()
        context['cupon_form'] = CuponForm()
        context['descuento'] = cart.get_cupon_descuento()

        # Obtiene el cupón aplicado si existe
        cupon_id = self.request.session.get('cupon_id')
        if cupon_id:
            try:
                context['cupon_aplicado'] = Cupon.objects.get(id=cupon_id)
            except Cupon.DoesNotExist:
                pass
        return context


# Agrega un producto al carrito (solo POST, verifica stock)
@require_POST
def add_to_cart(request, producto_id):
    producto = get_object_or_404(
        Producto, id=producto_id, disponible=True
    )
    form = AgregarAlCarritoForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        # Verifica que la cantidad solicitada no supere el stock
        if cd['cantidad'] > producto.stock:
            messages.error(
                request,
                f'Solo hay {producto.stock} unidades disponibles '
                f'de "{producto.nombre}".'
            )
            return redirect('products:detail', slug=producto.slug)
        cart = Cart(request)
        cart.add(
            producto=producto,
            cantidad=cd['cantidad'],
            update_quantity=cd['update']
        )
        messages.success(
            request,
            f'{cd["cantidad"]} x "{producto.nombre}" añadido al carrito.'
        )
    return redirect('cart:detail')


# Elimina un producto del carrito (solo POST)
@require_POST
def remove_from_cart(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    cart = Cart(request)
    cart.remove(producto)
    messages.info(request, f'"{producto.nombre}" eliminado del carrito.')
    return redirect('cart:detail')


# Actualiza la cantidad de un producto en el carrito (solo POST)
@require_POST
def update_cart(request, producto_id):
    producto = get_object_or_404(
        Producto, id=producto_id, disponible=True
    )
    form = AgregarAlCarritoForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart = Cart(request)
        # Verifica stock antes de actualizar
        if cd['cantidad'] > producto.stock:
            messages.error(
                request,
                f'Solo hay {producto.stock} unidades disponibles '
                f'de "{producto.nombre}".'
            )
            return redirect('cart:detail')
        cart.add(
            producto=producto,
            cantidad=cd['cantidad'],
            update_quantity=True
        )
        messages.success(
            request,
            f'Cantidad de "{producto.nombre}" actualizada.'
        )
    return redirect('cart:detail')


# Vacía todo el carrito (solo POST)
@require_POST
def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    messages.info(request, 'Carrito vaciado.')
    return redirect('cart:detail')


# Aplica un cupón de descuento al carrito (solo POST)
@require_POST
def apply_cupon(request):
    form = CuponForm(request.POST)
    if form.is_valid():
        codigo = form.cleaned_data['codigo']
        try:
            cupon = Cupon.objects.get(
                codigo__iexact=codigo, activo=True
            )
            cart = Cart(request)
            # Verifica que el subtotal alcance el monto mínimo del cupón
            if cart.subtotal < cupon.monto_minimo:
                messages.error(
                    request,
                    f'El monto mínimo para este cupón es '
                    f'${cupon.monto_minimo:.2f}.'
                )
                return redirect('cart:detail')
            if not cupon.es_valido:
                messages.error(
                    request, 'Este cupón ha expirado o ya no es válido.'
                )
                return redirect('cart:detail')
            cart.set_cupon(cupon)
            messages.success(
                request,
                f'Cupón "{cupon.codigo}" aplicado. '
                f'Descuento: {cupon.valor}'
                f'{"%" if cupon.tipo == "PORCENTAJE" else "$"}'
            )
        except Cupon.DoesNotExist:
            messages.error(
                request, 'Cupón no encontrado o inactivo.'
            )
    return redirect('cart:detail')


# Elimina el cupón aplicado al carrito (solo POST)
@require_POST
def remove_cupon(request):
    if 'cupon_id' in request.session:
        del request.session['cupon_id']
        request.session.modified = True
        messages.info(request, 'Cupón eliminado.')
    return redirect('cart:detail')
