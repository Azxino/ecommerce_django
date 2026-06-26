from django.contrib.auth.models import AbstractUser
from django.db import models


# Modelo de usuario personalizado con roles (Administrador / Cliente)
class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        CLIENT = 'CLIENTE', 'Cliente'

    # Rol del usuario: determina qué secciones del sistema puede acceder
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.CLIENT,
        verbose_name='Rol'
    )
    # Teléfono de contacto del usuario
    telefono = models.CharField(
        max_length=15, blank=True, null=True, verbose_name='Teléfono'
    )
    # Dirección de envío del usuario
    direccion = models.TextField(
        blank=True, null=True, verbose_name='Dirección'
    )

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    # Representación en texto del usuario (nombre + rol)
    def __str__(self):
        return f'{self.get_full_name() or self.username} ({self.get_role_display()})'

    # Propiedad: verifica si el usuario es administrador
    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    # Propiedad: verifica si el usuario es cliente
    @property
    def is_client(self):
        return self.role == self.Role.CLIENT
