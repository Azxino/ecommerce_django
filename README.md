# D'gala - Tienda de Ropa en Línea

Sistema web de comercio electrónico desarrollado con Django, diseñado para la venta de ropa y accesorios con gestión completa de catálogo, carrito de compras, pedidos y panel administrativo.

---

## Características Principales

- **Catálogo de Productos**: Navegación por categorías, búsqueda por nombre/descripción, productos destacados.
- **Carrito de Compras**: Basado en sesión, sin necesidad de registro para agregar productos.
- **Sistema de Cupones**: Descuentos porcentuales o montos fijos con validaciones de monto mínimo y vigencia.
- **Gestión de Pedidos**: Flujo completo PENDIENTE → CONFIRMADO → ENVIADO → ENTREGADO, con cancelación y restauración de stock.
- **Panel Administrativo**: Dashboard con estadísticas, CRUD completo de usuarios, productos, categorías, pedidos y cupones.
- **Autenticación y Roles**: Sistema de usuarios con roles ADMIN y CLIENTE, registro con auto-login.

---

## Tecnologías

| Tecnología | Versión |
|-----------|---------|
| Python | 3.10+ |
| Django | 5.2+ |
| SQLite | 3.x |
| Bootstrap | 5.x |
| Pillow | 10.x |

---

## Estructura del Proyecto

```
ropa_shop/
├── config/                # Configuración principal (settings, urls, wsgi, asgi)
│   ├── settings.py        # Configuración general del proyecto
│   ├── urls.py            # Enrutamiento raíz
│   ├── wsgi.py            # Punto de entrada WSGI
│   └── asgi.py            # Punto de entrada ASGI
├── apps/                  # Aplicaciones funcionales
│   ├── accounts/          # Cuentas de usuario, autenticación y roles
│   ├── products/          # Catálogo de productos y categorías
│   ├── cart/              # Carrito de compras y sistema de cupones
│   ├── orders/            # Gestión de pedidos y detalle de pedidos
│   └── dashboard/         # Panel de administración con CRUD y estadísticas
├── templates/             # Plantillas HTML (herencia de plantillas Django)
│   ├── base.html          # Plantilla base con navbar y footer
│   ├── products/          # Vistas públicas de productos
│   ├── cart/              # Vista del carrito de compras
│   ├── orders/            # Vistas de pedidos del cliente
│   └── dashboard/         # Panel admin con sidebar de navegación
├── static/                # Archivos estáticos
│   ├── css/style.css      # Estilos personalizados
│   ├── js/script.js       # JavaScript personalizado
│   └── bootstrap/         # Bootstrap 5 (CSS + JS)
├── media/                 # Archivos subidos (imágenes de productos)
├── manage.py              # Punto de entrada de Django
└── requirements.txt       # Dependencias del proyecto
```

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd ropa_shop
```

### 2. Crear y activar entorno virtual

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno (opcional)

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `DJANGO_SECRET_KEY` | Clave secreta de Django | `django-insecure-dev-key-change-in-production` |
| `DJANGO_DEBUG` | Modo debug | `True` |
| `DJANGO_ALLOWED_HOSTS` | Hosts permitidos | `127.0.0.1,localhost` |

### 5. Aplicar migraciones

```bash
python manage.py migrate
```

### 6. Cargar datos de prueba (opcional)

```bash
python manage.py seed_data
```

Esto crea:
- **Admin**: `admin` / `admin123`
- **Cliente**: `cliente` / `cliente123`
- **6 categorías** y **15 productos**
- **4 cupones**: `BIENVENIDO10`, `DESCUENTO50`, `ENVIOGRATIS`, `VERANO20`

### 7. Iniciar servidor

```bash
python manage.py runserver
```

El sistema estará disponible en `http://127.0.0.1:8000/`.

---

## Rutas del Sistema

| Ruta | Módulo | Descripción |
|------|--------|-------------|
| `/` | - | Redirección a listado de productos |
| `/cuenta/` | accounts | Registro, inicio de sesión, perfil |
| `/productos/` | products | Catálogo y detalle de productos |
| `/carrito/` | cart | Carrito de compras y cupones |
| `/pedidos/` | orders | Historial y detalle de pedidos |
| `/panel/` | dashboard | Panel de administración |
| `/admin/` | Django Admin | Administración nativa de Django |

---

## Modelo de Datos

```
CustomUser (accounts) ──── 1:N ──── Pedido (orders)
Categoria  (products) ──── 1:N ──── Producto (products)
Producto   (products) ──── 1:N ──── DetallePedido (orders)
Pedido     (orders)   ──── 1:N ──── DetallePedido (orders)
Cupon      (cart)     ──── independiente (aplicado en sesión)
```

---

## Roles de Usuario

- **ADMIN**: Acceso al panel de administración (`/panel/`), gestión completa de usuarios, productos, categorías, pedidos y cupones.
- **CLIENTE**: Registro, navegación de productos, compras, historial de pedidos, edición de perfil.

---

## Licencia

Este proyecto es de uso educativo y demostrativo.
