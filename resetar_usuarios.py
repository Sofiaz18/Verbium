#!/usr/bin/env python
"""
Script para resetar senhas dos usuários de teste
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_academico.settings')
django.setup()

from django.contrib.auth.models import User

def resetar_senhas():
    print("RESETANDO SENHAS DOS USUARIOS...")
    print("=" * 40)
    
    # Professor
    try:
        admin = User.objects.get(username='admin')
        admin.set_password('admin123')
        admin.save()
        print("OK Professor 'admin' - senha: admin123")
    except User.DoesNotExist:
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@exemplo.com',
            password='admin123',
            first_name='Professor',
            last_name='Admin'
        )
        print("OK Professor 'admin' criado - senha: admin123")
    
    # Alunos
    alunos = ['aluno1', 'aluno2', 'aluno3']
    nomes = ['João Silva', 'Maria Santos', 'Pedro Costa']
    
    for i, username in enumerate(alunos):
        try:
            aluno = User.objects.get(username=username)
            aluno.set_password('senha123')
            aluno.save()
            print(f"OK Aluno '{username}' - senha: senha123")
        except User.DoesNotExist:
            nome_completo = nomes[i].split()
            aluno = User.objects.create_user(
                username=username,
                email=f'{username}@exemplo.com',
                password='senha123',
                first_name=nome_completo[0],
                last_name=nome_completo[1]
            )
            print(f"OK Aluno '{username}' criado - senha: senha123")
    
    print("=" * 40)
    print("USUARIOS PRONTOS PARA USAR!")
    print("=" * 40)
    print("PROFESSOR:")
    print("   Usuário: admin")
    print("   Senha: admin123")
    print()
    print("ALUNOS:")
    print("   Usuário: aluno1, aluno2, aluno3")
    print("   Senha: senha123")
    print("=" * 40)

if __name__ == '__main__':
    resetar_senhas()