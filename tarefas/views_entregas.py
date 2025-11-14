from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models_redacao import RedacaoTema, RedacaoEntrega

def is_professor(user):
    return user.is_superuser

@login_required
@user_passes_test(is_professor)
def entregas_tema(request, tema_id):
    """Professor vê todas as entregas de um tema específico"""
    tema = get_object_or_404(RedacaoTema, id=tema_id, professor=request.user)
    entregas = RedacaoEntrega.objects.filter(tema=tema).select_related('aluno', 'correcao', 'analise_ia').order_by('-data_entrega')
    
    # Estatísticas
    entregas_corrigidas = entregas.filter(status='corrigida').count()
    entregas_pendentes = entregas.filter(status='pendente').count()
    entregas_ia = entregas.filter(status='ia_analisada').count()
    
    return render(request, 'redacao/entregas_tema.html', {
        'tema': tema,
        'entregas': entregas,
        'entregas_corrigidas': entregas_corrigidas,
        'entregas_pendentes': entregas_pendentes,
        'entregas_ia': entregas_ia,
    })