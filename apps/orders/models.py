from decimal import Decimal

from django.conf import settings
from django.db import models

from apps.products.models import Producto


class Pedido(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        CONFIRMADO = 'CONFIRMADO', 'Confirmado'
        ENVIADO = 'ENVIADO', 'Enviado'
        ENTREGADO = 'ENTREGADO', 'Entregado'
        CANCELADO = 'CANCELADO', 'Cancelado'

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='pedidos', verbose_name='Usuario'
    )
    estado = models.CharField(
        max_length=15, choices=Estado.choices,
        default=Estado.PENDIENTE, verbose_name='Estado'
    )
    subtotal = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Subtotal'
    )
    descuento = models.DecimalField(
        max_digits=10, decimal_places=2,
        default=0, verbose_name='Descuento'
    )
    total = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Total'
    )
    cupon_codigo = models.CharField(
        max_length=20, blank=True, null=True,
        verbose_name='Cupón aplicado'
    )
    notas = models.TextField(
        blank=True, null=True, verbose_name='Notas'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Creado'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Actualizado'
    )

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-created_at']

    def __str__(self):
        return f'Pedido #{self.id} - {self.usuario.username} ({self.get_estado_display()})'


class DetallePedido(models.Model):
    pedido = models.ForeignKey(
        Pedido, on_delete=models.CASCADE,
        related_name='detalles', verbose_name='Pedido'
    )
    producto = models.ForeignKey(
        Producto, on_delete=models.PROTECT,
        related_name='detalles_pedido', verbose_name='Producto'
    )
    precio = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Precio unitario'
    )
    cantidad = models.PositiveIntegerField(verbose_name='Cantidad')
    subtotal = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Subtotal'
    )

    class Meta:
        verbose_name = 'Detalle de pedido'
        verbose_name_plural = 'Detalles de pedidos'

    def __str__(self):
        return f'{self.producto.nombre} x {self.cantidad}'
