import whisper
import time
import torch
import threading
import queue
from pathlib import Path
from .config import Config

class AudioTranscriber:
    def __init__(self, params):
        self.params = params
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.interrupted = False
        
    def initialize(self):
        """Inicializa o modelo e configura a GPU"""
        print(f"🖥️ Dispositivo: {self.device.upper()}")
        
        if self.device == "cuda":
            print(f"🎮 GPU: {torch.cuda.get_device_name(0)}")
            torch.backends.cudnn.benchmark = True
            torch.backends.cuda.matmul.allow_tf32 = True
            torch.backends.cudnn.allow_tf32 = True

        print(f"🤖 Carregando modelo Whisper '{self.params['model']}'...")
        start_time = time.time()

        self._load_model()

        if self.device == "cuda":
            print("🔥 GPU preparada para uso")
            torch.cuda.empty_cache()

        load_time = time.time() - start_time
        print(f"✅ Modelo {self.params['model']} carregado em {load_time:.1f}s")

    def _load_model(self):
        result_queue = queue.Queue()
        
        loading_thread = threading.Thread(
            target=self._load_model_thread, 
            args=(result_queue,)
        )
        loading_thread.daemon = True
        loading_thread.start()
        
        try:
            while loading_thread.is_alive():
                try:
                    status, result = result_queue.get(timeout=0.1)
                    
                    if status == "success":
                        self.model = result
                        break
                    elif status == "error":
                        raise result
                        
                except queue.Empty:
                    continue
                except KeyboardInterrupt:
                    print("\n⛔ Carregamento do modelo cancelado...")
                    raise
            
            if not hasattr(self, 'model') or self.model is None:
                try:
                    status, result = result_queue.get(timeout=1)
                    if status == "success":
                        self.model = result
                    elif status == "error":
                        raise result
                except queue.Empty:
                    raise RuntimeError("Timeout no carregamento do modelo")
        
        finally:
            loading_thread.join(timeout=1)

    def _load_model_thread(self, result_queue):
        """Carrega o modelo em thread separada"""
        try:
            model = whisper.load_model(self.params["model"], device=self.device)
            result_queue.put(("success", model))
        except Exception as e:
            result_queue.put(("error", e))

    def transcribe_files(self):
        """Transcreve todos os arquivos de áudio encontrados"""
        if not self.model:
            raise RuntimeError("Modelo não foi inicializado. Chame initialize() primeiro.")
            
        Config.ensure_directories()
        
        audio_files = self._get_audio_files()
        if not audio_files:
            print("❌ Nenhum arquivo de áudio encontrado na pasta 'data/input'.")
            return

        print(f"\n🎵 Encontrados {len(audio_files)} arquivos de áudio")
        print(f"📁 Salvando transcrições em: {Config.OUTPUT_DIR}")
        print("💡 Pressione Ctrl+C para cancelar a qualquer momento")
        print("-" * 50)

        total_transcribe_time = 0
        total_audio_duration = 0
        processed_files = 0
        
        try:
            for i, audio_file in enumerate(audio_files, 1):
                if self.interrupted:
                    break
                    
                txt_file = Config.OUTPUT_DIR / f"{audio_file.stem}.txt"

                if txt_file.exists():
                    print(f"[{i}/{len(audio_files)}] ⚠️ {audio_file.name} -> Já transcrito, pulando...")
                    continue

                result = self._transcribe_single_file(audio_file, i, len(audio_files))
                if result:
                    total_transcribe_time += result["transcribe_time"]
                    total_audio_duration += result["audio_duration"]
                    processed_files += 1

        except KeyboardInterrupt:
            self.interrupted = True
            raise

        self._print_summary(total_transcribe_time, total_audio_duration, processed_files, len(audio_files))

    def _get_audio_files(self):
        """Retorna lista de arquivos de áudio suportados"""
        audio_files = []
        for format_ext in Config.SUPPORTED_AUDIO_FORMATS:
            audio_files.extend(Config.INPUT_DIR.glob(f"*{format_ext}"))
        return audio_files

    def _transcribe_single_file(self, audio_file, current_index, total_files):
        """Transcreve um único arquivo de áudio"""
        print(f"[{current_index}/{total_files}] 🎧 Transcrevendo: {audio_file.name}")

        try:
            transcribe_start = time.time()
            
            transcribe_options = {
                "language": "pt",
                "verbose": False,
                "condition_on_previous_text": False,
                "temperature": self.params["temperature"],
                "compression_ratio_threshold": 2.4,
                "logprob_threshold": -1.0,
                "no_speech_threshold": 0.6,
                "beam_size": self.params["beam_size"],
                "best_of": self.params["best_of"],
            }

            if self.device == "cuda":
                transcribe_options["fp16"] = True

            result = self.model.transcribe(str(audio_file), **transcribe_options)
            transcribe_time = time.time() - transcribe_start

            if self.device == "cuda":
                torch.cuda.empty_cache()

            txt_file = Config.OUTPUT_DIR / f"{audio_file.stem}.txt"
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(result["text"].strip())

            return self._print_file_result(txt_file, result, transcribe_time)

        except KeyboardInterrupt:
            raise
        except Exception as e:
            print(f"   ❌ Erro ao transcrever {audio_file.name}: {e}")
            return None

    def _print_file_result(self, txt_file, result, transcribe_time):
        """Imprime resultado da transcrição de um arquivo"""
        word_count = len(result["text"].split())
        
        audio_duration = result.get("segments", [])
        if audio_duration:
            audio_duration = audio_duration[-1].get("end", 0)
        else:
            audio_duration = transcribe_time

        speed_factor = audio_duration / transcribe_time if transcribe_time > 0 and audio_duration > 0 else 0
        speed_text = f"({speed_factor:.1f}x tempo real)" if speed_factor > 1 else ""

        print(f"   ✅ Salvo: {txt_file.name}")
        print(f"   ⏱️ Tempo: {transcribe_time:.1f}s {speed_text}")
        print(f"   📝 Palavras: {word_count}")
        print(f"   👀 Prévia: {result['text'][:80]}...")
        print()

        return {
            "transcribe_time": transcribe_time,
            "audio_duration": audio_duration
        }

    def _print_summary(self, total_transcribe_time, total_audio_duration, processed_files, total_files):
        """Imprime resumo final da transcrição"""
        print("\n")
        
        if processed_files == total_files:
            print("🎉 TRANSCRIÇÃO CONCLUÍDA COM SUCESSO!")
        else:
            print("⚠️ TRANSCRIÇÃO PARCIALMENTE CONCLUÍDA")
        
        print("\n")
        print(f"📊 Arquivos processados: {processed_files}/{total_files}")
        
        if total_transcribe_time > 0 and total_audio_duration > 0:
            overall_speed = total_audio_duration / total_transcribe_time
            print(f"⚡ Velocidade geral: {overall_speed:.1f}x tempo real")
        
        print(f"📁 Arquivos salvos em: {Config.OUTPUT_DIR}")
        
        if processed_files < total_files:
            remaining = total_files - processed_files
            print(f"🔄 {remaining} arquivo(s) restante(s) - execute novamente para continuar")