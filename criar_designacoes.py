#!/usr/bin/env python
"""
Script para criar designações automáticas dos alunos para o professor admin
Execute: python criar_designacoes.py
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_academico.settings')
django.setup()

from django.contrib.auth.models import User
from tarefas.models import DesignacaoAluno

def criar_designacoes():
    # Buscar o professor admin
    try:
        professor = User.objects.get(username='admin', is_superuser=True)
        print(f"Professor encontrado: {professor.username}")
    except User.DoesNotExist:
        print("ERRO: Professor admin não encontrado")
        return

    # Buscar todos os alunos
    alunos = User.objects.filter(is_superuser=False)
    print(f"Alunos encontrados: {alunos.count()}")

    # Criar designações
    for aluno in alunos:
        designacao, criada = DesignacaoAluno.objects.get_or_create(
            professor=professor,
            aluno=aluno,
            defaults={'ativa': True}
        )
        
        if criada:
            print(f"OK: Designação criada - {aluno.username} -> {professor.username}")
        else:
            print(f"AVISO: Designação já existe - {aluno.username} -> {professor.username}")

    print(f"\nTotal de designações ativas: {DesignacaoAluno.objects.filter(ativa=True).count()}")

if __name__ == '__main__':
    criar_designacoes()