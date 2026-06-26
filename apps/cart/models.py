from django.db import models
from django.utils import timezone


class Cupon(models.Model):
    class TipoDescuento(models.TextChoices):
        PORCENTAJE = 'PORCENTAJE', 'Porcentaje (%)'
        MONTO_FIJO = 'MONTO_FIJO', 'Monto fijo ($)'

    codigo = models.CharField(
        max_length=20, unique=True, verbose_name='Código'
    )
    descripcion = models.CharField(
        max_length=255, blank=True, verbose_name='Descripción'
    )
    tipo = models.CharField(
        max_length=15, choices=TipoDescuento.choices,
        default=TipoDescuento.PORCENTAJE, verbose_name='Tipo'
    )
    valor = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Valor'
    )
    monto_minimo = models.DecimalField(
        max_digits=10, decimal_places=2,
        default=0, verbose_name='Monto mínimo'
    )
    max_usos = models.PositiveIntegerField(
        default=0, verbose_name='Usos máximos',
        help_text='0 = ilimitado'
    )
    usos_actuales = models.PositiveIntegerField(
        default=0, verbose_name='Usos actuales'
    )
    activo = models.BooleanField(default=True, verbose_name='Activo')
    fecha_expiracion = models.DateTimeField(
        verbose_name='Fecha de expiración'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Creado'
    )

    class Meta:
        verbose_name = 'Cupón'
        verbose_name_plural = 'Cupones'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.codigo} ({self.valor}{"%" if self.tipo == "PORCENTAJE" else "$"})'

    @property
    def es_valido(self):
        if not self.activo:
            return False
        if self.fecha_expiracion and self.fecha_expiracion < timezone.now():
            return False
        if self.max_usos > 0 and self.usos_actuales >= self.max_usos:
            return False
        return True

    def aplicar_descuento(self, subtotal):
        if not self.es_valido:
            return subtotal
        if subtotal < self.monto_minimo:
            return subtotal
        if self.tipo == self.TipoDescuento.PORCENTAJE:
            descuento = subtotal * (self.valor / 100)
            return max(subtotal - descuento, 0)
        return max(subtotal - self.valor, 0)

    def incrementar_uso(self):
        self.usos_actuales += 1
        self.save(update_fields=['usos_actuales'])
