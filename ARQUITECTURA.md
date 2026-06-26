# D'gala — Arquitectura y Modelado UML (PlantUML)

Este archivo contiene diagramas PlantUML que modelan la arquitectura del sistema.  
Puedes renderizarlos en: https://www.plantuml.com/plantuml/uml/ o usando la extensión PlantUML en VS Code.

---

## 1. Diagrama de Clases (Modelo de Datos)

```plantuml
@startuml Dgala_ModeloDeDatos
!theme plain
skinparam classAttributeIconSize 0
skinparam backgroundColor #FEFEFE
skinparam linetype ortho

' ============================================================================
' ENUMERACIONES
' ============================================================================
enum Rol {
    ADMIN
    CLIENTE
}

enum TipoCupon {
    PORCENTAJE
    MONTO_FIJO
}

enum EstadoPedido {
    PENDIENTE
    CONFIRMADO
    ENVIADO
    ENTREGADO
    CANCELADO
}

' ============================================================================
' CLASES (MODELOS)
' ============================================================================
class CustomUser {
    - id: BigAutoField
    - password: CharField(128)
    - last_login: DateTimeField
    - is_superuser: BooleanField
    - username: CharField(150) {unique}
    - first_name: CharField(150)
    - last_name: CharField(150)
    - email: EmailField(254)
    - is_staff: BooleanField
    - is_active: BooleanField
    - date_joined: DateTimeField
    - role: CharField(10) {enum: Rol}
    - telefono: CharField(15)
    - direccion: TextField
    ..
    + is_admin(): bool
    + is_client(): bool
    ..
    {field} groups: ManyToManyField -> Group
    {field} user_permissions: ManyToManyField -> Permission
}

class Categoria {
    - id: BigAutoField
    - nombre: CharField(100) {unique}
    - slug: SlugField(120) {unique}
    - descripcion: TextField
    - activo: BooleanField
    - created_at: DateTimeField
}

class Producto {
    - id: BigAutoField
    - nombre: CharField(200)
    - slug: SlugField(220) {unique}
    - descripcion: TextField
    - precio: DecimalField(10,2)
    - stock: PositiveIntegerField
    - imagen: ImageField
    - disponible: BooleanField
    - destacado: BooleanField
    - created_at: DateTimeField
    - updated_at: DateTimeField
    ..
    + tiene_stock(): bool
    + stock_bajo(): bool
}

class Cupon {
    - id: BigAutoField
    - codigo: CharField(20) {unique}
    - descripcion: CharField(255)
    - tipo: CharField(15) {enum: TipoCupon}
    - valor: DecimalField(10,2)
    - monto_minimo: DecimalField(10,2)
    - max_usos: PositiveIntegerField
    - usos_actuales: PositiveIntegerField
    - activo: BooleanField
    - fecha_expiracion: DateTimeField
    - created_at: DateTimeField
    ..
    + es_valido(): bool
    + aplicar_descuento(subtotal): Decimal
    + incrementar_uso(): void
}

class Pedido {
    - id: BigAutoField
    - estado: CharField(15) {enum: EstadoPedido}
    - subtotal: DecimalField(10,2)
    - descuento: DecimalField(10,2)
    - total: DecimalField(10,2)
    - cupon_codigo: CharField(20)
    - notas: TextField
    - created_at: DateTimeField
    - updated_at: DateTimeField
}

class DetallePedido {
    - id: BigAutoField
    - precio: DecimalField(10,2)
    - cantidad: PositiveIntegerField
    - subtotal: DecimalField(10,2)
}

' ============================================================================
' RELACIONES
' ============================================================================
CustomUser "1" --o{ "0..*" Pedido : usuario
Categoria "1" --o{ "0..*" Producto : categoria
Producto "1" --o{ "0..*" DetallePedido : producto
Pedido "1" --o{ "0..*" DetallePedido : detalles
Pedido "*" o-- "0..1" Cupon : <<aplica>>

note top of CustomUser : Modelo de usuario personalizado\ncon roles ADMIN/CLIENTE
note top of Pedido : Estados:\nPENDIENTE → CONFIRMADO\n→ ENVIADO → ENTREGADO\n(CANCELADO desde PEND o CONF)

@enduml
```

---

## 2. Diagrama de Componentes (Arquitectura del Sistema)

```plantuml
@startuml Dgala_Arquitectura
!theme plain
skinparam backgroundColor #FEFEFE
skinparam componentStyle rectangle

' ============================================================================
' CAPA DE PRESENTACION
' ============================================================================
package "Capa de Presentación" as Presentacion {
    [base.html] as BaseHTML
    [style.css] as CSS
    [script.js] as JS
    [Bootstrap 5] as BS5

    package "Plantillas Públicas" as PubTemplates {
        [product_list.html]
        [product_detail.html]
        [category_list.html]
        [cart_detail.html]
        [order_list.html]
        [order_detail.html]
    }

    package "Plantillas Admin" as AdminTemplates {
        [base_admin.html]
        [home.html]
        [user_list.html]
        [user_form.html]
        [product_list.html]
        [product_form.html]
        [category_list.html]
        [category_form.html]
        [order_list.html]
        [order_detail.html]
        [coupon_list.html]
        [coupon_form.html]
        [confirm_delete.html]
    }

    BaseHTML --> PubTemplates : extiende
    BaseHTML --> AdminTemplates : extiende
    PubTemplates --> CSS
    PubTemplates --> JS
    PubTemplates --> BS5
    AdminTemplates --> CSS
    AdminTemplates --> JS
    AdminTemplates --> BS5
}

' ============================================================================
' CAPA DE APLICACION (LOGICA DE NEGOCIO)
' ============================================================================
package "Capa de Aplicación (Apps Django)" as Aplicacion {
    [accounts] as Accounts
    [products] as Products
    [cart] as Cart
    [orders] as Orders
    [dashboard] as Dashboard

    package "Middleware" as MW {
        [NoCacheMiddleware]
        [SecurityMiddleware]
        [SessionMiddleware]
        [CsrfViewMiddleware]
        [AuthMiddleware]
        [MessageMiddleware]
        [XFrameOptionsMiddleware]
    }

    package "Context Processors" as CP {
        [categorias_globales]
        [cart_items_count]
    }
}

' ============================================================================
' CAPA DE RUTEO
' ============================================================================
package "Enrutamiento (urls.py)" as Routing {
    [config/urls.py] as RootURL
    [accounts/urls.py] as AccURL
    [products/urls.py] as ProdURL
    [cart/urls.py] as CartURL
    [orders/urls.py] as OrdURL
    [dashboard/urls.py] as DashURL
}

' ============================================================================
' CAPA DE DATOS
' ============================================================================
package "Capa de Datos" as Datos {
    database "SQLite\ndb.sqlite3" as DB
    file_system "media/\n(Imágenes)" as Media
    database "Sesiones\n(DB Backend)" as Sessions
}

' ============================================================================
' CONEXIONES ENTRE CAPAS
' ============================================================================
RootURL --> AccURL : /cuenta/
RootURL --> ProdURL : /productos/
RootURL --> CartURL : /carrito/
RootURL --> OrdURL : /pedidos/
RootURL --> DashURL : /panel/

AccURL --> Accounts
ProdURL --> Products
CartURL --> Cart
OrdURL --> Orders
DashURL --> Dashboard

Accounts --> MW : pasa por
Products --> MW
Cart --> MW
Orders --> MW
Dashboard --> MW

Accounts --> CP
Products --> CP
Cart --> CP
Orders --> CP
Dashboard --> CP

Accounts --> DB : CRUD CustomUser
Products --> DB : CRUD Categoria/Producto
Cart --> DB : Cupon
Cart --> Sessions : carrito en sesión
Orders --> DB : CRUD Pedido/DetallePedido
Dashboard --> DB : CRUD todo
Dashboard --> Products : estadísticas

Products --> Media : leer/escribir imágenes

' CLIENTE
actor Usuario as U
U --> RootURL : HTTP Request
RootURL --> U : HTTP Response (HTML)

@enduml
```

---

## 3. Diagrama de Casos de Uso

```plantuml
@startuml Dgala_CasosDeUso
!theme plain
skinparam backgroundColor #FEFEFE
left to right direction

' ============================================================================
' ACTORES
' ============================================================================
actor "Visitante" as V
actor "Cliente" as C
actor "Administrador" as A

' ============================================================================
' CASOS DE USO
' ============================================================================
rectangle "D'gala - Tienda de Ropa" as Sistema {

    ' === VISITANTE ===
    usecase "UC1: Registrarse" as UC1
    usecase "UC2: Iniciar Sesión" as UC2
    usecase "UC3: Ver Catálogo de Productos" as UC3
    usecase "UC4: Buscar Productos" as UC4
    usecase "UC5: Filtrar por Categoría" as UC5
    usecase "UC6: Ver Detalle de Producto" as UC6
    usecase "UC7: Agregar al Carrito" as UC7
    usecase "UC8: Ver Carrito de Compras" as UC8

    ' === CLIENTE ===
    usecase "UC9: Realizar Pedido" as UC9
    usecase "UC10: Ver Historial de Pedidos" as UC10
    usecase "UC11: Ver Detalle de Pedido" as UC11
    usecase "UC12: Cancelar Pedido" as UC12
    usecase "UC13: Editar Perfil" as UC13
    usecase "UC14: Aplicar Cupón de Descuento" as UC14
    usecase "UC15: Cerrar Sesión" as UC15

    ' === ADMINISTRADOR ===
    usecase "UC16: Ver Dashboard de Estadísticas" as UC16
    usecase "UC17: Gestionar Usuarios (CRUD)" as UC17
    usecase "UC18: Gestionar Productos (CRUD)" as UC18
    usecase "UC19: Gestionar Categorías (CRUD)" as UC19
    usecase "UC20: Gestionar Pedidos" as UC20
    usecase "UC21: Cambiar Estado de Pedido" as UC21
    usecase "UC22: Gestionar Cupones (CRUD)" as UC22
}

' ============================================================================
' RELACIONES
' ============================================================================
V --> UC1
V --> UC2
V --> UC3
V --> UC4
V --> UC5
V --> UC6
V --> UC7
V --> UC8

C --> UC9 : incluye
C --> UC10
C --> UC11
C --> UC12
C --> UC13
C --> UC14
C --> UC15

A --> UC16
A --> UC17
A --> UC18
A --> UC19
A --> UC20
A --> UC21
A --> UC22

' Herencia de actores
C --|> V : extiende
A --|> C : extiende

note right of UC9
  Incluye:
  - Verificar stock
  - Descontar inventario
  - Aplicar cupón
  - Crear pedido + detalles
  - Limpiar carrito
end note

note right of UC20
  Incluye:
  - Listar pedidos
  - Filtrar por estado
  - Ver detalle
  - Actualizar estado
end note

@enduml
```

---

## 4. Diagrama de Secuencia — Creación de Pedido

```plantuml
@startuml Dgala_CrearPedido
!theme plain
skinparam backgroundColor #FEFEFE
skinparam sequenceMessageAlign left

actor "Cliente" as Cliente
participant "Navegador" as Browser
participant "CSRF\nMiddleware" as CSRF
participant "create_order\nView" as View
participant "Cart\n(Sesión)" as Cart
participant "Cupon\nModel" as Cupon
participant "Pedido\nModel" as Pedido
participant "DetallePedido\nModel" as Det
participant "Producto\nModel" as Prod

Cliente -> Browser: Click "Realizar Pedido"
Browser -> CSRF: POST /pedidos/crear/\n(csrf_token)
CSRF -> View: Request validada

View -> Cart: Obtener items\n(CART_SESSION_ID)
Cart --> View: Lista de items\ncon producto_id, cantidad

View -> View: Verificar carrito no vacío

loop por cada item
    View -> Prod: get(id)
    Prod --> View: Producto
    View -> View: Verificar stock >= cantidad
    View -> Prod: stock -= cantidad
    View -> Prod: save()
end

View -> Cupon: get(codigo) [si aplica]
Cupon --> View: Objeto Cupon
View -> Cupon: aplicar_descuento(subtotal)
Cupon --> View: monto_descuento
View -> Cupon: incrementar_uso()

View -> Pedido: create(usuario, subtotal,\ndescuento, total, cupon...)
Pedido --> View: pedido_obj

loop por cada item
    View -> Det: create(pedido, producto,\nprecio, cantidad, subtotal)
end

View -> Cart: clear()
Cart -> Cart: session['cart'] = {}

View -> Browser: redirect('orders:detail', pk=pk)
Browser -> View: GET /pedidos/<pk>/
View --> Browser: HTML con detalle del pedido

Browser -> Cliente: Muestra confirmación

@enduml
```

---

## 5. Diagrama de Estados — Ciclo de Vida del Pedido

```plantuml
@startuml Dgala_EstadoPedido
!theme plain
skinparam backgroundColor #FEFEFE
skinparam monochrome true

state "PENDIENTE" as Pendiente
state "CONFIRMADO" as Confirmado
state "ENVIADO" as Enviado
state "ENTREGADO" as Entregado
state "CANCELADO" as Cancelado

[*] --> Pendiente : Cliente crea pedido
Pendiente --> Confirmado : Admin confirma
Pendiente --> Cancelado : Cliente cancela
Confirmado --> Enviado : Admin marca como enviado
Confirmado --> Cancelado : Cliente cancela
Enviado --> Entregado : Admin marca como entregado

note top of Pendiente
  Estado inicial.
  Stock ya descontado.
end note

note right of Cancelado
  Solo si el estado
  anterior era PENDIENTE
  o CONFIRMADO.
  Al cancelar se
  RESTAURA el stock.
end note

@enduml
```

---

## 6. Diagrama de Paquetes — Estructura Django

```plantuml
@startuml Dgala_Paquetes
!theme plain
skinparam backgroundColor #FEFEFE
skinparam packageStyle rectangle

package "ropa_shop" as ROOT {
    package "config" as Config {
        [settings.py] as Settings
        [urls.py] as URLs
        [wsgi.py] as WSGI
        [asgi.py] as ASGI
    }

    package "apps" as Apps {
        package "accounts" as Acc {
            [models.py] as AccModels
            [views.py] as AccViews
            [forms.py] as AccForms
            [urls.py] as AccUrls
            [middleware.py] as AccMW
            [decorators.py] as AccDec
            [admin.py] as AccAdmin
            [seed_data.py] as Seed
        }

        package "products" as Prod {
            [models.py] as ProdModels
            [views.py] as ProdViews
            [forms.py] as ProdForms
            [urls.py] as ProdUrls
            [admin.py] as ProdAdmin
            [context_processors.py] as ProdCP
        }

        package "cart" as Cart {
            [models.py] as CartModels
            [views.py] as CartViews
            [forms.py] as CartForms
            [urls.py] as CartUrls
            [cart.py] as CartLogic
            [admin.py] as CartAdmin
            [context_processors.py] as CartCP
        }

        package "orders" as Ord {
            [models.py] as OrdModels
            [views.py] as OrdViews
            [forms.py] as OrdForms
            [urls.py] as OrdUrls
            [admin.py] as OrdAdmin
        }

        package "dashboard" as Dash {
            [views.py] as DashViews
            [urls.py] as DashUrls
        }
    }

    package "templates" as Templates {
        [base.html]
        package "products/" as TProd
        package "cart/" as TCart
        package "orders/" as TOrd
        package "dashboard/" as TDash
    }

    package "static" as Static {
        package "css/" as CSS
        package "js/" as JS
        package "bootstrap/" as BS
    }
}

' Dependencias entre módulos
AccViews ..> AccModels : usa
AccViews ..> AccForms : usa
AccUrls ..> AccViews : enruta

ProdViews ..> ProdModels
ProdViews ..> ProdForms
ProdUrls ..> ProdViews
ProdCP ..> ProdModels

CartViews ..> CartLogic
CartViews ..> CartModels
CartViews ..> CartForms
CartUrls ..> CartViews
CartCP ..> CartLogic

OrdViews ..> OrdModels
OrdViews ..> OrdForms
OrdUrls ..> OrdViews

DashViews ..> AccModels
DashViews ..> ProdModels
DashViews ..> OrdModels
DashViews ..> CartModels
DashUrls ..> DashViews

' Context processors inyectados en templates
ProdCP ..> Templates : categorias_globales
CartCP ..> Templates : cart_items_count

' URLs raíz enrutan a sub-urls
URLs ..> AccUrls : /cuenta/
URLs ..> ProdUrls : /productos/
URLs ..> CartUrls : /carrito/
URLs ..> OrdUrls : /pedidos/
URLs ..> DashUrls : /panel/

' Templates heredan
Templates <.. TProd : extiende
Templates <.. TCart
Templates <.. TOrd
Templates <.. TDash

' Static usado por templates
Templates ..> CSS
Templates ..> JS
Templates ..> BS

@enduml
```

---

## Instrucciones de Uso

1. Copia cualquier bloque `@startuml ... @enduml` en un archivo `.puml`.
2. Abre el archivo en:
   - **VS Code**: Extensión "PlantUML" (jebbs.plantuml).
   - **Web**: https://www.plantuml.com/plantuml/uml/
   - **CLI**: `plantuml archivo.puml` (requiere Java y PlantUML).
3. Los diagramas se renderizarán como imágenes SVG/PNG.

### Diagramas incluidos

| Diagrama | Archivo PlantUML | Descripción |
|----------|-----------------|-------------|
| Clases | `diagrama_clases.puml` | Modelo de datos completo con 6 entidades, relaciones, tipos y métodos |
| Componentes | `diagrama_componentes.puml` | Arquitectura por capas (presentación, aplicación, ruteo, datos) |
| Casos de Uso | `diagrama_casos_uso.puml` | 22 casos de uso distribuidos en 3 roles (visitante, cliente, admin) |
| Secuencia | `diagrama_secuencia_pedido.puml` | Flujo completo de creación de pedido con 7 participantes |
| Estados | `diagrama_estados_pedido.puml` | Ciclo de vida del pedido con 5 estados y transiciones |
| Paquetes | `diagrama_paquetes.puml` | Estructura de módulos Python y dependencias entre componentes |
