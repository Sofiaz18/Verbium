from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Entrega

def is_professor(user):
    return user.is_superuser

@login_required
@user_passes_test(is_professor)
def aprovar_entrega(request, entrega_id):
    entrega = get_object_or_404(Entrega, id=entrega_id, tarefa__professor=request.user)
    entrega.status = 'aprovada'
    entrega.save()
    messages.success(request, f'Entrega de {entrega.aluno.username} APROVADA!')
    return redirect('tarefas:detalhe_tarefa_entrega', tarefa_id=entrega.tarefa.id)

@login_required
@user_passes_test(is_professor)
def rejeitar_entrega(request, entrega_id):
    entrega = get_object_or_404(Entrega, id=entrega_id, tarefa__professor=request.user)
    entrega.status = 'rejeitada'
    entrega.save()
    messages.error(request, f'Entrega de {entrega.aluno.username} REJEITADA!')
    return redirect('tarefas:detalhe_tarefa_entrega', tarefa_id=entrega.tarefa.id)