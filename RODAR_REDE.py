#!/usr/bin/env python3
"""
VERBIUM - Rodar na Rede Local
Executa o servidor Django para acesso de outros dispositivos
"""

import os
import socket

def get_local_ip():
    """Obtém IP local da máquina"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "192.168.1.100"  # IP padrão se não conseguir detectar

def main():
    # Limpar tela
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("🚀 VERBIUM - Servidor na Rede")
    print("=" * 50)
    
    # Obter IP
    ip = get_local_ip()
    porta = "8000"
    
    print(f"📡 IP Local: {ip}")
    print(f"🔌 Porta: {porta}")
    print("=" * 50)
    
    print("🌐 COMO ACESSAR:")
    print(f"   • Neste PC: http://127.0.0.1:{porta}")
    print(f"   • Outros dispositivos: http://{ip}:{porta}")
    print("=" * 50)
    
    print("👥 USUÁRIOS DE TESTE:")
    print("   • Professor: admin / admin123")
    print("   • Aluno: aluno1 / senha123")
    print("=" * 50)
    
    print("📱 INSTRUÇÕES:")
    print("   1. Conecte outros dispositivos na MESMA rede WiFi")
    print(f"   2. Abra navegador e digite: http://{ip}:{porta}")
    print("   3. Faça login com os usuários acima")
    print("=" * 50)
    
    print("⚠️  IMPORTANTE:")
    print("   • Mantenha este terminal ABERTO")
    print("   • Para parar: Ctrl+C")
    print("   • Se não funcionar, libere porta 8000 no Firewall")
    print("=" * 50)
    
    input("Pressione ENTER para iniciar...")
    
    # Executar servidor
    comando = f"python manage.py runserver {ip}:{porta}"
    print(f"\n🚀 Executando: {comando}")
    print("=" * 50)
    
    os.system(comando)

if __name__ == "__main__":
    main()