#!/usr/bin/env python
"""
Script para rodar o Verbium na rede local
Permite acesso de outros dispositivos na mesma rede
"""

import os
import sys
import socket
import subprocess

def get_local_ip():
    """Obtém o IP local da máquina"""
    try:
        # Conecta a um endereço externo para descobrir o IP local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

def main():
    print("🚀 VERBIUM - Iniciando servidor na rede local...")
    print("=" * 50)
    
    # Obtém o IP local
    local_ip = get_local_ip()
    port = "8000"
    
    print(f"📡 IP Local: {local_ip}")
    print(f"🔌 Porta: {port}")
    print("=" * 50)
    
    print("🌐 URLs de Acesso:")
    print(f"   • Local: http://127.0.0.1:{port}")
    print(f"   • Rede:  http://{local_ip}:{port}")
    print("=" * 50)
    
    print("📱 Para acessar de outros dispositivos:")
    print(f"   1. Conecte o dispositivo na mesma rede WiFi")
    print(f"   2. Abra o navegador e digite: http://{local_ip}:{port}")
    print("=" * 50)
    
    print("👥 Usuários de teste:")
    print("   • Professor: admin / admin123")
    print("   • Aluno: aluno1 / senha123")
    print("=" * 50)
    
    print("⚠️  IMPORTANTE:")
    print("   • Mantenha este terminal aberto")
    print("   • Para parar: Ctrl+C")
    print("   • Firewall pode bloquear - libere a porta 8000")
    print("=" * 50)
    
    input("Pressione ENTER para iniciar o servidor...")
    
    try:
        # Inicia o servidor Django
        os.system(f"python manage.py runserver {local_ip}:{port}")
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor parado pelo usuário")
        print("✅ Verbium encerrado com sucesso!")

if __name__ == "__main__":
    main()