from django import forms

from .models import Pedido


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ('notas',)
        widgets = {
            'notas': forms.Textarea(
                attrs={
                    'class': 'form-control', 'rows': 3,
                    'placeholder': 'Notas adicionales para tu pedido...'
                }
            ),
        }


class CambiarEstadoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ('estado',)
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }
