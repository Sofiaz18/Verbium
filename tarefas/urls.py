from django.urls import path
from . import views
from .views_home import home
from .views_dashboard import dashboard
from .views_auth import logout_view
from .views_avaliacao import aprovar_entrega, rejeitar_entrega
from .views_cadastro import cadastro_aluno, cadastro_professor
from .views_ia import gerador_questoes
from .views_redacao import (lista_redacoes, criar_tema_redacao, gerar_tema_ia, 
                           escrever_redacao, corrigir_redacao, ver_feedback_redacao, contar_palavras_ajax, correcoes_pendentes)
from .views_correcao import corrigir_rapido
from .views_redacao_extra import responder_comentario, detalhe_tema
from .views_entregas import entregas_tema
from .views_trocar_professor import trocar_professor, meus_alunos
from .views_ajuda import ajuda

# Define o namespace do app para uso em templates (ex: {% url 'tarefas:lista_tarefas' %})
app_name = 'tarefas' 
urlpatterns = [
    # Página inicial
    path('', home, name='home'),
    
    # Dashboard
    path('dashboard/', dashboard, name='dashboard'),
    
    # Logout personalizado
    path('logout/', logout_view, name='logout'),
    
    # Ex: /tarefas/ - Página principal (Lista de Tarefas)
    path('tarefas/', views.lista_tarefas, name='lista_tarefas'), 
    
    # Ex: /tarefas/nova/ - Criar Nova Tarefa (Apenas Professor)
    path('tarefas/nova/', views.criar_tarefa, name='criar_tarefa'),
    
    # Ex: /tarefas/1/entrega/ - Detalhe da Tarefa e Submissão/Revisão
    path('tarefas/<int:tarefa_id>/entrega/', views.detalhe_tarefa_entrega, name='detalhe_tarefa_entrega'),
    
    # Avaliação de entregas
    path('entrega/<int:entrega_id>/aprovar/', aprovar_entrega, name='aprovar_entrega'),
    path('entrega/<int:entrega_id>/rejeitar/', rejeitar_entrega, name='rejeitar_entrega'),
    
    # Cadastros
    path('cadastro/aluno/', cadastro_aluno, name='cadastro_aluno'),
    path('cadastro/professor/', cadastro_professor, name='cadastro_professor'),
    
    # IA - Gerador de Questões
    path('ia/questoes/', gerador_questoes, name='gerador_questoes'),
    
    # Sistema de Redações ENEM
    path('redacoes/', lista_redacoes, name='lista_redacoes'),
    path('redacoes/criar/', criar_tema_redacao, name='criar_tema_redacao'),
    path('redacoes/gerar-tema/', gerar_tema_ia, name='gerar_tema_ia'),
    path('redacoes/<int:tema_id>/escrever/', escrever_redacao, name='escrever_redacao'),
    path('redacoes/corrigir/<int:entrega_id>/', corrigir_redacao, name='corrigir_redacao'),
    path('redacoes/corrigir-rapido/<int:entrega_id>/', corrigir_rapido, name='corrigir_rapido'),
    path('redacoes/correcoes-pendentes/', correcoes_pendentes, name='correcoes_pendentes'),
    path('redacoes/feedback/<int:entrega_id>/', ver_feedback_redacao, name='ver_feedback_redacao'),
    path('redacoes/tema/<int:tema_id>/', detalhe_tema, name='detalhe_tema'),
    path('redacoes/tema/<int:tema_id>/entregas/', entregas_tema, name='entregas_tema'),
    path('redacoes/comentario/<int:comentario_id>/responder/', responder_comentario, name='responder_comentario'),
    path('ajax/contar-palavras/', contar_palavras_ajax, name='contar_palavras_ajax'),
    
    # Gerenciamento de Professor-Aluno
    path('trocar-professor/', trocar_professor, name='trocar_professor'),
    path('meus-alunos/', meus_alunos, name='meus_alunos'),
    
    # Sistema de Ajuda
    path('ajuda/', ajuda, name='ajuda'),
]