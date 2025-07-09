import subprocess
import sys
import os

def run(command):
    print(f"\n🔧 Executando: {command}\n")
    try:
        subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro durante execução: {e}")
        return False

def uninstall_torch():
    """Remove instalações anteriores do PyTorch"""
    print("🗑️ Removendo instalações anteriores do PyTorch...")
    return run("pip uninstall -y torch torchvision torchaudio")

def install_cuda():
    """Instala PyTorch com suporte CUDA"""
    print("🚀 Instalando PyTorch com suporte CUDA (cu118)...")
    return run("pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")

def install_cpu():
    """Instala PyTorch versão CPU"""
    print("💻 Instalando PyTorch versão CPU...")
    return run("pip install torch torchvision torchaudio")

def install_requirements():
    """Instala demais dependências"""
    print("📦 Instalando demais dependências...")
    return run("pip install -r requirements-base.txt")

def check_cuda():
    """Verifica se CUDA está disponível"""
    try:
        import torch
        print(f"\n🐍 PyTorch versão: {torch.__version__}")
        
        if torch.cuda.is_available():
            print("✅ CUDA está disponível!")
            print(f"🖥️  GPU detectada: {torch.cuda.get_device_name(0)}")
            print(f"🔢 Versão CUDA: {torch.version.cuda}")
            print(f"🧮 Número de GPUs: {torch.cuda.device_count()}")
            
            try:
                x = torch.rand(5, 3).cuda()
                print(f"✅ Teste de tensor na GPU: Sucesso")
            except Exception as e:
                print(f"⚠️  Aviso no teste de GPU: {e}")
        else:
            print("❌ CUDA não está disponível.")
            print("💡 Usando versão CPU do PyTorch.")
            
    except ImportError:
        print("\n⚠️  PyTorch não está instalado.")
        print("💡 Execute a instalação primeiro (opção 1 ou 2).")
    except Exception as e:
        print(f"\n❌ Erro ao verificar CUDA: {e}")

def test_installation():
    """Testa se tudo está funcionando"""
    print("🧪 Testando instalação...")
    
    try:
        import whisper
        import torch
        
        print("✅ Todas as dependências importadas com sucesso!")
        print("🎤 Testando carregamento do modelo Whisper...")
        
        _ = whisper.load_model("tiny")
        print("✅ Modelo Whisper carregado com sucesso!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def menu():
    print("=" * 60)
    print("🎛️  INSTALADOR - AMBIENTE DE TRANSCRIÇÃO (WHISPER)")
    print("=" * 60)
    print("1. 🚀 Instalar com suporte a CUDA (recomendado se tiver GPU)")
    print("2. 💻 Instalar versão CPU (sem GPU)")
    print("3. 🗑️  Desinstalar PyTorch")
    print("4. 🔍 Verificar GPU/CUDA atual")
    print("5. 🧪 Testar instalação completa")
    print("6. 📖 Mostrar informações do sistema")
    print("0. 👋 Sair")
    print("=" * 60)

    escolha = input("Escolha uma opção: ").strip()

    try:
        if escolha == "1":
            print("\n🚀 INSTALAÇÃO COM CUDA")
            print("-" * 30)
            success = True
            success &= uninstall_torch()
            success &= install_cuda()
            success &= install_requirements()
            
            if success:
                print("\n✅ Instalação CUDA concluída!")
                check_cuda()
            else:
                print("\n❌ Houve problemas na instalação.")
                
        elif escolha == "2":
            print("\n💻 INSTALAÇÃO CPU")
            print("-" * 20)
            success = True
            success &= uninstall_torch()
            success &= install_cpu()
            success &= install_requirements()
            
            if success:
                print("\n✅ Instalação CPU concluída!")
                check_cuda()
            else:
                print("\n❌ Houve problemas na instalação.")
                
        elif escolha == "3":
            print("\n🗑️ DESINSTALAÇÃO")
            print("-" * 15)
            uninstall_torch()
            
        elif escolha == "4":
            print("\n🔍 VERIFICAÇÃO GPU/CUDA")
            print("-" * 25)
            check_cuda()

        elif escolha == "5":
            print("\n🧪 TESTE DE INSTALAÇÃO")
            print("-" * 23)
            test_installation()
            
        elif escolha == "6":
            print("\n📖 INFORMAÇÕES DO SISTEMA")
            print("-" * 28)
            print(f"🐍 Python: {sys.version}")
            print(f"📁 Diretório atual: {os.getcwd()}")
            check_cuda()
            
        elif escolha == "0":
            print("\n👋 Saindo do instalador...")
            sys.exit(0)
        else:
            print("❌ Opção inválida. Tente novamente.")
            
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro durante a execução: {e}")
    except KeyboardInterrupt:
        print("\n⛔ Operação cancelada pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
    
    input("\n⏸️  Pressione ENTER para continuar...")

if __name__ == "__main__":
    while True:
        try:
            menu()
        except KeyboardInterrupt:
            print("\n\n👋 Saindo...")
            break