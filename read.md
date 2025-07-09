# 🎙️ Speech2Text AI

Transcritor de arquivos de áudio para texto usando OpenAI Whisper.

## 🚀 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/speech2text-ai.git
cd speech2text-ai
```

### 2. Configure o ambiente
```bash
python setup_environment.py
```

Escolha:
- **Opção 1**: Com GPU (mais rápido)
- **Opção 2**: Apenas CPU (qualquer PC)

### 3. Execute
```bash
python run.py
```

## 📁 Como usar

1. Coloque arquivos de áudio em `data/input/`
2. Execute `python run.py`
3. Transcrições aparecerão em `data/output/`

## 🎵 Formatos suportados
MP3, WAV, M4A, FLAC

## 🎯 Modelos disponíveis
- `tiny` - Rápido, qualidade básica
- `base` - Equilibrado
- `medium` - **Recomendado**
- `large` - Máxima qualidade

## 📁 Estrutura do projeto
```
speech2text-ai/
├── src/                  # Código fonte
├── data/
│   ├── input/           # 📥 Seus arquivos de áudio
│   └── output/          # 📤 Transcrições
├── setup_environment.py # 🛠️ Instalador
└── run.py              # 🏃 Executar
```

## 🔧 Comandos úteis

```bash
# Configurar ambiente
python setup_environment.py

# Executar aplicação
python run.py

# Ou executar diretamente
python -m src.main
```

## 🐛 Problemas?

- **GPU não funciona**: Execute `setup_environment.py`, opção 1
- **Muito lento**: Use modelo `tiny` ou `base`
- **Erro de instalação**: Execute `setup_environment.py`, opção 6 para testar

## 📊 Performance esperada

**Com GPU**: 10-20x mais rápido que tempo real  
**Apenas CPU**: 1-2x tempo real

---

⭐ **Se foi útil, deixe uma estrela no GitHub!**