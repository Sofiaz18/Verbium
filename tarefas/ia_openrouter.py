import requests
import json
from django.conf import settings

class OpenRouterIA:
    """Cliente para API OpenRouter para gerar questões reais com IA"""
    
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def gerar_questoes_ia(self, materia, quantidade=5, nivel="medio"):
        """Gera questões usando IA real"""
        
        prompt = f"""
        Você é um professor especialista em {materia}. Crie {quantidade} questões de nível {nivel} para uma avaliação.

        Requisitos:
        - Questões claras e objetivas
        - Adequadas para estudantes do ensino médio
        - Variadas (dissertativas, objetivas, práticas)
        - Com diferentes níveis de dificuldade

        Formato de resposta:
        1. [Questão 1]
        2. [Questão 2]
        ...

        Matéria: {materia}
        Quantidade: {quantidade}
        Nível: {nivel}
        """
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json={
                    "model": "meta-llama/llama-3.1-8b-instruct:free",
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "max_tokens": 1000,
                    "temperature": 0.7
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                content = data['choices'][0]['message']['content']
                return self._processar_resposta(content)
            else:
                return self._questoes_fallback(materia, quantidade)
                
        except Exception as e:
            print(f"Erro na API: {e}")
            return self._questoes_fallback(materia, quantidade)
    
    def gerar_criterios_avaliacao(self, tipo_questao="dissertativa"):
        """Gera critérios de avaliação usando IA"""
        
        prompt = f"""
        Crie critérios de avaliação detalhados para questões do tipo: {tipo_questao}

        Inclua:
        - Pontuação específica para cada critério
        - Total de 10 pontos
        - Critérios claros e objetivos

        Formato:
        - Critério 1 (X pontos)
        - Critério 2 (X pontos)
        ...
        """
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json={
                    "model": "meta-llama/llama-3.1-8b-instruct:free",
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "max_tokens": 500,
                    "temperature": 0.5
                },
                timeout=20
            )
            
            if response.status_code == 200:
                data = response.json()
                content = data['choices'][0]['message']['content']
                return content.split('\n')
            else:
                return self._criterios_fallback(tipo_questao)
                
        except Exception as e:
            return self._criterios_fallback(tipo_questao)
    
    def _processar_resposta(self, content):
        """Processa a resposta da IA e extrai as questões"""
        linhas = content.split('\n')
        questoes = []
        
        for linha in linhas:
            linha = linha.strip()
            if linha and (linha.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.')) or 
                         linha.startswith(('•', '-', '*'))):
                # Remove numeração e limpa a questão
                questao = linha.split('.', 1)[-1].strip()
                if questao:
                    questoes.append(questao)
        
        return questoes if questoes else self._questoes_fallback("geral", 5)
    
    def _questoes_fallback(self, materia, quantidade):
        """Questões de backup caso a API falhe"""
        questoes_backup = {
            'matematica': [
                "Resolva a equação quadrática: x² - 5x + 6 = 0",
                "Calcule a derivada da função f(x) = 3x² + 2x - 1",
                "Determine a área de um triângulo com base 8cm e altura 6cm",
                "Encontre o valor de x na equação: 2x + 7 = 15",
                "Calcule a média aritmética dos números: 12, 18, 24, 30"
            ],
            'portugues': [
                "Identifique a figura de linguagem na frase: 'Seus olhos eram duas estrelas brilhantes'",
                "Analise a função sintática do termo destacado: 'O menino *estudioso* passou na prova'",
                "Explique a diferença entre 'mas' e 'mais' com exemplos",
                "Classifique o sujeito da oração: 'Chegaram os convidados da festa'",
                "Reescreva o texto corrigindo os erros de concordância"
            ]
        }
        
        return questoes_backup.get(materia.lower(), [
            "Explique o conceito principal do tema estudado",
            "Compare dois aspectos importantes do assunto",
            "Analise criticamente o tópico apresentado",
            "Descreva a importância prática do conteúdo",
            "Relacione o tema com situações cotidianas"
        ])[:quantidade]
    
    def _criterios_fallback(self, tipo_questao):
        """Critérios de backup"""
        criterios = {
            'dissertativa': [
                "- Conhecimento do conteúdo (4 pontos)",
                "- Organização das ideias (2 pontos)", 
                "- Argumentação (2 pontos)",
                "- Linguagem adequada (2 pontos)"
            ],
            'objetiva': [
                "- Resposta correta (8 pontos)",
                "- Justificativa (2 pontos)"
            ],
            'pratica': [
                "- Execução correta (5 pontos)",
                "- Resultado final (3 pontos)",
                "- Organização (2 pontos)"
            ]
        }
        
        return criterios.get(tipo_questao, criterios['dissertativa'])