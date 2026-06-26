from django.contrib import admin

from .models import Cupon


@admin.register(Cupon)
class CuponAdmin(admin.ModelAdmin):
    list_display = (
        'codigo', 'tipo', 'valor', 'monto_minimo',
        'activo', 'fecha_expiracion', 'usos_actuales', 'max_usos'
    )
    list_filter = ('tipo', 'activo')
    search_fields = ('codigo', 'descripcion')
