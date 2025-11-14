#!/usr/bin/env python
"""
Script para resetar senhas dos usuários
Execute: python resetar_senhas.py
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_academico.settings')
django.setup()

from django.contrib.auth.models import User

def resetar_senhas():
    # Resetar senha do admin
    try:
        admin = User.objects.get(username='admin')
        admin.set_password('admin123')
        admin.save()
        print("OK: Senha do admin resetada para 'admin123'")
    except User.DoesNotExist:
        print("ERRO: Usuario admin nao encontrado")

    # Resetar senhas dos alunos
    alunos = ['aluno1', 'aluno2', 'aluno3']
    for username in alunos:
        try:
            aluno = User.objects.get(username=username)
            aluno.set_password('senha123')
            aluno.save()
            print(f"OK: Senha do {username} resetada para 'senha123'")
        except User.DoesNotExist:
            print(f"ERRO: Usuario {username} nao encontrado")

    print("\nCredenciais atualizadas:")
    print("Professor: admin / admin123")
    print("Alunos: aluno1, aluno2, aluno3 / senha123")

if __name__ == '__main__':
    resetar_senhas()