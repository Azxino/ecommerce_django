from django import forms


class AgregarAlCarritoForm(forms.Form):
    cantidad = forms.IntegerField(
        min_value=1, max_value=99,
        initial=1,
        widget=forms.NumberInput(
            attrs={'class': 'form-control', 'min': '1', 'value': '1'}
        )
    )
    update = forms.BooleanField(
        required=False, initial=False,
        widget=forms.HiddenInput
    )


class CuponForm(forms.Form):
    codigo = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa tu código'
            }
        )
    )
