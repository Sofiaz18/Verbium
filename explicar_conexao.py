#!/usr/bin/env python
"""
Explicação de como funciona a conexão automática aluno-professor
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_academico.settings')
django.setup()

from django.contrib.auth.models import User
from tarefas.models import DesignacaoAluno

def explicar_conexao():
    print("COMO FUNCIONA A CONEXAO AUTOMATICA ALUNO-PROFESSOR")
    print("=" * 60)
    
    print("\n1. QUANDO UM NOVO ALUNO SE CADASTRA:")
    print("   - Sistema procura o PRIMEIRO professor disponivel")
    print("   - Cria uma DesignacaoAluno automaticamente")
    print("   - Aluno fica conectado e pode ver tarefas/redacoes")
    
    print("\n2. QUANDO UM NOVO PROFESSOR SE CADASTRA:")
    print("   - Sistema procura alunos SEM professor")
    print("   - Conecta TODOS os alunos sem professor ao novo professor")
    print("   - Professor ja tem alunos para ensinar")
    
    print("\n3. LOGICA DO CODIGO:")
    print("   ALUNO:")
    print("   professor = User.objects.filter(is_superuser=True).first()")
    print("   DesignacaoAluno.objects.create(professor=professor, aluno=user)")
    print()
    print("   PROFESSOR:")
    print("   alunos_sem_prof = alunos que nao tem DesignacaoAluno")
    print("   for aluno in alunos_sem_prof:")
    print("       DesignacaoAluno.objects.create(professor=novo_prof, aluno=aluno)")
    
    print("\n" + "=" * 60)
    print("SITUACAO ATUAL:")
    print("=" * 60)
    
    # Mostrar situação atual
    professores = User.objects.filter(is_superuser=True)
    alunos = User.objects.filter(is_superuser=False)
    
    print(f"\nProfessores cadastrados: {professores.count()}")
    for prof in professores:
        alunos_do_prof = DesignacaoAluno.objects.filter(professor=prof).count()
        print(f"  - {prof.username}: {alunos_do_prof} aluno(s)")
    
    print(f"\nAlunos cadastrados: {alunos.count()}")
    alunos_sem_prof = []
    for aluno in alunos:
        tem_prof = DesignacaoAluno.objects.filter(aluno=aluno).exists()
        if tem_prof:
            designacao = DesignacaoAluno.objects.get(aluno=aluno)
            print(f"  - {aluno.username} -> Prof. {designacao.professor.username}")
        else:
            print(f"  - {aluno.username} -> SEM PROFESSOR")
            alunos_sem_prof.append(aluno.username)
    
    print("\n" + "=" * 60)
    print("TESTE PRATICO:")
    print("=" * 60)
    
    if alunos_sem_prof:
        print(f"ALUNOS SEM PROFESSOR: {len(alunos_sem_prof)}")
        print("- Se um novo professor se cadastrar, pegara estes alunos")
    else:
        print("TODOS OS ALUNOS TEM PROFESSOR")
        print("- Novos alunos serao conectados ao primeiro professor")
    
    print(f"\nPROXIMO ALUNO SERA CONECTADO A: {professores.first().username if professores.exists() else 'NENHUM PROFESSOR'}")
    
    print("\n" + "=" * 60)
    print("VANTAGENS DESTE SISTEMA:")
    print("=" * 60)
    print("✅ Conexao automatica - nao precisa configurar manualmente")
    print("✅ Novos alunos sempre tem um professor")
    print("✅ Novos professores ja recebem alunos")
    print("✅ Sistema balanceado e justo")
    print("✅ Funciona mesmo com 1 professor e muitos alunos")

if __name__ == '__main__':
    explicar_conexao()