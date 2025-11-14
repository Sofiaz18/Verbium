from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def ajuda(request):
    """Sistema de ajuda personalizado por perfil"""
    
    # Determinar o perfil do usuário
    if request.user.is_superuser:
        perfil = 'professor'
    else:
        perfil = 'aluno'
    
    # Conteúdo de ajuda específico para cada perfil
    ajuda_content = {
        'professor': {
            'titulo': '👨🏫 Guia do Professor',
            'secoes': [
                {
                    'titulo': '🚀 Primeiros Passos',
                    'items': [
                        'Acesse o Dashboard para ver o resumo da sua turma',
                        'Gerencie seus alunos em "👥 Meus Alunos"',
                        'Crie temas de redação ENEM com IA',
                        'Corrija redações com sugestões da IA'
                    ]
                },
                {
                    'titulo': '📝 Sistema de Redações',
                    'items': [
                        'Crie temas realistas com ajuda da IA',
                        'Anexe arquivos PDF como material de apoio',
                        'A IA analisa automaticamente todas as entregas',
                        'Use as sugestões da IA para agilizar a correção',
                        'Corrija nas 5 competências ENEM (0-200 pontos cada)',
                        'Adicione comentários específicos por competência'
                    ]
                },
                {
                    'titulo': '🤖 Recursos de IA',
                    'items': [
                        'Gerador de Temas: Cria temas ENEM por área',
                        'Gerador de Questões: Cria questões personalizadas',
                        'Correção Automática: Analisa redações instantaneamente',
                        'Sugestões Inteligentes: Ajuda na correção final'
                    ]
                },
                {
                    'titulo': '👥 Gerenciar Alunos',
                    'items': [
                        'Veja todos os alunos conectados à sua turma',
                        'Adicione alunos que não têm professor',
                        'Remova alunos da sua turma se necessário',
                        'Acompanhe estatísticas de cada aluno'
                    ]
                },
                {
                    'titulo': '💬 Sistema de Comentários',
                    'items': [
                        'Alunos podem comentar nas correções',
                        'Responda dúvidas diretamente no sistema',
                        'Use para esclarecer critérios de avaliação',
                        'Mantenha comunicação clara e educativa'
                    ]
                }
            ]
        },
        'aluno': {
            'titulo': '👨🎓 Guia do Aluno',
            'secoes': [
                {
                    'titulo': '🚀 Primeiros Passos',
                    'items': [
                        'Acesse o Dashboard para ver suas redações',
                        'Verifique se está conectado a um professor',
                        'Troque de professor se necessário em "🔄 Trocar Professor"',
                        'Escreva redações ENEM e receba feedback da IA'
                    ]
                },
                {
                    'titulo': '📝 Escrevendo Redações',
                    'items': [
                        'Leia atentamente o tema e textos de apoio',
                        'Baixe o material PDF se disponível',
                        'Escreva diretamente no editor online',
                        'Acompanhe o contador de palavras em tempo real',
                        'Respeite os limites mínimo e máximo de palavras',
                        'Sua redação será analisada pela IA automaticamente'
                    ]
                },
                {
                    'titulo': '📊 Acompanhando seu Progresso',
                    'items': [
                        'Veja suas notas no Dashboard',
                        'Acesse o feedback detalhado de cada redação',
                        'Compare sua nota com a sugestão da IA',
                        'Leia os comentários do professor por competência',
                        'Use o feedback para melhorar nas próximas redações'
                    ]
                },
                {
                    'titulo': '🎯 Competências ENEM',
                    'items': [
                        'C1 - Norma Culta: Gramática, ortografia, concordância',
                        'C2 - Tema: Compreensão e desenvolvimento do tema',
                        'C3 - Argumentação: Seleção e organização de ideias',
                        'C4 - Coesão: Conectivos e encadeamento de ideias',
                        'C5 - Proposta: Intervenção detalhada e viável'
                    ]
                },
                {
                    'titulo': '💬 Tirando Dúvidas',
                    'items': [
                        'Comente nas suas correções para tirar dúvidas',
                        'Pergunte sobre critérios de avaliação',
                        'Peça esclarecimentos sobre competências específicas',
                        'Use para solicitar feedback adicional',
                        'Mantenha comunicação respeitosa com o professor'
                    ]
                },
                {
                    'titulo': '🔄 Trocando de Professor',
                    'items': [
                        'Acesse "🔄 Trocar Professor" no Dashboard',
                        'Veja a lista de professores disponíveis',
                        'Escolha o professor que preferir',
                        'A troca é instantânea e você verá as atividades do novo professor',
                        'Suas entregas anteriores são mantidas'
                    ]
                }
            ]
        }
    }
    
    return render(request, 'tarefas/ajuda.html', {
        'perfil': perfil,
        'ajuda': ajuda_content[perfil]
    })