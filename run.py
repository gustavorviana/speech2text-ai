#!/usr/bin/env python3
"""
Script simples para executar a aplicação de transcrição
"""

import sys

def check_installation():
    """Verifica se as dependências estão instaladas"""
    try:
        import torch
        import whisper
        return True
    except ImportError:
        return False

def main():
    if not check_installation():
        print("❌ Dependências não instaladas!")
        print("💡 Execute 'python setup_environment.py' primeiro.")
        sys.exit(1)
    
    try:
        from src.main import main as app_main
        app_main()
        
    except KeyboardInterrupt:
        print("\n")
        print("=" * 50)
        print("⛔ OPERAÇÃO CANCELADA PELO USUÁRIO")
        print("=" * 50)
        sys.exit(0)
    except Exception as e:
        print("\n")
        print("=" * 50)
        print("❌ ERRO INESPERADO")
        print("=" * 50)
        print(f"🐛 Erro: {e}")
        print("💡 Tente executar 'python setup_environment.py' para verificar a instalação.")
        print("=" * 50)
        sys.exit(1)

if __name__ == "__main__":
    print("🎙️ Iniciando transcritor...")
    main()