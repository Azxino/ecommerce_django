from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardHomeView.as_view(), name='home'),

    path('usuarios/', views.DashboardUsuariosView.as_view(), name='user_list'),
    path('usuarios/crear/', views.DashboardUsuarioCreateView.as_view(), name='user_create'),
    path('usuarios/<int:pk>/editar/', views.DashboardUsuarioUpdateView.as_view(), name='user_update'),
    path('usuarios/<int:pk>/eliminar/', views.DashboardUsuarioDeleteView.as_view(), name='user_delete'),

    path('productos/', views.DashboardProductosView.as_view(), name='product_list'),
    path('productos/crear/', views.DashboardProductoCreateView.as_view(), name='product_create'),
    path('productos/<int:pk>/editar/', views.DashboardProductoUpdateView.as_view(), name='product_update'),
    path('productos/<int:pk>/eliminar/', views.DashboardProductoDeleteView.as_view(), name='product_delete'),

    path('categorias/', views.DashboardCategoriasView.as_view(), name='category_list'),
    path('categorias/crear/', views.DashboardCategoriaCreateView.as_view(), name='category_create'),
    path('categorias/<int:pk>/editar/', views.DashboardCategoriaUpdateView.as_view(), name='category_update'),
    path('categorias/<int:pk>/eliminar/', views.DashboardCategoriaDeleteView.as_view(), name='category_delete'),

    path('pedidos/', views.DashboardPedidosView.as_view(), name='order_list'),
    path('pedidos/<int:pk>/', views.DashboardPedidoDetailView.as_view(), name='order_detail'),
    path('pedidos/<int:pk>/estado/', views.DashboardPedidoUpdateView.as_view(), name='order_update'),

    path('cupones/', views.DashboardCuponesView.as_view(), name='coupon_list'),
    path('cupones/crear/', views.DashboardCuponCreateView.as_view(), name='coupon_create'),
    path('cupones/<int:pk>/editar/', views.DashboardCuponUpdateView.as_view(), name='coupon_update'),
    path('cupones/<int:pk>/eliminar/', views.DashboardCuponDeleteView.as_view(), name='coupon_delete'),
]
