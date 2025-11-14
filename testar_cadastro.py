#!/usr/bin/env python
"""
Teste do sistema de cadastro
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_academico.settings')
django.setup()

from django.contrib.auth.models import User
from tarefas.models import DesignacaoAluno

def testar_cadastro():
    print("TESTANDO SISTEMA DE CADASTRO")
    print("=" * 40)
    
    # Verificar usuários existentes
    professores = User.objects.filter(is_superuser=True)
    alunos = User.objects.filter(is_superuser=False)
    
    print(f"Professores cadastrados: {professores.count()}")
    for prof in professores:
        print(f"  - {prof.username} ({prof.first_name} {prof.last_name})")
    
    print(f"\nAlunos cadastrados: {alunos.count()}")
    for aluno in alunos:
        print(f"  - {aluno.username} ({aluno.first_name} {aluno.last_name})")
    
    # Verificar designações
    designacoes = DesignacaoAluno.objects.all()
    print(f"\nDesignações ativas: {designacoes.count()}")
    for des in designacoes:
        print(f"  - {des.aluno.username} -> {des.professor.username}")
    
    print("\n" + "=" * 40)
    print("URLS DE CADASTRO:")
    print("  - Aluno: http://127.0.0.1:8000/cadastro/aluno/")
    print("  - Professor: http://127.0.0.1:8000/cadastro/professor/")
    print("  - Login: http://127.0.0.1:8000/auth/login/")
    print("=" * 40)
    
    print("\nCODIGO DO PROFESSOR: PROF2024")
    print("=" * 40)

if __name__ == '__main__':
    testar_cadastro()