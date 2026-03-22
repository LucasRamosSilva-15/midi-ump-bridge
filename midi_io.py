# importa a biblioteca mido para lidar com MIDI
import mido

def choose_input():
    """
    Lista as entradas MIDI disponíveis, permite ao usuário escolher uma
    e retorna a porta MIDI selecionada.
    """

    # Obtém os nomes das entradas MIDI disponíveis
    inputs = mido.get_input_names()

    # Se não houver entradas, avisa o usuário
    if not inputs:
        print("No MIDI input devices found.")
        return None

    # Mostra as entradas disponíveis
    print("Available MIDI input devices:")
    for i, name in enumerate(inputs):
        print(f"{i}: {name}")

    # Solicita ao usuário a escolha da entrada
    choice = int(input("Escolha a entrada pelo número: "))

    # Verifica se a escolha é válida
    if 0 <= choice < len(inputs):
        # Abre e retorna a entrada MIDI selecionada
        return mido.open_input(inputs[choice])
    else:
        # Caso inválido
        print("Invalid choice.")
        return None