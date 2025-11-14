# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.http import Http404, HttpResponseForbidden
from django.db import models
# CORREÇÃO: Importar ValidationError para uso no bloco try/except da view
from django.core.exceptions import ValidationError 

# Importa os modelos criados
from .models import Tarefa, Entrega
# Importa os formulários a serem criados 
from .forms import TarefaForm, EntregaForm 


# Função para testar se o usuário é um Professor (Superuser)
def is_professor(user):
    return user.is_superuser

# ====================================================================
# VIEW: LISTA DE TAREFAS (Principal)
# ====================================================================
@login_required
def lista_tarefas(request):
    """
    Exibe a lista de tarefas.
    - Professor: lista todas as tarefas e o número de entregas.
    - Aluno: lista todas as tarefas, marcando o status de entrega.
    """
    
    # Busca tarefas baseado no tipo de usuário
    if request.user.is_superuser:
        # Professor vê todas as suas tarefas
        tarefas_query = Tarefa.objects.filter(professor=request.user, ativa=True).order_by('data_expiracao')
    else:
        # Aluno vê apenas tarefas do seu professor ou tarefas específicas para ele
        from .models import DesignacaoAluno
        designacao = DesignacaoAluno.objects.filter(aluno=request.user, ativa=True).first()
        if designacao:
            # Tarefas do professor designado + tarefas específicas para este aluno
            tarefas_query = Tarefa.objects.filter(
                models.Q(professor=designacao.professor, ativa=True, alunos_especificos__isnull=True) |
                models.Q(alunos_especificos=request.user, ativa=True)
            ).distinct().order_by('data_expiracao')
        else:
            # Se não tem designação, vê todas as tarefas (comportamento antigo)
            tarefas_query = Tarefa.objects.filter(ativa=True).order_by('data_expiracao')
    
    lista_de_tarefas = []
    
    for tarefa in tarefas_query:
        dados_tarefa = {
            'id': tarefa.id,
            'titulo': tarefa.titulo,
            'descricao': tarefa.descricao,
            'data_expiracao': tarefa.data_expiracao,
            'is_expired': tarefa.is_expired(),
        }
        
        if not request.user.is_superuser:
            # Lógica para Aluno
            entrega = Entrega.objects.filter(tarefa=tarefa, aluno=request.user).first()
            dados_tarefa['entregue'] = entrega is not None
            dados_tarefa['data_entrega_aluno'] = entrega.data_entrega if entrega else None
            dados_tarefa['nota'] = entrega.nota if entrega else None
            dados_tarefa['status'] = entrega.status if entrega else None
            dados_tarefa['num_entregas'] = 0 # Não relevante para o aluno

        else:
            # Lógica para Professor (Superuser)
            num_entregas = tarefa.entregas.count()
            dados_tarefa['entregue'] = False # Professor não entrega
            dados_tarefa['num_entregas'] = num_entregas # Professor vê a contagem

        lista_de_tarefas.append(dados_tarefa)

    context = {
        'tarefas': lista_de_tarefas,
        'now': timezone.now(),
    }
    
    return render(request, 'tarefas/lista_tarefas.html', context)

# ====================================================================
# VIEW: CRIAÇÃO DE TAREFAS (Apenas Professor)
# ====================================================================
@login_required
@user_passes_test(is_professor)
def criar_tarefa(request):
    """Permite ao Professor criar uma nova tarefa."""
    
    if request.method == 'POST':
        # Instancia o formulário com os dados POST
        form = TarefaForm(request.POST)
        if form.is_valid():
            # Não salva no banco ainda (commit=False)
            nova_tarefa = form.save(commit=False)
            # Atribui o professor logado
            nova_tarefa.professor = request.user
            nova_tarefa.save()
            messages.success(request, f'Tarefa "{nova_tarefa.titulo}" criada com sucesso!')
            return redirect('tarefas:lista_tarefas')
        else:
            # Se o formulário for inválido, exibe os erros
            messages.error(request, 'Erro ao criar a tarefa. Verifique os dados fornecidos.')
    else:
        # Cria um formulário vazio para o método GET
        form = TarefaForm()

    context = {
        'form': form,
        'titulo_pagina': 'Criar Nova Tarefa',
    }
    
    # Usaremos o mesmo template de detalhe para reuso
    return render(request, 'tarefas/criar_tarefa.html', context)

# ====================================================================
# VIEW: DETALHE DA TAREFA E ENTREGA
# ====================================================================
@login_required
def detalhe_tarefa_entrega(request, tarefa_id):
    """
    Lógica ramificada:
    - Se Aluno: Mostra detalhes da tarefa, status de entrega e formulário de envio.
    - Se Professor: Mostra detalhes da tarefa e lista todas as entregas dos alunos.
    """
    
    tarefa = get_object_or_404(Tarefa, pk=tarefa_id)
    
    if request.user.is_superuser:
        # --- Lógica para Professor ---
        entregas = Entrega.objects.filter(tarefa=tarefa).select_related('aluno').order_by('-data_entrega')
        
        context = {
            'tarefa': tarefa,
            'entregas': entregas,
            'titulo_pagina': f'Entregas para: {tarefa.titulo}',
        }
        return render(request, 'tarefas/detalhe_professor.html', context)
        
    else:
        # --- Lógica para Aluno ---
        
        # 1. Checa se já entregou
        entrega_existente = Entrega.objects.filter(tarefa=tarefa, aluno=request.user).first()
        
        # 2. Lógica de Submissão (POST)
        if request.method == 'POST':
            # Se já entregou, não permite nova submissão via POST, apenas atualização se necessário (que não vamos implementar agora)
            if entrega_existente:
                messages.error(request, 'Você já fez uma entrega para esta tarefa. Entre em contato com o professor se precisar alterar.')
                return redirect('tarefas:detalhe_tarefa_entrega', tarefa_id=tarefa.id)
            
            # Checa se expirou antes de processar o formulário
            if tarefa.is_expired():
                messages.error(request, 'O prazo para esta tarefa expirou.')
                return redirect('tarefas:detalhe_tarefa_entrega', tarefa_id=tarefa.id)

            # Processa a nova entrega
            form = EntregaForm(request.POST, request.FILES)
            if form.is_valid():
                nova_entrega = form.save(commit=False)
                nova_entrega.tarefa = tarefa
                nova_entrega.aluno = request.user
                
                try:
                    # O método save() do modelo Entrega possui a validação clean() que checa o prazo
                    nova_entrega.save()
                    messages.success(request, 'Sua entrega foi enviada com sucesso!')
                    return redirect('tarefas:detalhe_tarefa_entrega', tarefa_id=tarefa.id)
                except ValidationError as e:
                    messages.error(request, f'Erro de Validação: {str(e)}')
                    # Se falhar na validação, retorna para a mesma página
                    return redirect('tarefas:detalhe_tarefa_entrega', tarefa_id=tarefa.id)
            else:
                messages.error(request, 'Erro no envio do arquivo. Verifique se o arquivo foi selecionado.')
        
        # 3. Lógica de Exibição (GET)
        form = EntregaForm() # Cria o formulário vazio para exibição
        
        context = {
            'tarefa': tarefa,
            'entrega_existente': entrega_existente,
            'form': form,
            'now': timezone.now(),
            'pode_entregar': not tarefa.is_expired() and not entrega_existente,
        }
        return render(request, 'tarefas/detalhe_aluno.html', context)
