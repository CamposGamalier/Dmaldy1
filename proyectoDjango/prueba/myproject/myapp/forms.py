from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Producto, Profile

class CustomRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='Usuario', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=63, widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Contraseña')

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['id','nombre', 'descripcion', 'precio', 'imagen', 'categoria', 'stock']
        labels ={
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'precio': 'Precio',
            'imagen': 'Imagen',
            'categoria': 'Categoría',
            'stock': 'Stock'
        }
        widgets = {
            'id': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Ingrese ID',
                    'id': 'id'
                }
            ),
            'nombre': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Ingrese nombre',
                    'id': 'nombre'
                }
            ),
            'descripcion': forms.Textarea(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Ingrese descripción',
                    'id': 'descripcion',
                    'rows': 3
                }
            ),
            'precio': forms.NumberInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Ingrese precio',
                    'id': 'precio',
                    'step': '0.01'
                }
            ),
            'imagen': forms.FileInput(
                attrs = {
                    'class': 'form-control',
                    'id': 'imagen'
                }
            ),
            'categoria': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Ingrese categoría',
                    'id': 'categoria'
                }
            ),
            'stock': forms.NumberInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Ingrese stock',
                    'id': 'stock'
                }
            )
        }

class UpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']