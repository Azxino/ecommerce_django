from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.PedidoListView.as_view(), name='list'),
    path('crear/', views.create_order, name='create'),
    path('<int:pk>/', views.PedidoDetailView.as_view(), name='detail'),
    path(
        '<int:pk>/cancelar/',
        views.cancel_order,
        name='cancel'
    ),
]
