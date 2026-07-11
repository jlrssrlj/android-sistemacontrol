from django import forms
from django.contrib.auth.models import User
from dashboard.models import Empresa, Rol
from django import forms
from .models import Proveedor

class UsuarioEmpleadoForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    empresa = forms.ModelChoiceField(
        queryset=Empresa.objects.filter(activa=True),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    rol = forms.ModelChoiceField(
        queryset=Rol.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def clean(self):
        cleaned_data = super().clean()
        empresa = cleaned_data.get('empresa')
        rol = cleaned_data.get('rol')
        if empresa and rol and rol.empresa_id != empresa.id:
            raise forms.ValidationError('El rol seleccionado no pertenece a la empresa.')
        return cleaned_data


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'nit', 'direccion', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'nit': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }
