#!/usr/bin/env python
"""
Teste da funcionalidade trocar professor
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_academico.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def testar_trocar_professor():
    print("TESTANDO FUNCIONALIDADE TROCAR PROFESSOR")
    print("=" * 45)
    
    # Criar cliente de teste
    client = Client()
    
    # Pegar um aluno para testar
    aluno = User.objects.filter(is_superuser=False).first()
    
    if not aluno:
        print("ERRO: Nenhum aluno encontrado")
        return
    
    print(f"Testando com aluno: {aluno.username}")
    
    # Fazer login
    login_success = client.login(username=aluno.username, password='senha123')
    
    if not login_success:
        print("ERRO: Não conseguiu fazer login")
        return
    
    print("OK: Login realizado")
    
    # Testar acesso à página trocar professor
    try:
        response = client.get('/trocar-professor/')
        
        if response.status_code == 200:
            print("OK: Página trocar professor carregou")
            print(f"    Status: {response.status_code}")
        else:
            print(f"ERRO: Status {response.status_code}")
            
    except Exception as e:
        print(f"ERRO: {e}")
    
    # Testar professores disponíveis
    professores = User.objects.filter(is_superuser=True)
    print(f"Professores disponíveis: {professores.count()}")
    
    for prof in professores:
        from tarefas.models import DesignacaoAluno
        alunos_count = DesignacaoAluno.objects.filter(professor=prof, ativa=True).count()
        print(f"  - {prof.username}: {alunos_count} alunos")
    
    print("=" * 45)
    print("TESTE CONCLUÍDO")

if __name__ == '__main__':
    testar_trocar_professor()