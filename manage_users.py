#!/usr/bin/env python
"""
Script para criar usuários de teste no sistema
Execute: python manage_users.py
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_academico.settings')
django.setup()

from django.contrib.auth.models import User

def criar_usuarios():
    # Criar superusuário (Professor)
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@exemplo.com',
            password='admin123',
            first_name='Professor',
            last_name='Admin'
        )
        print(f"OK: Professor criado: {admin.username}")
    else:
        print("AVISO: Professor 'admin' ja existe")

    # Criar alunos de teste
    alunos = [
        {'username': 'aluno1', 'first_name': 'João', 'last_name': 'Silva'},
        {'username': 'aluno2', 'first_name': 'Maria', 'last_name': 'Santos'},
        {'username': 'aluno3', 'first_name': 'Pedro', 'last_name': 'Costa'},
    ]

    for aluno_data in alunos:
        if not User.objects.filter(username=aluno_data['username']).exists():
            aluno = User.objects.create_user(
                username=aluno_data['username'],
                email=f"{aluno_data['username']}@exemplo.com",
                password='senha123',
                first_name=aluno_data['first_name'],
                last_name=aluno_data['last_name']
            )
            print(f"OK: Aluno criado: {aluno.username}")
        else:
            print(f"AVISO: Aluno '{aluno_data['username']}' ja existe")

if __name__ == '__main__':
    criar_usuarios()
    print("\nUsuarios criados com sucesso!")
    print("\nCredenciais para teste:")
    print("Professor: admin / admin123")
    print("Alunos: aluno1, aluno2, aluno3 / senha123")