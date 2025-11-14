from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CadastroAlunoForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, label='Nome')
    last_name = forms.CharField(max_length=30, label='Sobrenome')
    email = forms.EmailField(label='Email')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        labels = {
            'username': 'Nome de usuário',
        }

class CadastroProfessorForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, label='Nome')
    last_name = forms.CharField(max_length=30, label='Sobrenome')
    email = forms.EmailField(label='Email')
    codigo_professor = forms.CharField(max_length=20, label='Código do Professor', help_text='Código fornecido pela instituição')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'codigo_professor')
        labels = {
            'username': 'Nome de usuário',
        }