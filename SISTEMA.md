# D'gala — Documentación del Sistema

## Módulos y Funcionalidades

---

### 1. `apps.accounts` — Cuentas de Usuario

Módulo de autenticación y gestión de usuarios con roles.

| Funcionalidad | Clase/Función | Descripción |
|--------------|---------------|-------------|
| Modelo de usuario | `CustomUser(AbstractUser)` | Usuario personalizado con campo `role` (`ADMIN`/`CLIENTE`), `telefono` y `direccion` |
| Registro | `RegistroView(CreateView)` | Registro con validación de email único, auto-login y mensaje de bienvenida |
| Inicio de sesión | `LoginView(FormView)` | Login con soporte para `?next=` y mensajes de error personalizados |
| Cierre de sesión | `LogoutView(TemplateView)` | Logout solo por POST (protegido CSRF), con cabeceras anti-caché |
| Edición de perfil | `PerfilView(UpdateView)` | Usuario autenticado edita su nombre, email, teléfono y dirección |
| Decoradores | `admin_required`, `client_required` | Decoradores para restringir acceso por rol |
| Middleware | `NoCacheMiddleware` | Agrega `Cache-Control: no-cache, no-store, must-revalidate, private` |
| Comando seed | `seed_data.py` | Pobla la base de datos con datos de prueba (admin, cliente, productos, cupones) |

**Formularios**: `RegistroForm` (username, email, nombre, apellido, teléfono, dirección, contraseñas), `LoginForm` (username, password con widgets Bootstrap), `UsuarioForm` (admin CRUD), `PerfilForm` (edición de perfil).

---

### 2. `apps.products` — Productos y Categorías

Módulo de catálogo con navegación y búsqueda.

| Funcionalidad | Clase/Función | Descripción |
|--------------|---------------|-------------|
| Modelo Categoria | `Categoria` | Nombre, slug automático, descripción, activo, fecha de creación |
| Modelo Producto | `Producto` | Categoría (FK), nombre, slug, descripción, precio, stock, imagen, disponible, destacado, timestamps |
| Propiedades | `tiene_stock`, `stock_bajo` | `tiene_stock`: stock > 0; `stock_bajo`: 0 < stock <= 5 |
| Listado público | `ProductoListView(ListView)` | Paginación (12 por página), búsqueda por nombre/descripción, filtro de destacados |
| Detalle producto | `ProductoDetailView(DetailView)` | Vista detalle con productos relacionados de la misma categoría |
| Filtro por categoría | `CategoriaListView(ListView)` | Productos filtrados por slug de categoría, paginado |
| Context processor | `categorias_globales` | Inyecta todas las categorías activas en todas las plantillas |
| Formularios | `CategoriaForm`, `ProductoForm` | Validación de precio > 0 en `ProductoForm` |

**Admin**: `CategoriaAdmin` con búsqueda por nombre; `ProductoAdmin` con filtros por categoría/disponible/destacado y edición inline de precio, stock, disponible, destacado.

---

### 3. `apps.cart` — Carrito de Compras y Cupones

Módulo de carrito basado en sesión con sistema de descuentos.

| Funcionalidad | Clase/Función | Descripción |
|--------------|---------------|-------------|
| Clase carrito | `Cart` | Carrito en sesión (`CART_SESSION_ID`). Métodos: `add`, `remove`, `clear`, `save`, `set_cupon`, `get_cupon_descuento`. Propiedades: `subtotal`, `total`, `descuento`, `total_items`. Iterador con datos completos del producto |
| Agregar producto | `add_to_cart` | POST, verifica stock disponible, actualiza cantidad si ya existe |
| Eliminar producto | `remove_from_cart` | POST, elimina producto del carrito |
| Actualizar cantidad | `update_cart` | POST, verifica stock antes de actualizar |
| Limpiar carrito | `clear_cart` | POST, vacía el carrito completo |
| Aplicar cupón | `apply_cupon` | POST, valida código, monto mínimo, vigencia y usos |
| Eliminar cupón | `remove_cupon` | POST, remueve cupón de la sesión |
| Detalle carrito | `CartDetailView(TemplateView)` | Muestra tabla de productos, formulario de cupón y resumen |
| Context processor | `cart_items_count` | Inyecta contador de items en todas las plantillas (0 si no autenticado) |

**Modelo Cupon**: Código único, tipo (`PORCENTAJE`/`MONTO_FIJO`), valor, monto mínimo, usos máximos/actuales, activo, fecha de expiración. Propiedades: `es_valido` (valida activo, no expirado, usos disponibles). Métodos: `aplicar_descuento(subtotal)` (según tipo), `incrementar_uso()`.

---

### 4. `apps.orders` — Pedidos

Módulo de gestión de pedidos con control de inventario.

| Funcionalidad | Clase/Función | Descripción |
|--------------|---------------|-------------|
| Modelo Pedido | `Pedido` | Estados: `PENDIENTE`, `CONFIRMADO`, `ENVIADO`, `ENTREGADO`, `CANCELADO`. Campos: usuario (FK), subtotal, descuento, total, código de cupón, notas, timestamps |
| Modelo DetallePedido | `DetallePedido` | pedido (FK), producto (FK con `PROTECT`), precio, cantidad, subtotal |
| Crear pedido | `create_order` | POST transaccional: verifica stock, descuenta inventario, aplica cupón, limpia carrito, crea pedido con detalles |
| Cancelar pedido | `cancel_order` | POST, solo si está PENDIENTE o CONFIRMADO, restaura stock |
| Listar pedidos | `PedidoListView(ListView)` | Pedidos del usuario autenticado, paginado (10), más recientes primero |
| Detalle pedido | `PedidoDetailView(DetailView)` | Detalle completo del pedido (solo el dueño) |
| Formularios | `PedidoForm` (solo notas), `CambiarEstadoForm` (solo estado) | Para uso en dashboard y frontend |

**Reglas de negocio**:
- No se puede crear pedido con carrito vacío.
- No se puede cancelar pedido si ya fue ENVIADO o ENTREGADO.
- Al cancelar se restaura el stock de todos los productos.
- `PROTECT` en producto evita eliminar productos con pedidos asociados.

---

### 5. `apps.dashboard` — Panel de Administración

Módulo de administración con CRUD completo y estadísticas.

| Funcionalidad | Clase/Función | Descripción |
|--------------|---------------|-------------|
| Dashboard home | `DashboardHomeView(TemplateView)` | Tarjetas con: total usuarios, clientes, productos activos, pedidos, pendientes, ingresos totales, stock bajo, últimos pedidos, últimos usuarios registrados |
| CRUD Usuarios | 4 vistas (list, create, update, delete) | Lista paginada (15), búsqueda, formularios con `UsuarioForm` |
| CRUD Productos | 4 vistas (list, create, update, delete) | Lista paginada (15) con búsqueda por nombre, formularios con `ProductoForm` |
| CRUD Categorías | 4 vistas (list, create, update, delete) | Gestión completa de categorías |
| CRUD Pedidos | 3 vistas (list, detail, update) | Lista con filtro por estado, detalle con items, cambio de estado |
| CRUD Cupones | 4 vistas (list, create, update, delete) | Gestión completa de cupones de descuento |
| Seguridad | Verificación en `get()` | Todas las vistas del dashboard verifican `request.user.is_admin` |

**Total: 22 vistas** (1 home + 4 usuarios + 4 productos + 4 categorías + 3 pedidos + 4 cupones + 2 adicionales).

---

### Arquitectura General

```
CLIENTE (Navegador)
    │
    ├── HTTP Request
    │
    ▼
config/urls.py (Enrutador raíz)
    │
    ├── /cuenta/         → apps.accounts.urls
    ├── /productos/      → apps.products.urls
    ├── /carrito/        → apps.cart.urls
    ├── /pedidos/        → apps.orders.urls
    ├── /panel/          → apps.dashboard.urls
    └── /admin/          → Django Admin
            │
            ▼
        views.py (Lógica de negocio)
            │
            ├── models.py (Modelos → SQLite)
            ├── forms.py (Validación de datos)
            └── templates/*.html (Renderizado)
                    │
                    ▼
            Respuesta HTTP (HTML)
```

**Patrón**: Django MTV (Model-Template-View) — equivalente a MVC donde:
- **Model**: `models.py` — define estructura de datos y lógica de negocio.
- **Template**: `templates/*.html` — presentación con herencia de plantillas.
- **View**: `views.py` — lógica de control, orquestación modelo-vista.

**Patrones de diseño adicionales**:
- **Class-based Views (CBV)**: Vistas genéricas de Django (`ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`, `FormView`, `TemplateView`).
- **Herencia de plantillas**: `base.html` → `base_admin.html` → vistas específicas.
- **Context Processors**: Funciones que inyectan datos globales en todas las plantillas.
- **Middleware**: Interceptación de requests/responses a nivel global.
- **Session-based State**: Carrito de compras almacenado en sesión HTTP.
- **Command Pattern**: Comando personalizado `seed_data` para poblar la base de datos.

---

## Interfaz y Recursos Locales

### Sistema de Plantillas

```
templates/
├── base.html                          # Plantilla raíz
│   ├── Navbar: Logo "D'gala", enlace Productos, carrito con badge,
│   │           login/registro o dropdown usuario
│   ├── Footer: Marca, enlaces, contacto
│   ├── Messages flash (Bootstrap alerts con auto-dismiss JS)
│   │
│   ├── products/
│   │   ├── product_list.html          # Buscador + grid productos + paginación
│   │   ├── product_detail.html        # Breadcrumbs + imagen + info + formulario carrito + relacionados
│   │   └── category_list.html         # Productos filtrados por categoría
│   │
│   ├── cart/
│   │   └── cart_detail.html           # Tabla items + formulario cupón + resumen + botón pedido
│   │
│   ├── orders/
│   │   ├── order_list.html            # Tabla pedidos con badges de estado
│   │   └── order_detail.html          # Detalle pedido + botón cancelar
│   │
│   └── dashboard/
│       ├── base_admin.html            # Extiende base.html + sidebar admin
│       ├── home.html                  # Dashboard con tarjetas de estadísticas
│       ├── user_list.html             # CRUD usuarios (tabla)
│       ├── user_form.html             # Crear/Editar usuario
│       ├── user_confirm_delete.html   # Confirmación de eliminación
│       ├── product_list.html          # CRUD productos (tabla + búsqueda)
│       ├── product_form.html          # Crear/Editar producto
│       ├── product_confirm_delete.html
│       ├── category_list.html         # CRUD categorías
│       ├── category_form.html
│       ├── category_confirm_delete.html
│       ├── order_list.html            # Pedidos + filtro por estado
│       ├── order_detail.html          # Detalle pedido + formulario cambio estado
│       ├── coupon_list.html           # CRUD cupones
│       ├── coupon_form.html
│       └── coupon_confirm_delete.html
```

**NOTA**: No existen `templates/accounts/register.html`, `login.html` ni `profile.html`. Las vistas referencian estas plantillas pero no están creadas, lo que generará errores `TemplateDoesNotExist`.

### Archivos Estáticos

```
static/
├── css/
│   └── style.css          # 102 líneas — estilos personalizados
│       ├── .product-card  → sombra, transición, hover
│       ├── .product-img   → altura fija, object-fit: cover
│       ├── .stock-bajo    → color rojo
│       ├── .stock-agotado → color gris
│       ├── Dashboard      → sidebar fijo, tarjetas, transiciones
│       └── Responsive     → ajustes para móvil
│
├── js/
│   └── script.js          # 29 líneas — funcionalidad
│       ├── Auto-dismiss alerts  → 5 segundos
│       ├── Bootstrap tooltips   → inicialización global
│       └── Confirmación eliminación → data-confirm attribute
│
└── bootstrap/
    ├── css/
    │   └── bootstrap.min.css     # Bootstrap 5
    └── js/
        └── bootstrap.bundle.min.js
```

**CDN externo**: Bootstrap Icons vía `https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/`.

### Assets Subidos por Usuario

```
media/
└── products/              # Imágenes de productos (upload_to='products/')
```

Actualmente vacío. Las imágenes se sirven en desarrollo mediante `django.conf.urls.static` cuando `DEBUG=True`.

---

## Seguridad y Buenas Prácticas

### Autenticación y Autorización

| Aspecto | Implementación |
|---------|---------------|
| Modelo de usuario | `CustomUser(AbstractUser)` con campo `role` (`ADMIN`/`CLIENTE`) |
| Configuración | `AUTH_USER_MODEL = 'accounts.CustomUser'` |
| Protección de vistas | `LoginRequiredMixin` en perfil, pedidos y dashboard |
| Roles | Decoradores `@admin_required` y `@client_required` |
| Dashboard | Verificación `request.user.is_admin` en cada vista |
| Logout | Solo por POST con `@csrf_protect` y `@never_cache` |

### Protección CSRF

- `CsrfViewMiddleware` activo en `settings.MIDDLEWARE`.
- Todos los formularios POST usan `{% csrf_token %}` en plantillas.
- Las vistas de logout/logout están protegidas con `@csrf_protect`.
- Las operaciones de carrito y pedidos usan `@require_POST` + `@csrf_protect`.

### Seguridad en Sesiones

- `SESSION_ENGINE = 'django.contrib.sessions.backends.db'` (sesiones en base de datos).
- El carrito se almacena en la sesión bajo la clave `CART_SESSION_ID = 'cart'`.
- Middleware `NoCacheMiddleware` evita caching de páginas después del logout.

### Cabeceras de Seguridad HTTP

| Cabecera | Valor | Origen |
|----------|-------|--------|
| `Cache-Control` | `no-cache, no-store, must-revalidate, private` | `NoCacheMiddleware` |
| `Pragma` | `no-cache` | `NoCacheMiddleware` |
| `Expires` | `0` | `NoCacheMiddleware` |
| `X-Frame-Options` | `DENY` | `XFrameOptionsMiddleware` (Django) |

### Validaciones y Reglas de Negocio

| Validación | Ubicación | Detalle |
|-----------|-----------|---------|
| Precio > 0 | `ProductoForm.clean_precio()` | Validación a nivel de formulario |
| Stock suficiente | `add_to_cart`, `update_cart`, `create_order` | Verificación antes de operar |
| Email único | `RegistroForm.clean_email()` | Verifica que el email no exista |
| Contraseñas seguras | `AUTH_PASSWORD_VALIDATORS` | MinimumLength, CommonPassword, NumericPassword |
| Cupón válido | `apply_cupon` | Verifica activo, no expirado, monto mínimo, usos disponibles |
| Cancelación pedido | `cancel_order` | Solo si estado es PENDIENTE o CONFIRMADO |
| Protección de datos | `DetallePedido.producto` | `on_delete=PROTECT` (no eliminar producto con pedidos) |

### Buenas Prácticas Implementadas

1. **Mensajes flash**: Sistema `django.contrib.messages` con clasificación por tipo (success, error, warning, info) y estilos Bootstrap.
2. **Redirección post-login**: Soporte para parámetro `?next=` en login.
3. **Paginación**: Todas las listas usan paginación (12-15 items por página).
4. **Slugs automáticos**: Categorías y productos generan slug automático desde el nombre.
5. **Validación de datos**: Formularios con `clean_*` methods y validadores de Django.
6. **Herencia de plantillas**: Sistema modular con `base.html` como raíz.
7. **Context processors**: Datos globales (categorías, contador carrito) disponibles en todas las plantillas.
8. **Configuración por entorno**: `SECRET_KEY`, `DEBUG` y `ALLOWED_HOSTS` configurables vía variables de entorno.
9. **Transacciones implícitas**: Las vistas de creación de pedidos operan como una unidad atómica.
10. **Zona horaria**: Configurada a `America/Mexico_City`.

### Pendientes de Mejora

| Aspecto | Estado | Recomendación |
|---------|--------|---------------|
| Plantillas accounts | ❌ Faltantes | Crear `templates/accounts/register.html`, `login.html`, `profile.html` |
| Pruebas | ❌ No existen | Implementar tests unitarios e integración con pytest |
| SECRET_KEY hardcodeada | ⚠️ Fallback inseguro | Configurar variable de entorno en producción |
| HTTPS/SSL | ❌ No configurado | Usar `SECURE_SSL_REDIRECT`, HSTS en producción |
| CORS | ❌ No configurado | Evaluar si se necesita para API futura |
| Logging | ❌ No configurado | Agregar configuración de logging a settings.py |
| Imagen por defecto | ⚠️ Sin placeholder | Agregar imagen default para productos sin foto |
| Traducciones | ⚠️ Sin archivos .po | Generar y compilar traducciones si se requiere i18n |
| Docker | ❌ No disponible | Crear Dockerfile y docker-compose para despliegue |
| .gitignore | ❌ Ausente | Agregar .gitignore para excluir venv, pycache, db.sqlite3, media |
