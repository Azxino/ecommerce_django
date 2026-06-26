from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartDetailView.as_view(), name='detail'),
    path('agregar/<int:producto_id>/', views.add_to_cart, name='add'),
    path('eliminar/<int:producto_id>/', views.remove_from_cart, name='remove'),
    path('actualizar/<int:producto_id>/', views.update_cart, name='update'),
    path('limpiar/', views.clear_cart, name='clear'),
    path('aplicar-cupon/', views.apply_cupon, name='apply_coupon'),
    path('eliminar-cupon/', views.remove_cupon, name='remove_coupon'),
]
