from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import DesignacaoAluno

@login_required
def trocar_professor(request):
    """Permite aluno trocar de professor"""
    
    # Só alunos podem trocar
    if request.user.is_superuser:
        messages.error(request, 'Professores não podem trocar de professor!')
        return redirect('tarefas:dashboard')
    
    # Buscar designação atual
    try:
        designacao_atual = DesignacaoAluno.objects.get(aluno=request.user, ativa=True)
        professor_atual = designacao_atual.professor
    except DesignacaoAluno.DoesNotExist:
        professor_atual = None
        designacao_atual = None
    
    # Buscar todos os professores disponíveis com contagem de alunos
    professores_disponiveis = User.objects.filter(is_superuser=True)
    
    # Adicionar contagem de alunos para cada professor
    for professor in professores_disponiveis:
        professor.total_alunos = DesignacaoAluno.objects.filter(professor=professor, ativa=True).count()
    
    if request.method == 'POST':
        novo_professor_id = request.POST.get('novo_professor')
        
        if not novo_professor_id:
            messages.error(request, 'Selecione um professor!')
            return render(request, 'tarefas/trocar_professor.html', {
                'professor_atual': professor_atual,
                'professores_disponiveis': professores_disponiveis
            })
        
        novo_professor = get_object_or_404(User, id=novo_professor_id, is_superuser=True)
        
        # Se já tem professor, desativar designação atual
        if designacao_atual:
            designacao_atual.ativa = False
            designacao_atual.save()
        
        # Criar nova designação
        DesignacaoAluno.objects.create(
            professor=novo_professor,
            aluno=request.user,
            ativa=True
        )
        
        messages.success(request, f'Você foi conectado ao Prof. {novo_professor.first_name or novo_professor.username}!')
        return redirect('tarefas:dashboard')
    
    return render(request, 'tarefas/trocar_professor.html', {
        'professor_atual': professor_atual,
        'professores_disponiveis': professores_disponiveis
    })

@login_required
def meus_alunos(request):
    """Professor vê seus alunos e pode gerenciar"""
    
    if not request.user.is_superuser:
        messages.error(request, 'Apenas professores podem acessar esta página!')
        return redirect('tarefas:dashboard')
    
    # Buscar alunos do professor
    designacoes = DesignacaoAluno.objects.filter(professor=request.user, ativa=True).select_related('aluno')
    
    # Buscar alunos sem professor
    alunos_com_professor = DesignacaoAluno.objects.filter(ativa=True).values_list('aluno_id', flat=True)
    alunos_sem_professor = User.objects.filter(is_superuser=False).exclude(id__in=alunos_com_professor)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'adicionar_aluno':
            aluno_id = request.POST.get('aluno_id')
            aluno = get_object_or_404(User, id=aluno_id, is_superuser=False)
            
            # Verificar se aluno já tem professor
            if DesignacaoAluno.objects.filter(aluno=aluno, ativa=True).exists():
                messages.error(request, f'{aluno.username} já tem um professor!')
            else:
                DesignacaoAluno.objects.create(professor=request.user, aluno=aluno)
                messages.success(request, f'{aluno.username} foi adicionado à sua turma!')
        
        elif action == 'remover_aluno':
            designacao_id = request.POST.get('designacao_id')
            designacao = get_object_or_404(DesignacaoAluno, id=designacao_id, professor=request.user)
            designacao.ativa = False
            designacao.save()
            messages.success(request, f'{designacao.aluno.username} foi removido da sua turma!')
        
        return redirect('tarefas:meus_alunos')
    
    return render(request, 'tarefas/meus_alunos.html', {
        'designacoes': designacoes,
        'alunos_sem_professor': alunos_sem_professor
    })