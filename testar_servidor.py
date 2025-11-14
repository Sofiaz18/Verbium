import socket
import subprocess
import sys

def get_ip():
    """Pega o IP local"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def test_django():
    """Testa se Django está funcionando"""
    try:
        result = subprocess.run([sys.executable, "manage.py", "check"], 
                              capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def main():
    print("🔍 TESTANDO VERBIUM...")
    print("=" * 40)
    
    # Teste Django
    if test_django():
        print("✅ Django: OK")
    else:
        print("❌ Django: ERRO")
        return
    
    # IP Local
    ip = get_ip()
    print(f"📡 IP Local: {ip}")
    
    print("=" * 40)
    print("🚀 INICIANDO SERVIDOR...")
    print(f"🌐 Acesse de outros dispositivos: http://{ip}:8000")
    print("⚠️  Certifique-se que estão na mesma rede WiFi")
    print("=" * 40)
    
    # Iniciar servidor
    try:
        subprocess.run([sys.executable, "manage.py", "runserver", f"{ip}:8000"])
    except KeyboardInterrupt:
        print("\n🛑 Servidor parado")

if __name__ == "__main__":
    main()