from django import forms

from .models import Categoria, Producto


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ('nombre', 'descripcion', 'activo')
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
            'activo': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = (
            'categoria', 'nombre', 'descripcion', 'precio',
            'stock', 'imagen', 'disponible', 'destacado'
        )
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4}
            ),
            'precio': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.01'}
            ),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
            'disponible': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'destacado': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio <= 0:
            raise forms.ValidationError('El precio debe ser mayor a cero.')
        return precio
