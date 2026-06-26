from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


# Decorador: solo permite acceso a administradores autenticados
def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Si no está autenticado, redirige al login
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para acceder.')
            return redirect('accounts:login')
        # Si no es admin, redirige a la tienda
        if not request.user.is_admin:
            messages.error(
                request, 'No tienes permisos de administrador.'
            )
            return redirect('products:list')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


# Decorador: solo permite acceso a clientes autenticados
def client_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Si no está autenticado, redirige al login
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para acceder.')
            return redirect('accounts:login')
        # Si no es cliente, redirige al panel admin
        if not request.user.is_client:
            messages.error(
                request, 'Esta sección es solo para clientes.'
            )
            return redirect('dashboard:home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
