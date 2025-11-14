#!/usr/bin/env python
"""
Script para testar o sistema completo
Execute: python testar_sistema.py
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_academico.settings')
django.setup()

from django.contrib.auth.models import User
from tarefas.models import Tarefa, Entrega, DesignacaoAluno
from django.utils import timezone
from datetime import timedelta

def testar_sistema():
    print("=== TESTE DO SISTEMA DE TAREFAS ACADEMICO ===\n")
    
    # 1. Verificar usuários
    print("1. USUARIOS:")
    usuarios = User.objects.all()
    for user in usuarios:
        tipo = "Professor" if user.is_superuser else "Aluno"
        print(f"   - {user.username} ({tipo})")
    
    # 2. Verificar designações
    print(f"\n2. DESIGNACOES:")
    designacoes = DesignacaoAluno.objects.filter(ativa=True)
    for des in designacoes:
        print(f"   - {des.aluno.username} -> {des.professor.username}")
    
    # 3. Criar tarefa de teste se não existir
    print(f"\n3. TAREFAS:")
    professor = User.objects.get(username='admin')
    tarefa_teste, criada = Tarefa.objects.get_or_create(
        titulo="Tarefa de Teste",
        professor=professor,
        defaults={
            'descricao': 'Esta é uma tarefa de teste criada automaticamente.',
            'data_expiracao': timezone.now() + timedelta(days=7),
            'ativa': True
        }
    )
    
    if criada:
        print(f"   - Tarefa de teste criada: {tarefa_teste.titulo}")
    else:
        print(f"   - Tarefa de teste já existe: {tarefa_teste.titulo}")
    
    tarefas = Tarefa.objects.filter(ativa=True)
    print(f"   - Total de tarefas ativas: {tarefas.count()}")
    
    # 4. Verificar entregas
    print(f"\n4. ENTREGAS:")
    entregas = Entrega.objects.all()
    print(f"   - Total de entregas: {entregas.count()}")
    for entrega in entregas:
        print(f"   - {entrega.aluno.username} -> {entrega.tarefa.titulo}")
    
    print(f"\n=== CREDENCIAIS PARA TESTE ===")
    print(f"Professor: admin / admin123")
    print(f"Alunos: aluno1, aluno2, aluno3 / senha123")
    
    print(f"\n=== URLS IMPORTANTES ===")
    print(f"Página inicial: http://127.0.0.1:8000/")
    print(f"Login: http://127.0.0.1:8000/auth/login/")
    print(f"Dashboard: http://127.0.0.1:8000/dashboard/")
    print(f"Tarefas: http://127.0.0.1:8000/tarefas/")
    print(f"Admin: http://127.0.0.1:8000/admin/")
    
    print(f"\n=== SISTEMA PRONTO PARA USO! ===")

if __name__ == '__main__':
    testar_sistema()