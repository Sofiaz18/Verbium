# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
import os

# Função auxiliar para garantir que o arquivo de entrega seja salvo corretamente
def user_directory_path(instance, filename):
    # O arquivo será carregado para MEDIA_ROOT/entregas/tarefa_<id>/aluno_<username>/<filename>
    return f'entregas/tarefa_{instance.tarefa.id}/aluno_{instance.aluno.username}/{filename}'

# ====================================================================
# MODELO TAREFA (Criado e gerenciado pelo Professor/Superuser)
# ====================================================================
class Tarefa(models.Model):
    """Representa uma tarefa ou atividade atribuída aos alunos designados."""
    
    # Campo para armazenar o professor que criou a tarefa
    professor = models.ForeignKey(User, on_delete=models.CASCADE, 
                                  limit_choices_to={'is_superuser': True},
                                  related_name='tarefas_criadas',
                                  verbose_name='Professor')
    
    # Alunos específicos para esta tarefa (opcional - se vazio, vai para todos os alunos do professor)
    alunos_especificos = models.ManyToManyField(User, 
                                                limit_choices_to={'is_superuser': False},
                                                related_name='tarefas_especificas',
                                                blank=True,
                                                verbose_name='Alunos Específicos')
    
    titulo = models.CharField(max_length=200, verbose_name='Título')
    descricao = models.TextField(verbose_name='Descrição')
    
    data_publicacao = models.DateTimeField(default=timezone.now, verbose_name='Publicado em')
    data_expiracao = models.DateTimeField(verbose_name='Data de Expiração')
    
    # Indica se a tarefa está ativa para aceitar novas entregas
    ativa = models.BooleanField(default=True, verbose_name='Ativa')

    class Meta:
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'
        # Ordena por data de expiração mais próxima
        ordering = ['data_expiracao']

    def __str__(self):
        return self.titulo
    
    def is_expired(self, data_comparacao=None):
        """Verifica se a tarefa expirou."""
        if data_comparacao:
            return self.data_expiracao < data_comparacao
        return self.data_expiracao < timezone.now()

# ====================================================================
# MODELO ENTREGA (Submetido pelo Aluno)
# ====================================================================
class Entrega(models.Model):
    """Representa a submissão de uma tarefa por um aluno."""
    
    tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE, related_name='entregas', 
                               verbose_name='Tarefa')
    
    # O aluno que fez a entrega (deve ser um usuário não-superuser)
    aluno = models.ForeignKey(User, on_delete=models.CASCADE, 
                              limit_choices_to={'is_superuser': False},
                              related_name='minhas_entregas',
                              verbose_name='Aluno')
    
    data_entrega = models.DateTimeField(default=timezone.now, verbose_name='Data da Entrega')
    
    # O arquivo submetido pelo aluno
    arquivo = models.FileField(upload_to=user_directory_path, verbose_name='Arquivo de Entrega')
    
    # Campos de Avaliação (preenchidos pelo professor)
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovada', 'Aprovada'),
        ('rejeitada', 'Rejeitada'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente', verbose_name='Status')
    nota = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Nota')
    comentarios_professor = models.TextField(null=True, blank=True, verbose_name='Comentários')

    class Meta:
        verbose_name = 'Entrega'
        verbose_name_plural = 'Entregas'
        # Garante que um aluno só pode ter uma entrega por tarefa
        unique_together = ('tarefa', 'aluno')
        # Ordena da entrega mais recente para a mais antiga
        ordering = ['-data_entrega']

    def __str__(self):
        return f'Entrega de {self.aluno.username} para {self.tarefa.titulo}'
    
    def clean(self):
        """Validação personalizada para garantir que a entrega não seja feita após o prazo."""
        if hasattr(self, 'tarefa') and self.tarefa and self.tarefa.is_expired():
            raise ValidationError('Esta tarefa expirou e não pode mais receber entregas.')

    def save(self, *args, **kwargs):
        # Chama a validação apenas se a tarefa estiver definida
        if hasattr(self, 'tarefa') and self.tarefa:
            self.clean()
        super().save(*args, **kwargs)

# ====================================================================
# MODELO DESIGNAÇÃO ALUNO-PROFESSOR
# ====================================================================
class DesignacaoAluno(models.Model):
    """Relaciona alunos com seus professores."""
    
    professor = models.ForeignKey(User, on_delete=models.CASCADE, 
                                  limit_choices_to={'is_superuser': True},
                                  related_name='alunos_designados',
                                  verbose_name='Professor')
    
    aluno = models.ForeignKey(User, on_delete=models.CASCADE, 
                              limit_choices_to={'is_superuser': False},
                              related_name='professor_designado',
                              verbose_name='Aluno')
    
    data_designacao = models.DateTimeField(default=timezone.now, verbose_name='Data da Designação')
    ativa = models.BooleanField(default=True, verbose_name='Ativa')

    class Meta:
        verbose_name = 'Designação de Aluno'
        verbose_name_plural = 'Designações de Alunos'
        unique_together = ('professor', 'aluno')
        ordering = ['-data_designacao']

    def __str__(self):
        return f'{self.aluno.username} -> {self.professor.username}'
