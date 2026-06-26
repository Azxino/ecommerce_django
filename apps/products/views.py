# Vistas de productos: listado público, detalle, y filtrado por categoría
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from .models import Categoria, Producto


# Listado de productos disponibles con búsqueda y destacados
class ProductoListView(ListView):
    model = Producto
    template_name = 'products/product_list.html'
    context_object_name = 'productos'
    paginate_by = 12

    # Filtra solo productos disponibles, soporta búsqueda por nombre/descripción
    def get_queryset(self):
        queryset = Producto.objects.filter(
            disponible=True
        ).select_related('categoria')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query)
                | Q(descripcion__icontains=query)
            )
        return queryset

    # Agrega categorías y productos destacados al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['categorias'] = Categoria.objects.filter(activo=True)
        context['destacados'] = Producto.objects.filter(
            disponible=True, destacado=True
        )[:4]
        return context


# Detalle de un producto con productos relacionados de la misma categoría
class ProductoDetailView(DetailView):
    model = Producto
    template_name = 'products/product_detail.html'
    context_object_name = 'producto'

    # Solo muestra productos disponibles
    def get_queryset(self):
        return Producto.objects.filter(
            disponible=True
        ).select_related('categoria')

    # Agrega productos relacionados (misma categoría, excluyendo el actual)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['relacionados'] = Producto.objects.filter(
            categoria=self.object.categoria,
            disponible=True
        ).exclude(id=self.object.id)[:4]
        return context


# Listado de productos filtrados por categoría (usando slug)
class CategoriaListView(ListView):
    model = Producto
    template_name = 'products/category_list.html'
    context_object_name = 'productos'
    paginate_by = 12

    # Obtiene la categoría por slug y filtra productos
    def get_queryset(self):
        self.categoria = get_object_or_404(
            Categoria, slug=self.kwargs['slug'], activo=True
        )
        return Producto.objects.filter(
            categoria=self.categoria, disponible=True
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categoria'] = self.categoria
        context['categorias'] = Categoria.objects.filter(activo=True)
        return context
