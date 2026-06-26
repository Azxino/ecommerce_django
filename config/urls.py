# Patrón MVC (Model-View-Controller): urlpatterns actúa como el controlador
# frontal (Front Controller) que recibe todas las peticiones HTTP y las
# despacha al controlador específico (vista) según la URL.
# Patrón Chain of Responsibility: cada petición atraviesa los patrones de URL
# en orden hasta encontrar el primero que coincide; si no hay coincidencia,
# Django devuelve 404.
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='products:list', permanent=False)),
    path('cuenta/', include('apps.accounts.urls')),
    path('productos/', include('apps.products.urls')),
    path('carrito/', include('apps.cart.urls')),
    path('pedidos/', include('apps.orders.urls')),
    path('panel/', include('apps.dashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
