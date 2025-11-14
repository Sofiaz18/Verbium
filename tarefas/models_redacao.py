from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import os

class RedacaoTema(models.Model):
    """Tema de redação acadêmico"""
    
    professor = models.ForeignKey(User, on_delete=models.CASCADE, 
                                  limit_choices_to={'is_superuser': True},
                                  related_name='temas_redacao')
    
    titulo = models.CharField(max_length=200, verbose_name='Título do Tema')
    enunciado = models.TextField(verbose_name='Enunciado Completo')
    textos_apoio = models.TextField(blank=True, verbose_name='Textos de Apoio')
    arquivo_tema = models.FileField(upload_to='redacao_temas/', blank=True, null=True, verbose_name='Arquivo do Tema (PDF)')
    
    data_publicacao = models.DateTimeField(default=timezone.now)
    data_expiracao = models.DateTimeField(verbose_name='Prazo de Entrega')
    
    palavras_min = models.IntegerField(default=200, verbose_name='Mínimo de Palavras')
    palavras_max = models.IntegerField(default=500, verbose_name='Máximo de Palavras')
    
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Tema de Redação'
        verbose_name_plural = 'Temas de Redação'
        ordering = ['-data_publicacao']
    
    def __str__(self):
        return self.titulo
    
    def is_expired(self):
        return self.data_expiracao < timezone.now()

class RedacaoEntrega(models.Model):
    """Redação entregue pelo aluno"""
    
    tema = models.ForeignKey(RedacaoTema, on_delete=models.CASCADE, related_name='entregas')
    aluno = models.ForeignKey(User, on_delete=models.CASCADE, 
                              limit_choices_to={'is_superuser': False},
                              related_name='redacoes_entregues')
    
    texto = models.TextField(verbose_name='Texto da Redação')
    data_entrega = models.DateTimeField(default=timezone.now)
    
    # Status da correção
    STATUS_CHOICES = [
        ('pendente', 'Aguardando Correção'),
        ('ia_analisada', 'Analisada pela IA'),
        ('corrigida', 'Corrigida pelo Professor'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    
    # Contagem de palavras
    palavras_count = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Entrega de Redação'
        verbose_name_plural = 'Entregas de Redação'
        unique_together = ('tema', 'aluno')
        ordering = ['-data_entrega']
    
    def __str__(self):
        return f'{self.aluno.username} - {self.tema.titulo}'
    
    def save(self, *args, **kwargs):
        # Contar palavras automaticamente
        self.palavras_count = len(self.texto.split()) if self.texto else 0
        super().save(*args, **kwargs)

class RedacaoCorrecao(models.Model):
    """Correção da redação com as 5 competências"""
    
    entrega = models.OneToOneField(RedacaoEntrega, on_delete=models.CASCADE, related_name='correcao')
    
    # 5 Competências (0-200 pontos cada)
    competencia_1 = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(200)],
        verbose_name='C1 - Norma Culta',
        help_text='Domínio da modalidade escrita formal'
    )
    competencia_2 = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(200)],
        verbose_name='C2 - Tema/Tipologia',
        help_text='Compreender a proposta e aplicar conceitos'
    )
    competencia_3 = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(200)],
        verbose_name='C3 - Argumentação',
        help_text='Selecionar e organizar informações'
    )
    competencia_4 = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(200)],
        verbose_name='C4 - Coesão',
        help_text='Conhecimento dos mecanismos linguísticos'
    )
    competencia_5 = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(200)],
        verbose_name='C5 - Proposta',
        help_text='Elaborar proposta de intervenção'
    )
    
    # Comentários por competência
    comentario_c1 = models.TextField(blank=True, verbose_name='Comentário C1')
    comentario_c2 = models.TextField(blank=True, verbose_name='Comentário C2')
    comentario_c3 = models.TextField(blank=True, verbose_name='Comentário C3')
    comentario_c4 = models.TextField(blank=True, verbose_name='Comentário C4')
    comentario_c5 = models.TextField(blank=True, verbose_name='Comentário C5')
    
    # Comentário geral
    comentario_geral = models.TextField(blank=True, verbose_name='Comentário Geral')
    
    # Dados da correção
    corrigida_por_ia = models.BooleanField(default=False)
    data_correcao = models.DateTimeField(default=timezone.now)
    professor = models.ForeignKey(User, on_delete=models.CASCADE, 
                                  limit_choices_to={'is_superuser': True},
                                  related_name='correcoes_feitas')
    
    class Meta:
        verbose_name = 'Correção de Redação'
        verbose_name_plural = 'Correções de Redação'
    
    def __str__(self):
        return f'Correção - {self.entrega}'
    
    @property
    def nota_total(self):
        """Calcula nota total (0-1000)"""
        return (self.competencia_1 + self.competencia_2 + self.competencia_3 + 
                self.competencia_4 + self.competencia_5)
    
    @property
    def nivel_geral(self):
        """Calcula nível geral baseado na nota total"""
        nota = self.nota_total
        if nota >= 900: return 5
        elif nota >= 700: return 4
        elif nota >= 500: return 3
        elif nota >= 300: return 2
        elif nota >= 100: return 1
        else: return 0
    
    def get_nivel_competencia(self, competencia_valor):
        """Retorna nível (0-5) baseado na pontuação da competência"""
        if competencia_valor >= 180: return 5
        elif competencia_valor >= 140: return 4
        elif competencia_valor >= 100: return 3
        elif competencia_valor >= 60: return 2
        elif competencia_valor >= 20: return 1
        else: return 0

class RedacaoAnaliseIA(models.Model):
    """Análise automática da IA para a redação"""
    
    entrega = models.OneToOneField(RedacaoEntrega, on_delete=models.CASCADE, related_name='analise_ia')
    
    # Sugestões da IA por competência
    sugestao_c1 = models.TextField(blank=True)
    sugestao_c2 = models.TextField(blank=True)
    sugestao_c3 = models.TextField(blank=True)
    sugestao_c4 = models.TextField(blank=True)
    sugestao_c5 = models.TextField(blank=True)
    
    # Notas sugeridas pela IA
    nota_ia_c1 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(200)])
    nota_ia_c2 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(200)])
    nota_ia_c3 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(200)])
    nota_ia_c4 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(200)])
    nota_ia_c5 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(200)])
    
    # Análise geral da IA
    analise_geral = models.TextField(blank=True)
    
    data_analise = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Análise IA'
        verbose_name_plural = 'Análises IA'
    
    def __str__(self):
        return f'IA - {self.entrega}'
    
    @property
    def nota_total_ia(self):
        return (self.nota_ia_c1 + self.nota_ia_c2 + self.nota_ia_c3 + 
                self.nota_ia_c4 + self.nota_ia_c5)

class RedacaoComentario(models.Model):
    """Sistema de comentários entre professor e aluno"""
    
    entrega = models.ForeignKey(RedacaoEntrega, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField(verbose_name='Comentário')
    data_comentario = models.DateTimeField(default=timezone.now)
    
    # Para responder a um comentário específico
    resposta_para = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='respostas')
    
    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['data_comentario']
    
    def __str__(self):
        return f'{self.autor.username}: {self.texto[:50]}...'