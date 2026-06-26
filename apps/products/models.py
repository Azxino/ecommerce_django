from django.db import models
from django.utils.text import slugify


class Categoria(models.Model):
    nombre = models.CharField(
        max_length=100, unique=True, verbose_name='Nombre'
    )
    slug = models.SlugField(
        max_length=120, unique=True, blank=True, editable=False
    )
    descripcion = models.TextField(
        blank=True, null=True, verbose_name='Descripción'
    )
    activo = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Creado'
    )

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)


class Producto(models.Model):
    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE,
        related_name='productos', verbose_name='Categoría'
    )
    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    slug = models.SlugField(
        max_length=220, unique=True, blank=True, editable=False
    )
    descripcion = models.TextField(verbose_name='Descripción')
    precio = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Precio'
    )
    stock = models.PositiveIntegerField(
        default=0, verbose_name='Stock'
    )
    imagen = models.ImageField(
        upload_to='products/', blank=True, null=True,
        verbose_name='Imagen'
    )
    disponible = models.BooleanField(default=True, verbose_name='Disponible')
    destacado = models.BooleanField(default=False, verbose_name='Destacado')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Creado'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Actualizado'
    )

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-created_at']

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    @property
    def tiene_stock(self):
        return self.stock > 0

    @property
    def stock_bajo(self):
        return 0 < self.stock <= 5
