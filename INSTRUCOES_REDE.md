# 🌐 VERBIUM - Acesso na Rede Local

## 🚀 Como Rodar na Rede

### Método 1: Script Automático (Recomendado)
```bash
python rodar_na_rede.py
```

### Método 2: Manual
```bash
# Descobrir seu IP local
ipconfig

# Rodar o servidor (substitua SEU_IP pelo IP encontrado)
python manage.py runserver SEU_IP:8000
```

## 📱 Como Acessar de Outros Dispositivos

### 1. **Conectar na Mesma Rede**
- Certifique-se que todos os dispositivos estão na mesma rede WiFi

### 2. **Descobrir o IP**
- Execute o script `rodar_na_rede.py`
- Ou use o comando `ipconfig` no Windows
- Procure por algo como: `192.168.1.100`

### 3. **Acessar pelo Navegador**
- No outro notebook/celular, digite: `http://192.168.1.100:8000`
- Substitua `192.168.1.100` pelo seu IP real

## 🔧 Possíveis Problemas

### ❌ "Não consegue acessar"
**Soluções:**
1. **Firewall do Windows:**
   - Vá em: Painel de Controle → Firewall → Permitir app
   - Adicione Python ou libere a porta 8000

2. **Antivírus:**
   - Temporariamente desabilite ou adicione exceção

3. **Rede diferente:**
   - Verifique se ambos dispositivos estão na mesma WiFi

### ❌ "Página não carrega"
**Soluções:**
1. Verifique se o servidor está rodando
2. Teste primeiro no próprio computador: `http://127.0.0.1:8000`
3. Confirme o IP correto com `ipconfig`

## 📋 Checklist Rápido

- [ ] Ambos dispositivos na mesma rede WiFi
- [ ] Servidor rodando com IP correto
- [ ] Firewall liberado para porta 8000
- [ ] URL correta: `http://SEU_IP:8000`

## 🎯 Exemplo Prático

Se seu IP for `192.168.0.105`:

1. **Rodar servidor:**
   ```bash
   python manage.py runserver 192.168.0.105:8000
   ```

2. **Acessar de outro dispositivo:**
   ```
   http://192.168.0.105:8000
   ```

## 👥 Usuários para Teste

- **Professor:** `admin` / `admin123`
- **Aluno:** `aluno1` / `senha123`

## 🔒 Segurança

⚠️ **ATENÇÃO:** Esta configuração é apenas para desenvolvimento/teste local.
Para produção, configure adequadamente o `ALLOWED_HOSTS` e use HTTPS.

---

**🚀 Pronto! Agora você pode acessar o Verbium de qualquer dispositivo na sua rede!**