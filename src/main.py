from .menu import choose_mode_and_params
from .transcriber import AudioTranscriber

def main():
    print("🎙️ Transcritor de Áudio para TXT")
    print("=" * 50)
    
    try:
        params = choose_mode_and_params()
        
        profile_name = params.get("profile_name")
        if profile_name:
            print(f"\n🎯 Executando com perfil: {profile_name}")
        else:
            print(f"\n⚙️ Configurações personalizadas:")
        
        print(f"📊 Modelo: {params['model']}")
        print(f"🎯 Beam size: {params['beam_size']}")
        print(f"🎯 Best of: {params['best_of']}")
        print(f"🌡️ Temperature: {params['temperature']}")
        print("-" * 50)
        
        transcriber = AudioTranscriber(params)
        transcriber.initialize()
        transcriber.transcribe_files()
    except Exception as e:
        print("\n")
        print("❌" * 25)
        print("💥 ERRO INESPERADO")
        print("❌" * 25)
        print(f"🐛 Detalhes do erro: {e}")
        print("🔧 Possíveis soluções:")
        print("   1. Verificar se os arquivos de áudio estão na pasta data/input/")
        print("   2. Executar 'python setup_environment.py' para verificar instalação")
        print("   3. Tentar com um modelo menor (tiny ou base)")
        print("❌" * 25)
        raise

if __name__ == "__main__":
    main()