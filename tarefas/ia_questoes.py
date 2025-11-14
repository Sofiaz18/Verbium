import random

class GeradorQuestoes:
    """Gerador de questões usando IA simulada para ajudar professores"""
    
    def __init__(self):
        self.templates_questoes = {
            'matematica': [
                "Resolva a equação: {eq}",
                "Calcule o valor de: {calc}",
                "Determine a derivada de: f(x) = {funcao}",
                "Encontre as raízes da equação: {eq_quadratica}",
                "Calcule a integral de: ∫{integral} dx"
            ],
            'portugues': [
                "Analise a figura de linguagem presente no texto: '{texto}'",
                "Identifique o sujeito e predicado na frase: '{frase}'",
                "Explique o uso da vírgula na seguinte frase: '{frase_virgula}'",
                "Classifique morfologicamente as palavras: {palavras}",
                "Reescreva o texto corrigindo os erros: '{texto_erro}'"
            ],
            'historia': [
                "Explique as causas da {evento_historico}",
                "Compare os governos de {personagem1} e {personagem2}",
                "Analise as consequências da {evento} para o Brasil",
                "Descreva o contexto histórico da {epoca}",
                "Relacione os fatores que levaram à {revolucao}"
            ],
            'ciencias': [
                "Explique o processo de {processo_biologico}",
                "Descreva a função do {orgao} no corpo humano",
                "Compare as características de {animal1} e {animal2}",
                "Explique como ocorre a {reacao_quimica}",
                "Analise os fatores que influenciam {fenomeno_natural}"
            ],
            'geografia': [
                "Analise as características climáticas da região {regiao}",
                "Explique a formação do relevo {tipo_relevo}",
                "Compare os aspectos econômicos de {pais1} e {pais2}",
                "Descreva os problemas ambientais da {area_geografica}",
                "Analise a distribuição populacional do {continente}"
            ]
        }
        
        self.dados_exemplo = {
            'eq': ['2x + 5 = 15', 'x² - 4x + 3 = 0', '3x - 7 = 2x + 1'],
            'calc': ['√144 + 2³', '(15 × 4) ÷ 3', '2⁴ - 3²'],
            'funcao': ['x² + 3x - 2', 'sen(x) + cos(x)', 'ln(x) + e^x'],
            'eq_quadratica': ['x² - 5x + 6 = 0', '2x² + 3x - 1 = 0', 'x² - 9 = 0'],
            'integral': ['x² + 2x', 'sen(x)', 'e^x + 1'],
            'texto': ['O vento sussurrava segredos', 'Suas palavras eram punhais', 'O tempo voou'],
            'frase': ['O menino brincava no parque', 'Maria comprou flores', 'Os alunos estudaram muito'],
            'frase_virgula': ['João, venha aqui', 'Estudei muito, mas não passei', 'Em casa, todos dormiam'],
            'palavras': ['casa, bonita, correr', 'livro, interessante, ler', 'escola, grande, estudar'],
            'texto_erro': ['Eu foi na escola ontem', 'Os menino brinca no parque', 'Ela tem muitos amigo'],
            'evento_historico': ['Revolução Francesa', 'Segunda Guerra Mundial', 'Independência do Brasil'],
            'personagem1': ['Dom Pedro I', 'Getúlio Vargas', 'Juscelino Kubitschek'],
            'personagem2': ['Dom Pedro II', 'Fernando Henrique', 'Lula'],
            'evento': ['Proclamação da República', 'Abolição da Escravatura', 'Era Vargas'],
            'epoca': ['Brasil Colonial', 'Império Brasileiro', 'República Velha'],
            'revolucao': ['Revolução de 1930', 'Revolução Constitucionalista', 'Revolução Farroupilha'],
            'processo_biologico': ['fotossíntese', 'respiração celular', 'digestão'],
            'orgao': ['coração', 'fígado', 'pulmões'],
            'animal1': ['mamíferos', 'aves', 'peixes'],
            'animal2': ['répteis', 'anfíbios', 'insetos'],
            'reacao_quimica': ['combustão', 'oxidação', 'fermentação'],
            'fenomeno_natural': ['chuva ácida', 'efeito estufa', 'erosão'],
            'regiao': ['Amazônia', 'Nordeste', 'Sul'],
            'tipo_relevo': ['montanhoso', 'planáltico', 'planície'],
            'pais1': ['Brasil', 'Argentina', 'Chile'],
            'pais2': ['Uruguai', 'Paraguai', 'Bolívia'],
            'area_geografica': ['Mata Atlântica', 'Cerrado', 'Caatinga'],
            'continente': ['América do Sul', 'Europa', 'África']
        }
    
    def gerar_questoes(self, materia, quantidade=5):
        """Gera questões para uma matéria específica"""
        if materia.lower() not in self.templates_questoes:
            return self.gerar_questoes_genericas(quantidade)
        
        templates = self.templates_questoes[materia.lower()]
        questoes = []
        
        for _ in range(quantidade):
            template = random.choice(templates)
            questao = self._preencher_template(template)
            questoes.append(questao)
        
        return questoes
    
    def gerar_questoes_genericas(self, quantidade=5):
        """Gera questões genéricas quando a matéria não é reconhecida"""
        questoes_genericas = [
            "Explique o conceito principal do tema estudado.",
            "Compare e contraste dois aspectos importantes do assunto.",
            "Analise criticamente o tópico apresentado em aula.",
            "Descreva a importância prática do conteúdo estudado.",
            "Relacione o tema com situações do cotidiano.",
            "Apresente argumentos a favor e contra o tema discutido.",
            "Elabore um resumo dos pontos principais do conteúdo.",
            "Proponha soluções para os problemas identificados no tema.",
            "Avalie os impactos do assunto na sociedade atual.",
            "Demonstre a aplicação prática dos conhecimentos adquiridos."
        ]
        
        return random.sample(questoes_genericas, min(quantidade, len(questoes_genericas)))
    
    def _preencher_template(self, template):
        """Preenche um template com dados aleatórios"""
        import re
        
        # Encontra todas as variáveis no template {variavel}
        variaveis = re.findall(r'\{(\w+)\}', template)
        
        questao = template
        for var in variaveis:
            if var in self.dados_exemplo:
                valor = random.choice(self.dados_exemplo[var])
                questao = questao.replace(f'{{{var}}}', valor)
        
        return questao
    
    def sugerir_criterios_avaliacao(self, tipo_questao="dissertativa"):
        """Sugere critérios de avaliação para as questões"""
        criterios = {
            'dissertativa': [
                "Clareza e organização das ideias (0-2 pontos)",
                "Conhecimento do conteúdo (0-3 pontos)",
                "Argumentação e exemplos (0-2 pontos)",
                "Uso correto da linguagem (0-2 pontos)",
                "Criatividade e originalidade (0-1 ponto)"
            ],
            'objetiva': [
                "Resposta correta (0-10 pontos)",
                "Justificativa da escolha (0-5 pontos bonus)"
            ],
            'pratica': [
                "Execução correta dos procedimentos (0-4 pontos)",
                "Resultado final (0-3 pontos)",
                "Organização e limpeza (0-2 pontos)",
                "Criatividade na solução (0-1 ponto)"
            ]
        }
        
        return criterios.get(tipo_questao, criterios['dissertativa'])