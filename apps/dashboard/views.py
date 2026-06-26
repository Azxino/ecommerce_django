# Patrón Template Method (CBV): 22 vistas que heredan de TemplateView,
# ListView, CreateView, UpdateView, DeleteView y DetailView. Cada una
# sobrescribe get(), get_queryset(), get_context_data(), form_valid(), etc.
# Patrón Strategy: composición con LoginRequiredMixin para autenticación
# más verificación manual de rol admin en get() como estrategia de autorización.
# Panel de administración (dashboard): vistas protegidas solo para administradores
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView
)

from apps.accounts.models import CustomUser
from apps.accounts.forms import UsuarioForm
from apps.cart.models import Cupon
from apps.orders.models import Pedido
from apps.products.forms import CategoriaForm, ProductoForm
from apps.products.models import Categoria, Producto


# Vista principal del panel: muestra estadísticas generales (usuarios, productos, pedidos, ingresos)
class DashboardHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'

    def get(self, request, *args, **kwargs):
        # Solo administradores pueden acceder al dashboard
        if not request.user.is_admin:
            messages.error(
                request, 'No tienes permisos de administrador.'
            )
            return redirect('products:list')
        return super().get(request, *args, **kwargs)

    # Prepara datos estadísticos para la plantilla del dashboard
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hoy = timezone.now()
        context['total_usuarios'] = CustomUser.objects.count()
        context['total_clientes'] = CustomUser.objects.filter(
            role=CustomUser.Role.CLIENT
        ).count()
        context['total_productos'] = Producto.objects.count()
        context['productos_disponibles'] = Producto.objects.filter(
            disponible=True
        ).count()
        context['total_pedidos'] = Pedido.objects.count()
        context['pedidos_pendientes'] = Pedido.objects.filter(
            estado=Pedido.Estado.PENDIENTE
        ).count()
        context['ingresos_totales'] = Pedido.objects.filter(
            estado__in=[
                Pedido.Estado.ENTREGADO, Pedido.Estado.ENVIADO,
                Pedido.Estado.CONFIRMADO
            ]
        ).aggregate(total=Sum('total'))['total'] or 0
        context['productos_stock_bajo'] = Producto.objects.filter(
            stock__lte=5, disponible=True
        ).order_by('stock')[:10]
        context['ultimos_pedidos'] = Pedido.objects.all(
        ).select_related('usuario')[:5]
        context['ultimos_usuarios'] = CustomUser.objects.all(
        ).order_by('-date_joined')[:5]
        return context


# Lista de usuarios (solo administradores)
class DashboardUsuariosView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'dashboard/user_list.html'
    context_object_name = 'usuarios'
    paginate_by = 15

    def get_queryset(self):
        return CustomUser.objects.all().order_by('-date_joined')


# Crear nuevo usuario (solo admin)
class DashboardUsuarioCreateView(LoginRequiredMixin, CreateView):
    model = CustomUser
    form_class = UsuarioForm
    template_name = 'dashboard/user_form.html'
    success_url = reverse_lazy('dashboard:user_list')

    def get(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, 'No tienes permisos de administrador.')
            return redirect('products:list')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(
            self.request, 'Usuario creado correctamente.'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, 'Corrige los errores en el formulario.'
        )
        return super().form_invalid(form)


# Editar usuario existente (solo admin)
class DashboardUsuarioUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UsuarioForm
    template_name = 'dashboard/user_form.html'
    success_url = reverse_lazy('dashboard:user_list')

    def get(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, 'No tienes permisos de administrador.')
            return redirect('products:list')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(
            self.request, 'Usuario actualizado correctamente.'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, 'Corrige los errores en el formulario.'
        )
        return super().form_invalid(form)


# Eliminar usuario (solo admin)
class DashboardUsuarioDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'dashboard/user_confirm_delete.html'
    success_url = reverse_lazy('dashboard:user_list')
    context_object_name = 'usuario'

    def get(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, 'No tienes permisos de administrador.')
            return redirect('products:list')
        return super().get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(
            request, 'Usuario eliminado correctamente.'
        )
        return super().delete(request, *args, **kwargs)


# Listado de productos (admin)
class DashboardProductosView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'dashboard/product_list.html'
    context_object_name = 'productos'
    paginate_by = 15

    # Soporta búsqueda por nombre de producto
    def get_queryset(self):
        qs = Producto.objects.all().select_related('categoria')
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(nombre__icontains=query)
        return qs.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


# Crear nuevo producto (solo admin)
class DashboardProductoCreateView(LoginRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'dashboard/product_form.html'
    success_url = reverse_lazy('dashboard:product_list')

    def get(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, 'No tienes permisos de administrador.')
            return redirect('products:list')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(
            self.request, 'Producto creado correctamente.'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, 'Corrige los errores en el formulario.'
        )
        return super().form_invalid(form)


# Editar producto existente (solo admin)
class DashboardProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'dashboard/product_form.html'
    success_url = reverse_lazy('dashboard:product_list')

    def get(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, 'No tienes permisos de administrador.')
            return redirect('products:list')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(
            self.request, 'Producto actualizado correctamente.'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, 'Corrige los errores en el formulario.'
        )
        return super().form_invalid(form)


# Eliminar producto (solo admin)
class DashboardProductoDeleteView(LoginRequiredMixin, DeleteView):
    model = Producto
    template_name = 'dashboard/product_confirm_delete.html'
    success_url = reverse_lazy('dashboard:product_list')
    context_object_name = 'producto'

    def get(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, 'No tienes permisos de administrador.')
            return redirect('products:list')
        return super().get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(
            request, 'Producto eliminado correctamente.'
        )
        return super().delete(request, *args, **kwargs)


# Listado de categorías (admin)
class DashboardCategoriasView(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = 'dashboard/category_list.html'
    context_object_name = 'categorias'

    def get_queryset(self):
        return Categoria.objects.all().order_by('nombre')


# Crear nueva categoría (solo admin)
class DashboardCategoriaCreateView(LoginRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'dashboard/category_form.html'
    success_url = reverse_lazy('dashboard:category_list')

    def get(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, 'No tienes permisos de administrador.')
            return redirect('products:list')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(
            self.request, 'Categoría creada correctamente.'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, 'Corrige los errores en el formulario.'
        )
        return super().form_invalid(form)


# Editar categoría existente (solo admin)
class DashboardCategoriaUpdateView(LoginRequiredMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'dashboard/category_form.html'
    success_url = reverse_lazy('dashboard:category_list')

    def get(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, 'No tienes permisos de administrador.')
            return redirect('products:list')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(
            self.request, 'Categoría actualizada correctamente.'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, 'Corrige los errores en el formulario.'
        )
        return super().form_invalid(form)


# Eliminar categoría (solo admin)
class DashboardCategoriaDeleteView(LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'dashboard/category_confirm_delete.html'
    success_url = reverse_lazy('dashboard:category_list')
    context_object_name = 'categoria'

    def get(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, 'No tienes permisos de administrador.')
            return redirect('products:list')
        return super().get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(
            request, 'Categoría eliminada correctamente.'
        )
        return super().delete(request, *args, **kwargs)


# Listado de pedidos (admin) con filtro por estado
class DashboardPedidosView(LoginRequiredMixin, ListView):
    model = Pedido
    template_name = 'dashboard/order_list.html'
    context_object_name = 'pedidos'
    paginate_by = 15

    def get_queryset(self):
        qs = Pedido.objects.all().select_related('usuario')
        estado = self.request.GET.get('estado')
        if estado:
            qs = qs.filter(estado=estado)
        return qs.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estado_actual'] = self.request.GET.get('estado', '')
        context['estados'] = Pedido.Estado.choices
        return context


# Detalle de pedido (admin)
class DashboardPedidoDetailView(LoginRequiredMixin, DetailView):
    model = Pedido
    template_name = 'dashboard/order_detail.html'
    context_object_name = 'pedido'

    def get_queryset(self):
        return Pedido.objects.all().prefetch_related(
            'detalles__producto'
        ).select_related('usuario')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pedido_estados'] = Pedido.Estado.choices
        return context


# Actualizar estado de pedido (solo admin, acepta GET y POST)
class DashboardPedidoUpdateView(LoginRequiredMixin, UpdateView):
    model = Pedido
    fields = ('estado',)
    template_name = 'dashboard/order_detail.html'
    context_object_name = 'pedido'

    def get(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, 'No tienes permisos de administrador.')
            return redirect('products:list')
        return super().get(request, *args, **kwargs)

    # Cambia el estado del pedido vía POST
    def post(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, 'No tienes permisos de administrador.')
            return redirect('products:list')
        self.object = self.get_object()
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in dict(Pedido.Estado.choices):
            self.object.estado = nuevo_estado
            self.object.save(update_fields=['estado'])
            messages.success(
                request,
                f'Estado del pedido #{self.object.id} '
                f'actualizado a {self.object.get_estado_display()}.'
            )
        return redirect('dashboard:order_detail', pk=self.object.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pedido_estados'] = Pedido.Estado.choices
        return context


# Listado de cupones (admin)
class DashboardCuponesView(LoginRequiredMixin, ListView):
    model = Cupon
    template_name = 'dashboard/coupon_list.html'
    context_object_name = 'cupones'

    def get_queryset(self):
        return Cupon.objects.all().order_by('-created_at')


# Crear nuevo cupón de descuento (solo admin)
class DashboardCuponCreateView(LoginRequiredMixin, CreateView):
    model = Cupon
    fields = (
        'codigo', 'descripcion', 'tipo', 'valor',
        'monto_minimo', 'max_usos', 'activo', 'fecha_expiracion'
    )
    template_name = 'dashboard/coupon_form.html'
    success_url = reverse_lazy('dashboard:coupon_list')

    def get(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, 'No tienes permisos de administrador.')
            return redirect('products:list')
        return super().get(request, *args, **kwargs)

    # Personaliza widgets y etiquetas del formulario de cupón
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['fecha_expiracion'].widget.attrs.update(
            {'class': 'form-control', 'type': 'datetime-local'}
        )
        form.fields['codigo'].widget.attrs.update(
            {'class': 'form-control'}
        )
        form.fields['descripcion'].widget.attrs.update(
            {'class': 'form-control', 'rows': 2}
        )
        form.fields['valor'].widget.attrs.update(
            {'class': 'form-control', 'step': '0.01'}
        )
        form.fields['monto_minimo'].widget.attrs.update(
            {'class': 'form-control', 'step': '0.01'}
        )
        form.fields['max_usos'].widget.attrs.update(
            {'class': 'form-control'}
        )
        form.fields['tipo'].widget.attrs.update(
            {'class': 'form-select'}
        )
        labels = {
            'codigo': 'Código',
            'descripcion': 'Descripción',
            'tipo': 'Tipo de descuento',
            'valor': 'Valor',
            'monto_minimo': 'Monto mínimo',
            'max_usos': 'Usos máximos',
            'activo': 'Activo',
            'fecha_expiracion': 'Fecha de expiración',
        }
        form.fields['activo'].widget.attrs.update(
            {'class': 'form-check-input'}
        )
        for field_name, label in labels.items():
            form.fields[field_name].label = label
        return form

    def form_valid(self, form):
        messages.success(
            self.request, 'Cupón creado correctamente.'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, 'Corrige los errores en el formulario.'
        )
        return super().form_invalid(form)


# Editar cupón existente (solo admin)
class DashboardCuponUpdateView(LoginRequiredMixin, UpdateView):
    model = Cupon
    fields = (
        'codigo', 'descripcion', 'tipo', 'valor',
        'monto_minimo', 'max_usos', 'activo', 'fecha_expiracion'
    )
    template_name = 'dashboard/coupon_form.html'
    success_url = reverse_lazy('dashboard:coupon_list')

    def get(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, 'No tienes permisos de administrador.')
            return redirect('products:list')
        return super().get(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['fecha_expiracion'].widget.attrs.update(
            {'class': 'form-control', 'type': 'datetime-local'}
        )
        form.fields['codigo'].widget.attrs.update(
            {'class': 'form-control'}
        )
        form.fields['descripcion'].widget.attrs.update(
            {'class': 'form-control', 'rows': 2}
        )
        form.fields['valor'].widget.attrs.update(
            {'class': 'form-control', 'step': '0.01'}
        )
        form.fields['monto_minimo'].widget.attrs.update(
            {'class': 'form-control', 'step': '0.01'}
        )
        form.fields['max_usos'].widget.attrs.update(
            {'class': 'form-control'}
        )
        form.fields['tipo'].widget.attrs.update(
            {'class': 'form-select'}
        )
        form.fields['activo'].widget.attrs.update(
            {'class': 'form-check-input'}
        )
        labels = {
            'codigo': 'Código',
            'descripcion': 'Descripción',
            'tipo': 'Tipo de descuento',
            'valor': 'Valor',
            'monto_minimo': 'Monto mínimo',
            'max_usos': 'Usos máximos',
            'activo': 'Activo',
            'fecha_expiracion': 'Fecha de expiración',
        }
        for field_name, label in labels.items():
            form.fields[field_name].label = label
        return form

    def form_valid(self, form):
        messages.success(
            self.request, 'Cupón actualizado correctamente.'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, 'Corrige los errores en el formulario.'
        )
        return super().form_invalid(form)


# Eliminar cupón (solo admin)
class DashboardCuponDeleteView(LoginRequiredMixin, DeleteView):
    model = Cupon
    template_name = 'dashboard/coupon_confirm_delete.html'
    success_url = reverse_lazy('dashboard:coupon_list')
    context_object_name = 'cupon'

    def get(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, 'No tienes permisos de administrador.')
            return redirect('products:list')
        return super().get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(
            request, 'Cupón eliminado correctamente.'
        )
        return super().delete(request, *args, **kwargs)
