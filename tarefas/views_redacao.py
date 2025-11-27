from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Exists, OuterRef
from django.http import JsonResponse
from django.utils import timezone
from .models_redacao import RedacaoTema, RedacaoEntrega, RedacaoCorrecao, RedacaoAnaliseIA, RedacaoComentario
from .ia_enem import CorretorEnemIA

def is_professor(user):
    return user.is_superuser

@login_required
def lista_redacoes(request):
    """Lista redações para professor ou aluno"""
    if request.user.is_superuser:
        # Professor vê todos os temas que criou
        temas = RedacaoTema.objects.filter(professor=request.user).order_by('-data_publicacao')
        # Contar pendentes de correção
        pendentes_count = RedacaoEntrega.objects.filter(
            tema__professor=request.user,
            status__in=['pendente', 'ia_analisada']
        ).count()
        return render(request, 'redacao/lista_professor.html', {
            'temas': temas,
            'pendentes_count': pendentes_count
        })
    else:
        # Aluno vê temas disponíveis e suas entregas
        
        # Subquery para verificar se o aluno atual já entregou a redação para um tema
        entregas_aluno = RedacaoEntrega.objects.filter(
            tema=OuterRef('pk'),
            aluno=request.user
        )
        
        # Anotar cada tema com a informação se foi entregue ou não
        temas_disponiveis = RedacaoTema.objects.filter(ativo=True).annotate(
            usuario_entregou=Exists(entregas_aluno)
        ).order_by('-data_publicacao')

        minhas_entregas = RedacaoEntrega.objects.filter(aluno=request.user).select_related('tema', 'correcao')
        
        return render(request, 'redacao/lista_aluno.html', {
            'temas_disponiveis': temas_disponiveis,
            'minhas_entregas': minhas_entregas
        })

@login_required
@user_passes_test(is_professor)
def criar_tema_redacao(request):
    """Professor cria novo tema de redação"""
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        enunciado = request.POST.get('enunciado')
        textos_apoio = request.POST.get('textos_apoio', '')
        data_expiracao = request.POST.get('data_expiracao')
        palavras_min = int(request.POST.get('palavras_min', 200))
        palavras_max = int(request.POST.get('palavras_max', 500))
        arquivo_tema = request.FILES.get('arquivo_tema')
        
        tema = RedacaoTema.objects.create(
            professor=request.user,
            titulo=titulo,
            enunciado=enunciado,
            textos_apoio=textos_apoio,
            data_expiracao=data_expiracao,
            palavras_min=palavras_min,
            palavras_max=palavras_max,
            arquivo_tema=arquivo_tema
        )
        
        messages.success(request, f'Tema "{titulo}" criado com sucesso!')
        return redirect('tarefas:lista_redacoes')
    
    return render(request, 'redacao/criar_tema.html')

@login_required
@user_passes_test(is_professor)
def gerar_tema_ia(request):
    """Gera tema usando IA"""
    if request.method == 'POST':
        area = request.POST.get('area', 'geral')
        
        ia = CorretorEnemIA()
        tema_gerado = ia.gerar_tema_redacao(area)
        
        return JsonResponse({'tema': tema_gerado})
    
    return JsonResponse({'erro': 'Método não permitido'})

@login_required
def escrever_redacao(request, tema_id):
    """Aluno escreve redação"""
    tema = get_object_or_404(RedacaoTema, id=tema_id, ativo=True)
    
    # Professores não podem escrever redações
    if request.user.is_superuser:
        messages.error(request, 'Professores não podem escrever redações!')
        return redirect('tarefas:detalhe_tema', tema_id=tema.id)
    
    # Verifica se já entregou
    entrega_existente = RedacaoEntrega.objects.filter(tema=tema, aluno=request.user).first()
    
    if request.method == 'POST':
        if entrega_existente:
            messages.error(request, 'Você já entregou esta redação!')
            return redirect('tarefas:lista_redacoes')
        
        if tema.is_expired():
            messages.error(request, 'Prazo expirado para esta redação!')
            return redirect('tarefas:lista_redacoes')
        
        texto = request.POST.get('texto', '').strip()
        
        if not texto:
            messages.error(request, 'Texto da redação é obrigatório!')
            return render(request, 'redacao/escrever.html', {'tema': tema})
        
        # Verificar limite de palavras
        palavras = len(texto.split())
        if palavras < tema.palavras_min:
            messages.error(request, f'Redação deve ter pelo menos {tema.palavras_min} palavras. Sua redação tem {palavras} palavras.')
            return render(request, 'redacao/escrever.html', {'tema': tema, 'texto': texto})
        
        if palavras > tema.palavras_max:
            messages.error(request, f'Redação deve ter no máximo {tema.palavras_max} palavras. Sua redação tem {palavras} palavras.')
            return render(request, 'redacao/escrever.html', {'tema': tema, 'texto': texto})
        
        # Criar entrega
        entrega = RedacaoEntrega.objects.create(
            tema=tema,
            aluno=request.user,
            texto=texto,
            status='pendente'
        )
        
        # Analisar com IA automaticamente
        try:
            ia = CorretorEnemIA()
            analise = ia.corrigir_redacao_completa(texto, tema.titulo)
            
            RedacaoAnaliseIA.objects.create(
                entrega=entrega,
                nota_ia_c1=analise['c1']['nota'],
                nota_ia_c2=analise['c2']['nota'],
                nota_ia_c3=analise['c3']['nota'],
                nota_ia_c4=analise['c4']['nota'],
                nota_ia_c5=analise['c5']['nota'],
                sugestao_c1=analise['c1']['sugestao'],
                sugestao_c2=analise['c2']['sugestao'],
                sugestao_c3=analise['c3']['sugestao'],
                sugestao_c4=analise['c4']['sugestao'],
                sugestao_c5=analise['c5']['sugestao'],
                analise_geral=analise['analise_geral']
            )
            
            entrega.status = 'ia_analisada'
            entrega.save()
            
            messages.success(request, 'Redação entregue e analisada pela IA! Aguarde a correção do professor.')
        except:
            messages.success(request, 'Redação entregue! Aguarde a correção.')
        
        return redirect('tarefas:lista_redacoes')
    
    return render(request, 'redacao/escrever.html', {
        'tema': tema,
        'entrega_existente': entrega_existente
    })

@login_required
@user_passes_test(is_professor)
def corrigir_redacao(request, entrega_id):
    """Professor corrige redação"""
    entrega = get_object_or_404(RedacaoEntrega, id=entrega_id, tema__professor=request.user)
    
    # Buscar análise da IA se existir
    analise_ia = getattr(entrega, 'analise_ia', None)
    
    if request.method == 'POST':
        # Criar ou atualizar correção
        correcao, created = RedacaoCorrecao.objects.get_or_create(
            entrega=entrega,
            defaults={
                'professor': request.user,
                'competencia_1': 0,
                'competencia_2': 0,
                'competencia_3': 0,
                'competencia_4': 0,
                'competencia_5': 0
            }
        )
        
        # Atualizar notas das competências
        correcao.competencia_1 = int(request.POST.get('c1', 0))
        correcao.competencia_2 = int(request.POST.get('c2', 0))
        correcao.competencia_3 = int(request.POST.get('c3', 0))
        correcao.competencia_4 = int(request.POST.get('c4', 0))
        correcao.competencia_5 = int(request.POST.get('c5', 0))
        
        # Atualizar comentários
        correcao.comentario_c1 = request.POST.get('comentario_c1', '')
        correcao.comentario_c2 = request.POST.get('comentario_c2', '')
        correcao.comentario_c3 = request.POST.get('comentario_c3', '')
        correcao.comentario_c4 = request.POST.get('comentario_c4', '')
        correcao.comentario_c5 = request.POST.get('comentario_c5', '')
        correcao.comentario_geral = request.POST.get('comentario_geral', '')
        
        correcao.save()
        
        # Atualizar status da entrega
        entrega.status = 'corrigida'
        entrega.save()
        
        messages.success(request, f'Redação de {entrega.aluno.username} corrigida! Nota: {correcao.nota_total}/1000')
        return redirect('tarefas:lista_redacoes')
    
    return render(request, 'redacao/corrigir.html', {
        'entrega': entrega,
        'analise_ia': analise_ia
    })

@login_required
@user_passes_test(is_professor)
def correcoes_pendentes(request):
    """Lista todas as redações pendentes de correção do professor"""
    entregas_pendentes = RedacaoEntrega.objects.filter(
        tema__professor=request.user,
        status__in=['pendente', 'ia_analisada']
    ).select_related('tema', 'aluno').order_by('data_entrega')
    
    return render(request, 'redacao/correcoes_pendentes.html', {
        'entregas_pendentes': entregas_pendentes
    })

@login_required
def ver_feedback_redacao(request, entrega_id):
    """Aluno vê feedback da sua redação"""
    if request.user.is_superuser:
        # Professor pode ver qualquer entrega dos seus temas
        entrega = get_object_or_404(RedacaoEntrega, id=entrega_id, tema__professor=request.user)
    else:
        # Aluno só pode ver suas próprias entregas
        entrega = get_object_or_404(RedacaoEntrega, id=entrega_id, aluno=request.user)
    
    comentarios = entrega.comentarios.filter(resposta_para=None).order_by('data_comentario')
    
    if request.method == 'POST':
        texto_comentario = request.POST.get('comentario', '').strip()
        if texto_comentario:
            RedacaoComentario.objects.create(
                entrega=entrega,
                autor=request.user,
                texto=texto_comentario
            )
            messages.success(request, 'Comentário adicionado!')
            return redirect('tarefas:ver_feedback_redacao', entrega_id=entrega_id)
    
    return render(request, 'redacao/feedback.html', {
        'entrega': entrega,
        'comentarios': comentarios
    })

@login_required
def contar_palavras_ajax(request):
    """Conta palavras em tempo real via AJAX"""
    if request.method == 'POST':
        texto = request.POST.get('texto', '')
        palavras = len(texto.split()) if texto.strip() else 0
        
        return JsonResponse({'palavras': palavras})
    
    return JsonResponse({'erro': 'Método não permitido'})