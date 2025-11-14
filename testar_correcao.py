#!/usr/bin/env python
"""
Teste do sistema de correção
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_academico.settings')
django.setup()

from tarefas.models_redacao import RedacaoEntrega, RedacaoCorrecao
from django.contrib.auth.models import User

def testar_correcao():
    print("TESTANDO SISTEMA DE CORRECAO")
    print("=" * 35)
    
    # Buscar uma entrega para testar
    entrega = RedacaoEntrega.objects.first()
    
    if not entrega:
        print("ERRO: Nenhuma entrega encontrada")
        return
    
    print(f"Testando entrega: {entrega.id}")
    print(f"Aluno: {entrega.aluno.username}")
    print(f"Tema: {entrega.tema.titulo}")
    
    # Buscar professor
    professor = User.objects.filter(is_superuser=True).first()
    
    if not professor:
        print("ERRO: Nenhum professor encontrado")
        return
    
    print(f"Professor: {professor.username}")
    
    # Testar criação de correção
    try:
        correcao, created = RedacaoCorrecao.objects.get_or_create(
            entrega=entrega,
            defaults={
                'professor': professor,
                'competencia_1': 120,
                'competencia_2': 140,
                'competencia_3': 100,
                'competencia_4': 80,
                'competencia_5': 60
            }
        )
        
        if created:
            print("OK: Correção criada com sucesso")
        else:
            print("OK: Correção já existia")
        
        print(f"Nota total: {correcao.nota_total}/1000")
        
    except Exception as e:
        print(f"ERRO: {e}")
    
    print("=" * 35)
    print("TESTE CONCLUÍDO")

if __name__ == '__main__':
    testar_correcao()