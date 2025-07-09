from .config import Config

def choose_mode_and_params():
    print("🛠️ Escolha o modo de execução:")
    print("1. Padrão (modelo 'medium' com parâmetros padrão)")
    print("2. Avançado (escolher modelo e parâmetros)")
    print("3. 💾 Criar/Editar perfil personalizado")
    print("4. 🎯 Executar com perfil salvo")
    choice = input("Digite 1, 2, 3 ou 4: ").strip()

    if choice == "2":
        return _advanced_mode_selection()
    elif choice == "3":
        return _create_or_edit_profile()
    elif choice == "4":
        return _execute_with_profile()
    else:
        return _default_mode_selection()

def _advanced_mode_selection():
    """Configuração avançada com seleção de modelo e parâmetros"""
    model = _select_model()
    beam_size = _select_beam_size()
    best_of = _select_best_of()
    temperature = _select_temperature()
    
    return {
        "model": model,
        "beam_size": beam_size,
        "best_of": best_of,
        "temperature": temperature,
    }

def _default_mode_selection():
    """Configuração padrão com parâmetros fixos"""
    return {
        "model": Config.DEFAULT_MODEL,
        "beam_size": Config.DEFAULT_BEAM_SIZE,
        "best_of": Config.DEFAULT_BEST_OF,
        "temperature": Config.DEFAULT_TEMPERATURE,
    }

def _create_or_edit_profile():
    """Cria ou edita um perfil personalizado"""
    print("\n💾 CRIAÇÃO/EDIÇÃO DE PERFIL")
    print("=" * 40)
    
    profiles = Config.load_profiles()
    if profiles:
        print("📋 Perfis existentes:")
        for i, (name, profile) in enumerate(profiles.items(), 1):
            print(f"  {i}. {name} - {profile.get('description', 'Sem descrição')}")
        print()
    
    print("Opções:")
    print("1. ➕ Criar novo perfil")
    if profiles:
        print("2. ✏️  Editar perfil existente")
        print("3. 🗑️  Excluir perfil")
    print("0. ↩️  Voltar ao menu anterior")
    
    choice = input("Escolha uma opção: ").strip()
    
    if choice == "1":
        return _create_new_profile()
    elif choice == "2" and profiles:
        return _edit_existing_profile()
    elif choice == "3" and profiles:
        _delete_profile()
        return _create_or_edit_profile()
    elif choice == "0":
        return choose_mode_and_params()
    else:
        print("⚠️ Opção inválida.")
        return _create_or_edit_profile()

def _create_new_profile():
    """Cria um novo perfil"""
    print("\n➕ CRIAR NOVO PERFIL")
    print("-" * 25)
    
    while True:
        profile_name = input("📝 Nome do perfil: ").strip()
        if profile_name:
            profiles = Config.load_profiles()
            if profile_name in profiles:
                overwrite = input(f"⚠️ Perfil '{profile_name}' já existe. Sobrescrever? (s/n): ").strip().lower()
                if overwrite == 's':
                    break
            else:
                break
        else:
            print("❌ Nome não pode estar vazio.")
    
    description = input("📄 Descrição do perfil (opcional): ").strip()
    
    print(f"\n⚙️ Configurando perfil '{profile_name}':")
    
    model = _select_model()
    beam_size = _select_beam_size()
    best_of = _select_best_of()
    temperature = _select_temperature()
    
    params = {
        "model": model,
        "beam_size": beam_size,
        "best_of": best_of,
        "temperature": temperature,
    }
    
    Config.save_profile(profile_name, params, description)
    
    print(f"\n✅ Perfil '{profile_name}' salvo com sucesso!")
    
    execute_now = input("🚀 Executar transcrição com este perfil agora? (s/n): ").strip().lower()
    if execute_now == 's':
        return params
    else:
        return choose_mode_and_params()

def _edit_existing_profile():
    """Edita um perfil existente"""
    profiles = Config.load_profiles()
    
    print("\n✏️ EDITAR PERFIL EXISTENTE")
    print("-" * 30)
    
    profile_names = list(profiles.keys())
    for i, name in enumerate(profile_names, 1):
        profile = profiles[name]
        print(f"{i}. {name}")
        print(f"   📊 Modelo: {profile['model']}, Beam: {profile['beam_size']}")
        print(f"   📝 {profile.get('description', 'Sem descrição')}")
    
    try:
        choice = int(input(f"\nEscolha o perfil para editar (1-{len(profile_names)}): "))
        if 1 <= choice <= len(profile_names):
            profile_name = profile_names[choice - 1]
            current_profile = profiles[profile_name]
            
            print(f"\n🔧 Editando perfil: {profile_name}")
            print("(Pressione ENTER para manter valor atual)")
            
            new_description = input(f"📄 Descrição [{current_profile.get('description', '')}]: ").strip()
            if not new_description:
                new_description = current_profile.get('description', '')
            
            print(f"\n📦 Modelo atual: {current_profile['model']}")
            model = _select_model_with_current(current_profile['model'])
            
            print(f"\n🎯 Beam size atual: {current_profile['beam_size']}")
            beam_size = _select_beam_size_with_current(current_profile['beam_size'])
            
            print(f"\n🎯 Best of atual: {current_profile['best_of']}")
            best_of = _select_best_of_with_current(current_profile['best_of'])
            
            print(f"\n🌡️ Temperature atual: {current_profile['temperature']}")
            temperature = _select_temperature_with_current(current_profile['temperature'])
            
            params = {
                "model": model,
                "beam_size": beam_size,
                "best_of": best_of,
                "temperature": temperature,
            }
            
            Config.save_profile(profile_name, params, new_description)
            print(f"\n✅ Perfil '{profile_name}' atualizado com sucesso!")
            
            execute_now = input("🚀 Executar transcrição com este perfil agora? (s/n): ").strip().lower()
            if execute_now == 's':
                return params
            else:
                return choose_mode_and_params()
        else:
            print("❌ Escolha inválida.")
            return _edit_existing_profile()
    except ValueError:
        print("❌ Entrada inválida.")
        return _edit_existing_profile()

def _delete_profile():
    """Exclui um perfil"""
    profiles = Config.load_profiles()
    
    print("\n🗑️ EXCLUIR PERFIL")
    print("-" * 20)
    
    profile_names = list(profiles.keys())
    for i, name in enumerate(profile_names, 1):
        print(f"{i}. {name}")
    
    try:
        choice = int(input(f"\nEscolha o perfil para excluir (1-{len(profile_names)}): "))
        if 1 <= choice <= len(profile_names):
            profile_name = profile_names[choice - 1]
            confirm = input(f"⚠️ Tem certeza que deseja excluir '{profile_name}'? (s/n): ").strip().lower()
            if confirm == 's':
                Config.delete_profile(profile_name)
                print(f"✅ Perfil '{profile_name}' excluído com sucesso!")
            else:
                print("❌ Exclusão cancelada.")
        else:
            print("❌ Escolha inválida.")
    except ValueError:
        print("❌ Entrada inválida.")

def _execute_with_profile():
    """Executa transcrição usando um perfil salvo"""
    profiles = Config.load_profiles()
    
    if not profiles:
        print("\n❌ Nenhum perfil encontrado!")
        print("💡 Crie um perfil primeiro (opção 3).")
        input("Pressione ENTER para continuar...")
        return choose_mode_and_params()
    
    print("\n🎯 EXECUTAR COM PERFIL")
    print("=" * 30)
    
    profile_names = list(profiles.keys())
    for i, name in enumerate(profile_names, 1):
        profile = profiles[name]
        print(f"{i}. 📋 {name}")
        print(f"   📊 Modelo: {profile['model']}")
        print(f"   ⚙️ Beam: {profile['beam_size']}, Best: {profile['best_of']}, Temp: {profile['temperature']}")
        print(f"   📝 {profile.get('description', 'Sem descrição')}")
        print()
    
    try:
        choice = int(input(f"Escolha o perfil (1-{len(profile_names)}): "))
        if 1 <= choice <= len(profile_names):
            profile_name = profile_names[choice - 1]
            selected_profile = profiles[profile_name]
            
            print(f"\n✅ Perfil selecionado: {profile_name}")
            print(f"📊 Configurações: {selected_profile['model']} | Beam: {selected_profile['beam_size']} | Best: {selected_profile['best_of']}")
            
            return {
                "model": selected_profile["model"],
                "beam_size": selected_profile["beam_size"],
                "best_of": selected_profile["best_of"],
                "temperature": selected_profile["temperature"],
                "profile_name": profile_name
            }
        else:
            print("❌ Escolha inválida.")
            return _execute_with_profile()
    except ValueError:
        print("❌ Entrada inválida.")
        return _execute_with_profile()

def _select_model_with_current(current_model):
    """Seleção de modelo mostrando valor atual"""
    print(f"Modelos disponíveis: {', '.join(Config.AVAILABLE_MODELS)}")
    model = input(f"Novo modelo [atual: {current_model}]: ").strip().lower()
    
    if not model:
        return current_model
    elif model in Config.AVAILABLE_MODELS:
        return model
    else:
        print("⚠️ Modelo inválido. Mantendo atual.")
        return current_model

def _select_beam_size_with_current(current_beam):
    """Seleção de beam_size mostrando valor atual"""
    beam_size = input(f"Beam size (1, 5 ou 10) [atual: {current_beam}]: ").strip()
    
    if not beam_size:
        return current_beam
    elif beam_size in ["1", "5", "10"]:
        return int(beam_size)
    else:
        print("⚠️ Valor inválido. Mantendo atual.")
        return current_beam

def _select_best_of_with_current(current_best):
    """Seleção de best_of mostrando valor atual"""
    best_of = input(f"Best of (1, 3 ou 5) [atual: {current_best}]: ").strip()
    
    if not best_of:
        return current_best
    elif best_of in ["1", "3", "5"]:
        return int(best_of)
    else:
        print("⚠️ Valor inválido. Mantendo atual.")
        return current_best

def _select_temperature_with_current(current_temp):
    """Seleção de temperatura mostrando valor atual"""
    temperature = input(f"Temperature (0.0 a 1.0) [atual: {current_temp}]: ").strip()
    
    if not temperature:
        return current_temp
    
    try:
        temp = float(temperature)
        if 0.0 <= temp <= 1.0:
            return temp
        else:
            print("⚠️ Valor fora do intervalo. Mantendo atual.")
            return current_temp
    except:
        print("⚠️ Valor inválido. Mantendo atual.")
        return current_temp

def _select_model():
    """Seleção do modelo Whisper"""
    print(f"\n📦 Modelos disponíveis:")
    print(f" {', '.join(Config.AVAILABLE_MODELS)}")
    model = input("Digite o nome do modelo desejado: ").strip().lower()
    
    if model not in Config.AVAILABLE_MODELS:
        print("⚠️ Modelo inválido. Usando 'base'.")
        model = "base"
    
    return model

def _select_beam_size():
    """Seleção do beam_size"""
    print("""
🎯 beam_size:
 - Controla o número de hipóteses consideradas pelo modelo na decodificação.
 - Valores baixos (ex: 1): transcrição mais rápida, menos precisa.
 - Valores altos (ex: 5, 10): transcrição mais lenta, mais precisa.
 - Recomendo 5 para bom equilíbrio.

Digite o valor de beam_size (1, 5 ou 10):""")
    beam_size = input().strip()
    
    if beam_size not in ["1", "5", "10"]:
        print("⚠️ Valor inválido. Usando 1.")
        return 1
    
    return int(beam_size)

def _select_best_of():
    """Seleção do best_of"""
    print("""
🎯 best_of:
 - Quantas transcrições alternativas o modelo gera para escolher a melhor.
 - 1: gera uma única transcrição.
 - 3 ou 5: gera múltiplas e escolhe a com maior confiança.
 - Aumentar melhora a precisão, porém aumenta o tempo.

Digite o valor de best_of (1, 3 ou 5):""")
    best_of = input().strip()
    
    if best_of not in ["1", "3", "5"]:
        print("⚠️ Valor inválido. Usando 1.")
        return 1
    
    return int(best_of)

def _select_temperature():
    """Seleção da temperatura"""
    print("""
🌡️ Temperatura:
 - Controla a aleatoriedade na geração do texto.
 - 0.0: saída mais determinística e precisa (ideal para transcrição).
 - Próximo de 1.0: saída mais criativa/variada (não recomendada para transcrição).
 - Use valores baixos para melhor fidelidade.

Digite o valor da temperatura (0.0 a 1.0):""")
    try:
        temperature = float(input().strip())
        if not 0.0 <= temperature <= 1.0:
            raise ValueError
        return temperature
    except:
        print("⚠️ Valor inválido. Usando 0.0")
        return 0.0