from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models_redacao import RedacaoEntrega, RedacaoCorrecao

def is_professor(user):
    return user.is_superuser

@login_required
@user_passes_test(is_professor)
def corrigir_rapido(request, entrega_id):
    """Correção rápida de redação"""
    entrega = get_object_or_404(RedacaoEntrega, id=entrega_id, tema__professor=request.user)
    
    # Buscar análise da IA
    try:
        analise_ia = entrega.analise_ia
    except:
        analise_ia = None
    
    if request.method == 'POST':
        # Criar ou atualizar correção
        correcao, created = RedacaoCorrecao.objects.get_or_create(
            entrega=entrega,
            defaults={'professor': request.user}
        )
        
        # Atualizar notas
        correcao.competencia_1 = int(request.POST.get('c1', 120))
        correcao.competencia_2 = int(request.POST.get('c2', 120))
        correcao.competencia_3 = int(request.POST.get('c3', 120))
        correcao.competencia_4 = int(request.POST.get('c4', 120))
        correcao.competencia_5 = int(request.POST.get('c5', 120))
        correcao.comentario_geral = request.POST.get('comentario', '')
        
        correcao.save()
        entrega.status = 'corrigida'
        entrega.save()
        
        messages.success(request, f'Redação corrigida! Nota: {correcao.nota_total}/1000')
        return redirect('tarefas:correcoes_pendentes')
    
    return render(request, 'redacao/corrigir_rapido.html', {
        'entrega': entrega,
        'analise_ia': analise_ia
    })