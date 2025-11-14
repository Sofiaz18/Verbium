from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Avg
from .models_redacao import RedacaoTema, RedacaoEntrega, RedacaoCorrecao
from .models import DesignacaoAluno

@login_required
def dashboard(request):
    """Dashboard com estatísticas do sistema"""
    
    if request.user.is_superuser:
        # Estatísticas para Professor
        temas = RedacaoTema.objects.filter(professor=request.user)
        entregas = RedacaoEntrega.objects.filter(tema__professor=request.user)
        alunos_designados = DesignacaoAluno.objects.filter(professor=request.user, ativa=True)
        
        # Calcular média das notas
        correcoes_prof = RedacaoCorrecao.objects.filter(entrega__tema__professor=request.user)
        if correcoes_prof.exists():
            total_notas = sum(c.nota_total for c in correcoes_prof)
            media_notas = total_notas / correcoes_prof.count()
        else:
            media_notas = 0
        
        stats = {
            'total_temas': temas.count(),
            'total_entregas': entregas.count(),
            'pendentes_correcao': entregas.filter(status__in=['pendente', 'ia_analisada']).count(),
            'total_alunos': alunos_designados.count(),
            'media_notas': media_notas,
        }
    else:
        # Estatísticas para Aluno
        temas_disponiveis = RedacaoTema.objects.filter(ativo=True)
        minhas_entregas = RedacaoEntrega.objects.filter(aluno=request.user)
        correcoes = RedacaoCorrecao.objects.filter(entrega__aluno=request.user)
        
        # Calcular média das notas do aluno
        if correcoes.exists():
            total_notas = sum(c.nota_total for c in correcoes)
            media_notas = total_notas / correcoes.count()
        else:
            media_notas = 0
        
        stats = {
            'temas_disponiveis': temas_disponiveis.count(),
            'redacoes_entregues': minhas_entregas.count(),
            'redacoes_pendentes': temas_disponiveis.count() - minhas_entregas.count(),
            'media_notas': media_notas,
        }
    
    return render(request, 'tarefas/dashboard.html', {'stats': stats})