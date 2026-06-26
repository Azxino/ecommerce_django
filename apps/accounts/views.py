from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView, FormView, TemplateView, UpdateView

from .forms import LoginForm, PerfilForm, RegistroForm
from .models import CustomUser


# Patrón Template Method (CBV): CreateView define el esqueleto del algoritmo
# (get, post, form_valid, etc.) y esta clase sobrescribe métodos específicos
# para personalizar el comportamiento (auto-login, mensajes, redirecciones).
# Vista de registro: crea un nuevo usuario, lo autentica automáticamente y redirige al listado de productos
class RegistroView(CreateView):
    model = CustomUser
    form_class = RegistroForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('products:list')

    # Si el formulario es válido, guarda el usuario, lo loguea y muestra mensaje de bienvenida
    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        messages.success(
            self.request,
            f'¡Bienvenido {user.first_name or user.username}! '
            'Tu cuenta ha sido creada exitosamente.'
        )
        return response

    # Si el formulario es inválido, muestra los errores
    def form_invalid(self, form):
        messages.error(
            self.request,
            'Corrige los errores en el formulario.'
        )
        return super().form_invalid(form)

    # Si el usuario ya está autenticado, redirige a productos (no debe ver el registro)
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('products:list')
        return super().get(request, *args, **kwargs)


# Patrón Template Method (CBV): FormView con personalización de form_valid
# para login con soporte ?next= y mensajes flash.
# Vista de inicio de sesión: valida credenciales e inicia sesión
class LoginView(FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('products:list')

    # Si las credenciales son correctas, inicia sesión y redirige (soporta ?next=)
    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        messages.success(
            self.request,
            f'Bienvenido de nuevo, {user.first_name or user.username}.'
        )
        next_url = self.request.GET.get('next')
        if next_url:
            return redirect(next_url)
        return super().form_valid(form)

    # Si las credenciales son incorrectas, muestra error
    def form_invalid(self, form):
        messages.error(
            self.request,
            'Usuario o contraseña incorrectos.'
        )
        return super().form_invalid(form)

    # Si el usuario ya está autenticado, redirige a productos
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('products:list')
        return super().get(request, *args, **kwargs)


# Patrón Template Method (CBV) + Patrón Decorator: @csrf_protect y @never_cache
# decoran el método post para agregar seguridad sin modificar la lógica interna.
# Vista de cierre de sesión: solo acepta POST (seguridad), evita que el navegador cachee la página
class LogoutView(TemplateView):
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, 'Has cerrado sesión correctamente.')
        return redirect('products:list')

    # Si alguien accede por GET, redirige al inicio (no cierra sesión automáticamente)
    def get(self, request, *args, **kwargs):
        return redirect('products:list')


# Patrón Template Method (CBV): UpdateView + LoginRequiredMixin (compuesto)
# Patrón Strategy: LoginRequiredMixin es una estrategia de autenticación que
# se compone con la vista para restringir acceso según el estado del usuario.
# Vista de perfil: solo usuarios autenticados pueden editar su perfil
class PerfilView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = PerfilForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')

    # Obtiene el usuario actual como objeto a editar
    def get_object(self, queryset=None):
        return self.request.user

    # Si el formulario es válido, actualiza el perfil y muestra mensaje de éxito
    def form_valid(self, form):
        messages.success(self.request, 'Perfil actualizado correctamente.')
        return super().form_valid(form)

    # Si el formulario es inválido, muestra los errores
    def form_invalid(self, form):
        messages.error(
            self.request, 'Corrige los errores en el formulario.'
        )
        return super().form_invalid(form)
