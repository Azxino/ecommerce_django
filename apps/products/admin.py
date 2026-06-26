from django.contrib import admin

from .models import Categoria, Producto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo', 'created_at')
    search_fields = ('nombre',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        'nombre', 'categoria', 'precio', 'stock',
        'disponible', 'destacado', 'created_at'
    )
    list_filter = ('categoria', 'disponible', 'destacado')
    search_fields = ('nombre', 'descripcion')
    list_editable = ('precio', 'stock', 'disponible', 'destacado')
