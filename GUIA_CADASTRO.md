# 👥 VERBIUM - Guia de Cadastro de Usuários

## 🎯 Como Novos Usuários se Cadastram

### 📝 **Para Alunos:**

1. **Acesse:** `http://SEU_IP:8000/cadastro/aluno/`
2. **Preencha:**
   - Nome de usuário (único)
   - Nome e sobrenome
   - Email
   - Senha (2x para confirmar)
3. **Clique:** "Cadastrar como Aluno"
4. **Resultado:** Será conectado automaticamente a um professor disponível

### 👨🏫 **Para Professores:**

1. **Acesse:** `http://SEU_IP:8000/cadastro/professor/`
2. **Preencha:**
   - Nome de usuário (único)
   - Nome e sobrenome
   - Email
   - Senha (2x para confirmar)
   - **Código do Professor:** `PROF2024`
3. **Clique:** "Cadastrar como Professor"
4. **Resultado:** Vira superusuário e conecta alunos sem professor

## 🔗 **URLs Importantes:**

- **Home:** `http://SEU_IP:8000/`
- **Login:** `http://SEU_IP:8000/auth/login/`
- **Cadastro Aluno:** `http://SEU_IP:8000/cadastro/aluno/`
- **Cadastro Professor:** `http://SEU_IP:8000/cadastro/professor/`

## 👥 **Usuários Já Existentes:**

### Professores:
- `admin` / `admin123`
- `fernando` / (senha dele)

### Alunos:
- `aluno1` / `senha123` (João Silva)
- `aluno2` / `senha123` (Maria Santos)
- `aluno3` / `senha123` (Pedro Costa)
- `Sofia` / (senha dela) (Sofia Zanini Galletti)

## 🔄 **Como Funciona a Conexão:**

1. **Aluno se cadastra** → Conecta automaticamente ao primeiro professor disponível
2. **Professor se cadastra** → Conecta automaticamente alunos que não têm professor
3. **Sistema garante** que todo aluno tem um professor designado

## ⚠️ **Importante:**

- **Código do Professor:** `PROF2024` (necessário para cadastro de professor)
- **Nomes únicos:** Cada usuário precisa de um username único
- **Conexão automática:** Sistema conecta alunos e professores automaticamente
- **Redações:** Só funcionam para alunos conectados a professores

## 🚀 **Testando:**

1. Cadastre um novo aluno em: `/cadastro/aluno/`
2. Faça login com as credenciais criadas
3. Vá em "Redações" para ver os temas disponíveis
4. Escreva uma redação e veja a correção automática!

---

**✅ Sistema de cadastro funcionando perfeitamente!**
**Novos usuários podem se registrar e usar todas as funcionalidades!**