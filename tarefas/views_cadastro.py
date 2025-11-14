from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms_cadastro import CadastroAlunoForm, CadastroProfessorForm
from .models import DesignacaoAluno

def cadastro_aluno(request):
    if request.method == 'POST':
        form = CadastroAlunoForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Verificar se foi escolhido um professor específico
            professor_escolhido_id = request.POST.get('professor_escolhido')
            
            if professor_escolhido_id and professor_escolhido_id != 'automatico':
                # Conectar ao professor escolhido
                professor = User.objects.get(id=professor_escolhido_id, is_superuser=True)
                DesignacaoAluno.objects.create(professor=professor, aluno=user)
                messages.success(request, f'Cadastro realizado! Você foi conectado ao Prof. {professor.first_name or professor.username}.')
            else:
                # Designar automaticamente para o primeiro professor disponível
                professor = User.objects.filter(is_superuser=True).first()
                if professor:
                    DesignacaoAluno.objects.create(professor=professor, aluno=user)
                    messages.success(request, f'Cadastro realizado! Você foi conectado automaticamente ao Prof. {professor.first_name or professor.username}.')
                else:
                    messages.success(request, 'Cadastro realizado! Aguarde um professor se cadastrar para receber tarefas.')
            
            return redirect('/auth/login/')
    else:
        form = CadastroAlunoForm()
    
    # Buscar professores disponíveis para mostrar na tela
    professores = User.objects.filter(is_superuser=True)
    
    return render(request, 'registration/cadastro_aluno.html', {
        'form': form,
        'professores': professores
    })

def cadastro_professor(request):
    if request.method == 'POST':
        form = CadastroProfessorForm(request.POST)
        if form.is_valid():
            # Verificar código do professor (simples validação)
            codigo = form.cleaned_data['codigo_professor']
            if codigo != 'PROF2024':  # Código fixo para demo
                messages.error(request, 'Código do professor inválido!')
                return render(request, 'registration/cadastro_professor.html', {'form': form})
            
            user = form.save()
            user.is_superuser = True
            user.is_staff = True
            user.save()
            
            # Conectar alunos sem professor automaticamente
            alunos_com_professor = DesignacaoAluno.objects.values_list('aluno_id', flat=True)
            alunos_sem_professor = User.objects.filter(
                is_superuser=False
            ).exclude(id__in=alunos_com_professor)
            
            count_conectados = 0
            for aluno in alunos_sem_professor:
                DesignacaoAluno.objects.create(professor=user, aluno=aluno)
                count_conectados += 1
            
            if count_conectados > 0:
                messages.success(request, f'Cadastro realizado! Você foi conectado a {count_conectados} aluno(s) que estavam aguardando.')
            else:
                messages.success(request, 'Cadastro de professor realizado com sucesso!')
            
            return redirect('/auth/login/')
    else:
        form = CadastroProfessorForm()
    
    return render(request, 'registration/cadastro_professor.html', {'form': form})