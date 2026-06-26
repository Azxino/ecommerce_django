from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.accounts.models import CustomUser
from apps.cart.models import Cupon
from apps.products.models import Categoria, Producto


class Command(BaseCommand):
    help = 'Población inicial de datos de prueba'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creando datos iniciales...')

        if not CustomUser.objects.filter(username='admin').exists():
            admin = CustomUser.objects.create_superuser(
                username='admin',
                email='admin@ropashop.com',
                password='admin123',
                first_name='Admin',
                last_name='Principal',
                role=CustomUser.Role.ADMIN,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Admin creado: admin / admin123'
                )
            )

        if not CustomUser.objects.filter(username='cliente').exists():
            cliente = CustomUser.objects.create_user(
                username='cliente',
                email='cliente@ropashop.com',
                password='cliente123',
                first_name='Cliente',
                last_name='Ejemplo',
                role=CustomUser.Role.CLIENT,
                telefono='5512345678',
                direccion='Calle Principal #123, Ciudad de México',
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Cliente creado: cliente / cliente123'
                )
            )

        categorias_data = [
            {'nombre': 'Camisetas', 'descripcion': 'Camisetas de algodón para hombre y mujer'},
            {'nombre': 'Pantalones', 'descripcion': 'Pantalones casual y formales'},
            {'nombre': 'Chaquetas', 'descripcion': 'Chaquetas y abrigos para todas las temporadas'},
            {'nombre': 'Vestidos', 'descripcion': 'Vestidos elegantes y casual'},
            {'nombre': 'Accesorios', 'descripcion': 'Cinturones, gorras, bufandas y más'},
            {'nombre': 'Calzado', 'descripcion': 'Zapatos, tenis y botas'},
        ]

        categorias = {}
        for cat_data in categorias_data:
            cat, created = Categoria.objects.get_or_create(
                nombre=cat_data['nombre'],
                defaults={'descripcion': cat_data['descripcion']}
            )
            categorias[cat.nombre] = cat
            if created:
                self.stdout.write(f'  Categoría creada: {cat.nombre}')

        productos_data = [
            {'nombre': 'Camiseta Algodón Premium', 'categoria': 'Camisetas', 'precio': 299.00, 'stock': 50, 'destacado': True},
            {'nombre': 'Camiseta Estampada Clásica', 'categoria': 'Camisetas', 'precio': 249.00, 'stock': 35, 'destacado': False},
            {'nombre': 'Camiseta Manga Larga', 'categoria': 'Camisetas', 'precio': 349.00, 'stock': 25, 'destacado': False},
            {'nombre': 'Pantalón Chino Beige', 'categoria': 'Pantalones', 'precio': 599.00, 'stock': 20, 'destacado': True},
            {'nombre': 'Pantalón Mezclilla Clásico', 'categoria': 'Pantalones', 'precio': 699.00, 'stock': 30, 'destacado': True},
            {'nombre': 'Short Deportivo', 'categoria': 'Pantalones', 'precio': 349.00, 'stock': 45, 'destacado': False},
            {'nombre': 'Chaqueta Impermeable', 'categoria': 'Chaquetas', 'precio': 1299.00, 'stock': 15, 'destacado': True},
            {'nombre': 'Chamarra Casual', 'categoria': 'Chaquetas', 'precio': 899.00, 'stock': 20, 'destacado': False},
            {'nombre': 'Vestido Floral', 'categoria': 'Vestidos', 'precio': 549.00, 'stock': 3, 'destacado': True},
            {'nombre': 'Vestido Casual Negro', 'categoria': 'Vestidos', 'precio': 449.00, 'stock': 12, 'destacado': False},
            {'nombre': 'Gorra Deportiva', 'categoria': 'Accesorios', 'precio': 199.00, 'stock': 60, 'destacado': False},
            {'nombre': 'Cinturón Cuero', 'categoria': 'Accesorios', 'precio': 399.00, 'stock': 0, 'destacado': False},
            {'nombre': 'Bufanda Tejida', 'categoria': 'Accesorios', 'precio': 249.00, 'stock': 40, 'destacado': False},
            {'nombre': 'Tenis Casual Blanco', 'categoria': 'Calzado', 'precio': 899.00, 'stock': 4, 'destacado': True},
            {'nombre': 'Botas Invierno', 'categoria': 'Calzado', 'precio': 1499.00, 'stock': 10, 'destacado': False},
        ]

        for prod_data in productos_data:
            producto, created = Producto.objects.get_or_create(
                nombre=prod_data['nombre'],
                defaults={
                    'categoria': categorias[prod_data['categoria']],
                    'descripcion': f'{prod_data["nombre"]} de alta calidad. '
                                  f'Diseño moderno y cómodo. Ideal para cualquier ocasión.',
                    'precio': prod_data['precio'],
                    'stock': prod_data['stock'],
                    'disponible': prod_data['stock'] > 0,
                    'destacado': prod_data['destacado'],
                }
            )
            if created:
                self.stdout.write(f'  Producto creado: {producto.nombre}')

        cupones_data = [
            {'codigo': 'BIENVENIDO10', 'tipo': Cupon.TipoDescuento.PORCENTAJE, 'valor': 10,
             'monto_minimo': 500, 'max_usos': 50, 'dias_valido': 30},
            {'codigo': 'DESCUENTO50', 'tipo': Cupon.TipoDescuento.MONTO_FIJO, 'valor': 50,
             'monto_minimo': 300, 'max_usos': 20, 'dias_valido': 15},
            {'codigo': 'ENVIOGRATIS', 'tipo': Cupon.TipoDescuento.PORCENTAJE, 'valor': 5,
             'monto_minimo': 200, 'max_usos': 100, 'dias_valido': 60},
            {'codigo': 'VERANO20', 'tipo': Cupon.TipoDescuento.PORCENTAJE, 'valor': 20,
             'monto_minimo': 1000, 'max_usos': 0, 'dias_valido': 45},
        ]

        for cupon_data in cupones_data:
            cupon, created = Cupon.objects.get_or_create(
                codigo=cupon_data['codigo'],
                defaults={
                    'tipo': cupon_data['tipo'],
                    'valor': cupon_data['valor'],
                    'monto_minimo': cupon_data['monto_minimo'],
                    'max_usos': cupon_data['max_usos'],
                    'descripcion': f'Cupón de {"%" if cupon_data["tipo"] == "PORCENTAJE" else "$"}'
                                   f'{cupon_data["valor"]} de descuento',
                    'fecha_expiracion': timezone.now() + timedelta(days=cupon_data['dias_valido']),
                }
            )
            if created:
                self.stdout.write(f'  Cupón creado: {cupon.codigo}')

        self.stdout.write(self.style.SUCCESS('\n¡Datos iniciales creados exitosamente!'))
