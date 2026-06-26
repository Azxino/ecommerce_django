from django.urls import path

from . import views

app_name = 'accounts'

# URLs de la aplicación de cuentas (registro, login, logout, perfil)
urlpatterns = [
    path('registro/', views.RegistroView.as_view(), name='register'),  # Crear cuenta nueva
    path('login/', views.LoginView.as_view(), name='login'),           # Iniciar sesión
    path('logout/', views.LogoutView.as_view(), name='logout'),        # Cerrar sesión
    path('perfil/', views.PerfilView.as_view(), name='profile'),       # Editar perfil
]
