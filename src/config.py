from pathlib import Path
import json

class Config:
    PROJECT_ROOT = Path(__file__).parent.parent
    DATA_DIR = PROJECT_ROOT / "data"
    INPUT_DIR = DATA_DIR / "input"
    OUTPUT_DIR = DATA_DIR / "output"
    PROFILES_DIR = PROJECT_ROOT / "profiles"
    PROFILES_FILE = PROFILES_DIR / "profiles.json"
    
    AVAILABLE_MODELS = ["tiny", "base", "small", "medium", "large", "large-v3"]
    
    DEFAULT_MODEL = "medium"
    DEFAULT_BEAM_SIZE = 1
    DEFAULT_BEST_OF = 1
    DEFAULT_TEMPERATURE = 0.0
    
    SUPPORTED_AUDIO_FORMATS = [".mp3", ".wav", ".m4a", ".flac", ".opus"]
    
    @classmethod
    def ensure_directories(cls):
        """Cria os diretórios necessários se não existirem"""
        cls.INPUT_DIR.mkdir(parents=True, exist_ok=True)
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        cls.PROFILES_DIR.mkdir(parents=True, exist_ok=True)
        
        if not cls.PROFILES_FILE.exists():
            cls._create_default_profiles()
    
    @classmethod
    def _create_default_profiles(cls):
        """Cria perfis padrão"""
        default_profiles = {
            "Rápido": {
                "model": "tiny",
                "beam_size": 1,
                "best_of": 1,
                "temperature": 0.0,
                "description": "Transcrição rápida com qualidade básica"
            },
            "Equilibrado": {
                "model": "base",
                "beam_size": 1,
                "best_of": 1,
                "temperature": 0.0,
                "description": "Boa relação velocidade/qualidade"
            },
            "Qualidade": {
                "model": "medium",
                "beam_size": 5,
                "best_of": 3,
                "temperature": 0.0,
                "description": "Alta qualidade, velocidade moderada"
            },
            "Máxima Precisão": {
                "model": "large",
                "beam_size": 10,
                "best_of": 5,
                "temperature": 0.0,
                "description": "Máxima qualidade possível (mais lento)"
            }
        }
        
        with open(cls.PROFILES_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_profiles, f, indent=4, ensure_ascii=False)
    
    @classmethod
    def load_profiles(cls):
        """Carrega todos os perfis salvos"""
        cls.ensure_directories()
        
        try:
            with open(cls.PROFILES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            cls._create_default_profiles()
            return cls.load_profiles()
    
    @classmethod
    def save_profiles(cls, profiles):
        """Salva perfis no arquivo"""
        cls.ensure_directories()
        
        with open(cls.PROFILES_FILE, 'w', encoding='utf-8') as f:
            json.dump(profiles, f, indent=4, ensure_ascii=False)
    
    @classmethod
    def save_profile(cls, name, params, description=""):
        """Salva um perfil específico"""
        profiles = cls.load_profiles()
        profiles[name] = {
            "model": params["model"],
            "beam_size": params["beam_size"],
            "best_of": params["best_of"],
            "temperature": params["temperature"],
            "description": description
        }
        cls.save_profiles(profiles)
    
    @classmethod
    def get_profile(cls, name):
        """Retorna um perfil específico"""
        profiles = cls.load_profiles()
        return profiles.get(name)
    
    @classmethod
    def delete_profile(cls, name):
        """Remove um perfil"""
        profiles = cls.load_profiles()
        if name in profiles:
            del profiles[name]
            cls.save_profiles(profiles)
            return True
        return False