# Patrones de Diseño — D'gala

---

## 1. Model-View-Template (MTV) / Model-View-Controller (MVC)

**Definición**: Patrón arquitectónico que separa la aplicación en tres componentes: Modelo (datos y lógica de negocio), Vista (lógica de presentación y control) y Plantilla (interfaz de usuario). Django implementa una variante llamada MTV donde la Vista actúa como controlador.

**Ubicación en el proyecto**: Todo el proyecto está estructurado bajo este patrón.

| Componente | Rol | Ubicación |
|-----------|-----|-----------|
| **Model** | Datos y reglas de negocio | `apps/*/models.py` |
| **View** | Lógica de control y orquestación | `apps/*/views.py` |
| **Template** | Presentación (HTML) | `templates/*.html` |

**Ejemplo — Flujo completo**:
1. `config/urls.py:9` enruta `GET /productos/` hacia `ProductoListView`
2. `apps/products/views.py:13` — `ProductoListView` obtiene datos via `Producto.objects.all()`
3. `templates/products/product_list.html` — Renderiza el listado HTML

**Fragmento** (`apps/products/views.py:13-28`):
```python
class ProductoListView(ListView):
    model = Producto
    template_name = 'products/product_list.html'
    context_object_name = 'productos'
    paginate_by = 12
```

---

## 2. Class-based Views (CBV) — Template Method

**Definición**: Las vistas basadas en clases de Django implementan el patrón Template Method. La clase base define el esqueleto del algoritmo (get, post, form_valid, etc.) y las subclases sobrescriben métodos específicos para personalizar el comportamiento sin cambiar la estructura general.

**Ubicación en el proyecto**: Todas las vistas del sistema (25+ vistas).

**Ejemplos**:

| Clase Base | Métodos Sobrescritos | Ubicación |
|-----------|---------------------|-----------|
| `CreateView` | `form_valid()`, `form_invalid()`, `get()` | `apps/accounts/views.py:16` — `RegistroView` |
| `FormView` | `form_valid()`, `form_invalid()`, `get()` | `apps/accounts/views.py:50` — `LoginView` |
| `UpdateView` | `form_valid()`, `form_invalid()`, `get_object()` | `apps/accounts/views.py:98` — `PerfilView` |
| `ListView` | (usa paginate_by, model, template_name) | `apps/products/views.py:13` — `ProductoListView` |
| `DetailView` | (usa model, slug_field) | `apps/products/views.py:31` — `ProductoDetailView` |
| `DeleteView` | (hereda comportamiento) | `apps/dashboard/views.py` — CRUD delete |

**Fragmento** (`apps/dashboard/views.py:150-165`):
```python
class DashboardUsuarioCreateView(CreateView):
    model = CustomUser
    form_class = UsuarioForm
    template_name = 'dashboard/user_form.html'
    success_url = reverse_lazy('dashboard:user_list')

    def get(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return redirect('products:list')
        return super().get(request, *args, **kwargs)
```

---

## 3. Decorator Pattern

**Definición**: Patrón estructural que permite añadir comportamiento adicional a un objeto (o función) de forma dinámica, envolviendo la función original con una función decoradora.

**Ubicación en el proyecto**:

### Decoradores personalizados

**`admin_required`** — `apps/accounts/decorators.py:4-12`

```python
def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin:
            return view_func(request, *args, **kwargs)
        return redirect('products:list')
    return _wrapped_view
```

**`client_required`** — `apps/accounts/decorators.py:14-22`

```python
def client_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_client:
            return view_func(request, *args, **kwargs)
        return redirect('dashboard:home')
    return _wrapped_view
```

### Decoradores de Django/framework

| Decorador | Propósito | Ubicación de uso |
|-----------|-----------|-----------------|
| `@require_POST` | Restringe vista a método POST | `apps/cart/views.py:31,49,67,84,100,117` |
| `@csrf_protect` | Protege contra CSRF | `apps/accounts/views.py:85` |
| `@never_cache` | Evita caching de la respuesta | `apps/accounts/views.py:86` |
| `@method_decorator` | Aplica decoradores a métodos de clase | `apps/accounts/views.py:85-86` |
| `@wraps` | Preserva metadatos de la función original | `apps/accounts/decorators.py:5` |

**Fragmento** (`apps/cart/views.py:31-33`):
```python
@require_POST
@csrf_protect
def add_to_cart(request, producto_id):
```

---

## 4. Singleton Pattern (a través del framework Django)

**Definición**: Patrón creacional que garantiza que una clase tenga una única instancia y proporciona un punto de acceso global a ella. Django implementa Singletons a nivel de configuración y conexiones.

**Ubicación en el proyecto**:

| Singleton | Descripción | Ubicación |
|-----------|-------------|-----------|
| `settings` | Objeto único de configuración global | `django.conf.settings` |
| Conexión BD | Una sola conexión a SQLite por request | `django.db.connection` |
| `Cart` (sesión) | Instancia única del carrito por sesión de usuario | `apps/cart/cart.py:18` |
| Cache | Único caché por proceso (si se configura) | `django.core.cache` |

**Fragmento** — Obtención del singleton de configuración en todo el proyecto:
```python
# apps/cart/cart.py:5
from django.conf import settings
CART_SESSION_ID = settings.CART_SESSION_ID
```

**Fragmento** — Carrito como singleton de sesión (`apps/cart/cart.py:18-21`):
```python
class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart
```

---

## 5. Strategy Pattern

**Definición**: Patrón de comportamiento que permite seleccionar un algoritmo en tiempo de ejecución. En lugar de implementar directamente un algoritmo, el código decide qué estrategia utilizar basándose en condiciones.

**Ubicación en el proyecto**:

### Estrategias de descuento — `apps/cart/models.py:42-52`

**Fragmento**:
```python
def aplicar_descuento(self, subtotal):
    if self.tipo == 'PORCENTAJE':
        return round(subtotal * (self.valor / 100), 2)
    elif self.tipo == 'MONTO_FIJO':
        return min(self.valor, subtotal)
    return 0
```

Se selecciona la estrategia de descuento según el tipo de cupón (`PORCENTAJE` vs `MONTO_FIJO`) en tiempo de ejecución.

### Estados del pedido — `apps/orders/models.py:16-20`

```python
ESTADO_CHOICES = [
    ('PENDIENTE', 'Pendiente'),
    ('CONFIRMADO', 'Confirmado'),
    ('ENVIADO', 'Enviado'),
    ('ENTREGADO', 'Entregado'),
    ('CANCELADO', 'Cancelado'),
]
```

Cada estado determina qué acciones son válidas (cancelar solo si PENDIENTE o CONFIRMADO, cambiar a ENVIADO solo si CONFIRMADO, etc.).

---

## 6. Chain of Responsibility (Middleware)

**Definición**: Patrón de comportamiento que permite pasar una solicitud a través de una cadena de manejadores. Cada manejador decide si procesa la solicitud o la pasa al siguiente.

**Ubicación en el proyecto**: Django implementa este patrón mediante su pila de middleware.

**Configuración** (`config/settings.py:32-41`):
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',           # Manejador 1
    'django.contrib.sessions.middleware.SessionMiddleware',    # Manejador 2
    'django.middleware.common.CommonMiddleware',               # Manejador 3
    'django.middleware.csrf.CsrfViewMiddleware',               # Manejador 4
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Manejador 5
    'django.contrib.messages.middleware.MessageMiddleware',    # Manejador 6
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Manejador 7
    'apps.accounts.middleware.NoCacheMiddleware',              # Manejador 8 (personalizado)
]
```

**Middleware personalizado** (`apps/accounts/middleware.py:5-14`):
```python
class NoCacheMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['Cache-Control'] = (
            'no-cache, no-store, must-revalidate, private'
        )
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
```

Cada middleware en la cadena procesa el request (y opcionalmente el response) en orden secuencial.

---

## 7. Command Pattern

**Definición**: Patrón de comportamiento que encapsula una solicitud como un objeto, permitiendo parametrizar clientes con diferentes solicitudes, hacer cola de operaciones, o soportar operaciones reversibles.

**Ubicación en el proyecto**: Comandos personalizados de Django (`manage.py`).

**Comando `seed_data`** — `apps/accounts/management/commands/seed_data.py`

**Fragmento**:
```python
class Command(BaseCommand):
    help = 'Puebla la base de datos con datos de prueba'

    def handle(self, *args, **options):
        # Crear usuarios
        admin = CustomUser.objects.create_superuser(...)
        cliente = CustomUser.objects.create_user(...)

        # Crear categorías
        categorias_data = [...]
        for cat in categorias_data:
            Categoria.objects.create(**cat)

        # Crear productos
        productos_data = [...]
        for prod in productos_data:
            Producto.objects.create(**prod)
```

Ejecución: `python manage.py seed_data`

---

## 8. Observer Pattern (Señales de Django)

**Definición**: Patrón de comportamiento donde un objeto (sujeto) mantiene una lista de dependientes (observadores) y les notifica automáticamente cualquier cambio de estado.

**Ubicación en el proyecto**: Django usa señales (`django.dispatch.Signal`) como implementación del patrón Observer. Aunque el proyecto no define señales personalizadas, las utiliza internamente:

- `post_save`: Notificaciones después de guardar un modelo (admin logs).
- `post_delete`: Notificaciones después de eliminar un modelo.
- `request_finished`: Cuando termina un request HTTP.

**Uso implícito**: Los `context_processors` actúan como observadores que se ejecutan en cada request:

`apps/products/context_processors.py:5-8`:
```python
def categorias_globales(request):
    return {
        'categorias': Categoria.objects.filter(activo=True)
    }
```

`apps/cart/context_processors.py:5-10`:
```python
def cart_items_count(request):
    if request.user.is_authenticated:
        cart = Cart(request)
        return {'cart_items_count': cart.total_items}
    return {'cart_items_count': 0}
```

---

## 9. Template Method (en Context Processors)

**Definición**: Variante del patrón donde un contexto processor se inyecta automáticamente en el pipeline de renderizado de Django. El framework proporciona el método `context_processors` y cada función implementa el comportamiento específico.

**Ubicación** (`config/settings.py:50-58`):
```python
'OPTIONS': {
    'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
        'apps.cart.context_processors.cart_items_count',
        'apps.products.context_processors.categorias_globales',
    ],
},
```

Cada context processor sigue la misma interfaz: `function(request) → dict`, pero implementa lógica diferente internamente.

---

## 10. Data Access Object (DAO) — ORM de Django

**Definición**: Patrón que abstrae y encapsula el acceso a la fuente de datos, proporcionando una interfaz uniforme para operaciones CRUD sin exponer los detalles de la base de datos.

**Ubicación en el proyecto**: Django ORM en todos los `views.py`, `models.py` y `admin.py`.

**Ejemplos**:

| Operación | Código | Ubicación |
|-----------|--------|-----------|
| Consultar todos | `Producto.objects.all()` | `apps/products/views.py:14` |
| Filtrar | `Pedido.objects.filter(usuario=request.user)` | `apps/orders/views.py:17` |
| Crear | `Pedido.objects.create(usuario=request.user, ...)` | `apps/orders/views.py:66` |
| Actualizar | `producto.stock -= cantidad; producto.save()` | `apps/orders/views.py:58` |
| Eliminar | `producto.delete()` | `apps/dashboard/views.py` (DeleteView) |
| Agregación | `Pedido.objects.filter(estado='ENTREGADO').aggregate(total=Sum('total'))` | `apps/dashboard/views.py:27` |

---

## Resumen de Patrones

| # | Patrón | Tipo | Ubicación Principal |
|---|--------|------|-------------------|
| 1 | **MTV / MVC** | Arquitectónico | Todo el proyecto |
| 2 | **Template Method (CBV)** | Comportamiento | `apps/*/views.py` (25+ vistas) |
| 3 | **Decorator** | Estructural | `apps/accounts/decorators.py`, vistas con `@require_POST`, `@csrf_protect`, `@never_cache` |
| 4 | **Singleton** | Creacional | `django.conf.settings`, `apps/cart/cart.py` (carrito por sesión) |
| 5 | **Strategy** | Comportamiento | `apps/cart/models.py:42` (tipos de descuento), `apps/orders/models.py:16` (estados) |
| 6 | **Chain of Responsibility** | Comportamiento | `config/settings.py:32` (middleware stack) |
| 7 | **Command** | Comportamiento | `apps/accounts/management/commands/seed_data.py` |
| 8 | **Observer** | Comportamiento | `apps/*/context_processors.py`, señales internas de Django |
| 9 | **Template Method (Context Processors)** | Comportamiento | `config/settings.py:50` (context_processors) |
| 10 | **DAO / ORM** | Estructural | `apps/*/views.py`, `apps/*/admin.py` (Django ORM) |



 el proyecto usa principalmente MTV (Django) y además estos patrones:

MTV (Model–Template–View)
Separación base del framework.
📍 models.py, views.py, templates/

Template Method (CBV)
Las vistas basadas en clases definen estructura y se personalizan métodos.
📍 apps/*/views.py (ListView, CreateView, etc.)

Decorator
Añade funcionalidades a vistas sin modificarlas.
📍 apps/accounts/decorators.py, apps/cart/views.py

Singleton
Instancia única en configuración y carrito por sesión.
📍 django.conf.settings, apps/cart/cart.py

Strategy
Cambia lógica según el caso (descuentos, estados).
📍 apps/cart/models.py, apps/orders/models.py

Chain of Responsibility
Peticiones pasan por middleware en cadena.
📍 config/settings.py (MIDDLEWARE)

Command
Comandos personalizados ejecutables.
📍 apps/accounts/management/commands/seed_data.py

Observer
Notificaciones automáticas (context processors / señales Django).
📍 apps/*/context_processors.py

DAO (ORM)
Acceso a datos mediante Django ORM.
📍 apps/*/models.py, views.py
