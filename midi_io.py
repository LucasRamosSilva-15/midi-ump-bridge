import mido

def select_midi_input():
    inputs = mido.get_input_names()

    if not inputs:
        print("No MIDI input devices found.")
        return None

    print("Available MIDI input devices:")
    for i, name in enumerate(inputs):
        print(f"{i}: {name}")

    choice = int(input("Escolha a entrada pelo número: "))

    if 0 <= choice < len(inputs):
        return mido.open_input(inputs[choice])
    else:
        print("Invalid choice.")
        return None