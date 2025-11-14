from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models_redacao import RedacaoTema, RedacaoEntrega, RedacaoComentario

@login_required
def responder_comentario(request, comentario_id):
    """Responder a um comentário específico"""
    comentario_pai = get_object_or_404(RedacaoComentario, id=comentario_id)
    
    if request.method == 'POST':
        texto = request.POST.get('resposta', '').strip()
        if texto:
            RedacaoComentario.objects.create(
                entrega=comentario_pai.entrega,
                autor=request.user,
                texto=texto,
                resposta_para=comentario_pai
            )
            messages.success(request, 'Resposta adicionada!')
        
        return redirect('tarefas:ver_feedback_redacao', entrega_id=comentario_pai.entrega.id)
    
    return JsonResponse({'erro': 'Método não permitido'})

@login_required
def detalhe_tema(request, tema_id):
    """Ver detalhes do tema e opção de escrever redação"""
    tema = get_object_or_404(RedacaoTema, id=tema_id, ativo=True)
    entrega_existente = None
    
    if not request.user.is_superuser:
        entrega_existente = RedacaoEntrega.objects.filter(tema=tema, aluno=request.user).first()
    
    return render(request, 'redacao/detalhe_tema.html', {
        'tema': tema,
        'entrega_existente': entrega_existente
    })