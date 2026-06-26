from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm, UserChangeForm, UserCreationForm
)

from .models import CustomUser


# Formulario de registro: crea un nuevo usuario con campos adicionales (teléfono, dirección)
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Correo electrónico')
    first_name = forms.CharField(
        required=True, max_length=30, label='Nombre'
    )
    last_name = forms.CharField(
        required=True, max_length=30, label='Apellido'
    )

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name',
            'telefono', 'direccion', 'password1', 'password2'
        )

    # Valida que el correo no esté ya registrado
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Este correo electrónico ya está registrado.'
            )
        return email


# Formulario de inicio de sesión: usuario + contraseña con estilos Bootstrap
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Nombre de usuario',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


# Formulario de administración de usuarios (para el panel de admin)
class UsuarioForm(UserChangeForm):
    password = None  # Oculta el campo de contraseña

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name',
            'telefono', 'direccion', 'is_active'
        )
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# Formulario de perfil: el usuario puede editar sus datos personales
class PerfilForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'telefono', 'direccion')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
