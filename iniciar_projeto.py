#!/usr/bin/env python
"""
Script para inicializar o projeto completo
Execute: python iniciar_projeto.py
"""
import os
import subprocess
import sys

def executar_comando(comando, descricao):
    print(f"Executando: {descricao}...")
    try:
        result = subprocess.run(comando, shell=True, check=True, capture_output=True, text=True)
        print(f"OK: {descricao} - Concluido")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERRO em {descricao}: {e}")
        print(f"Saida: {e.stdout}")
        print(f"Erro: {e.stderr}")
        return False

def main():
    print("Inicializando Sistema de Tarefas Academico")
    print("=" * 50)
    
    # 1. Aplicar migrações
    if not executar_comando("python manage.py makemigrations", "Criando migrações"):
        return
    
    if not executar_comando("python manage.py migrate", "Aplicando migrações"):
        return
    
    # 2. Criar usuários de teste
    if not executar_comando("python manage_users.py", "Criando usuários de teste"):
        return
    
    print("\nSistema inicializado com sucesso!")
    print("\nProximos passos:")
    print("1. Execute: python manage.py runserver")
    print("2. Acesse: http://127.0.0.1:8000")
    print("3. Faca login com:")
    print("   - Professor: admin / admin123")
    print("   - Aluno: aluno1 / senha123")
    print("\nDica: O professor pode criar tarefas e os alunos podem enviar arquivos!")

if __name__ == '__main__':
    main()