# -*- coding: utf-8 -*-
from django import forms
from .models import Tarefa, Entrega
from django.forms.widgets import DateTimeInput

# ====================================================================
# FORMULÁRIO TAREFA (Usado pelo Professor para Criar/Editar)
# ====================================================================
class TarefaForm(forms.ModelForm):
    # Sobrescreve o campo de data_expiracao para usar um widget de data/hora mais amigável
    data_expiracao = forms.DateTimeField(
        widget=DateTimeInput(attrs={'type': 'datetime-local'}),
        label='Data e Hora de Expiração'
    )
    
    class Meta:
        model = Tarefa
        # O professor (request.user) será atribuído na View, então não está aqui
        # 'data_publicacao' e 'ativa' terão valores padrão ou serão controlados no Admin
        fields = ['titulo', 'descricao', 'data_expiracao']
        labels = {
            'titulo': 'Título da Atividade',
            'descricao': 'Descrição Detalhada',
        }
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
        }

# ====================================================================
# FORMULÁRIO ENTREGA (Usado pelo Aluno para Submeter Arquivos)
# ====================================================================
class EntregaForm(forms.ModelForm):
    class Meta:
        model = Entrega
        # O aluno e a tarefa serão atribuídos na View
        fields = ['arquivo']
        labels = {
            'arquivo': 'Selecione o Arquivo para Envio (.pdf, .zip, etc.)',
        }
