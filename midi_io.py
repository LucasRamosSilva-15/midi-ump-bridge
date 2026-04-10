import mido

def select_midi_input():
    inputs = mido.get_input_names()
    if not inputs: return None
    
    print("\n--- Entradas Disponíveis ---")
    for i, name in enumerate(inputs):
        print(f"{i}: {name}")
    
    try:
        choice = int(input("Escolha o número da porta: "))
        return mido.open_input(inputs[choice])
    except (ValueError, IndexError):
        print("Seleção inválida.")
        return None