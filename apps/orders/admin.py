from django.contrib import admin

from .models import DetallePedido, Pedido


class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    readonly_fields = ('producto', 'precio', 'cantidad', 'subtotal')


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'usuario', 'estado', 'total',
        'created_at', 'updated_at'
    )
    list_filter = ('estado', 'created_at')
    search_fields = ('usuario__username', 'usuario__email')
    inlines = [DetallePedidoInline]
    readonly_fields = (
        'usuario', 'subtotal', 'descuento', 'total',
        'cupon_codigo', 'created_at'
    )


@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'producto', 'cantidad', 'precio', 'subtotal')
    readonly_fields = ('pedido', 'producto', 'precio', 'cantidad', 'subtotal')
