from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductoListView.as_view(), name='list'),
    path(
        '<slug:slug>/',
        views.ProductoDetailView.as_view(),
        name='detail'
    ),
    path(
        'categoria/<slug:slug>/',
        views.CategoriaListView.as_view(),
        name='category'
    ),
]
