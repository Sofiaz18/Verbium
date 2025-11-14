from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from .ia_questoes import GeradorQuestoes
from .ia_openrouter import OpenRouterIA

def is_professor(user):
    return user.is_superuser

@login_required
@user_passes_test(is_professor)
def gerador_questoes(request):
    """View para o gerador de questões com IA"""
    
    if request.method == 'POST':
        materia = request.POST.get('materia', 'geral')
        quantidade = int(request.POST.get('quantidade', 5))
        tipo_questao = request.POST.get('tipo_questao', 'dissertativa')
        usar_ia_real = request.POST.get('usar_ia_real', 'false') == 'true'
        
        if usar_ia_real:
            # Usar IA real do OpenRouter
            ia_client = OpenRouterIA()
            questoes = ia_client.gerar_questoes_ia(materia, quantidade)
            criterios = ia_client.gerar_criterios_avaliacao(tipo_questao)
        else:
            # Usar gerador local
            gerador = GeradorQuestoes()
            questoes = gerador.gerar_questoes(materia, quantidade)
            criterios = gerador.sugerir_criterios_avaliacao(tipo_questao)
        
        return JsonResponse({
            'questoes': questoes,
            'criterios': criterios,
            'materia': materia,
            'quantidade': quantidade,
            'ia_real': usar_ia_real
        })
    
    materias = ['matematica', 'portugues', 'historia', 'ciencias', 'geografia', 'geral']
    
    return render(request, 'tarefas/gerador_questoes.html', {
        'materias': materias
    })