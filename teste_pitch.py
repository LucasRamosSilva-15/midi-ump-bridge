from converter import midi1_to_midi2_pitch
from ump import create_midi2_pitch_bend, decode_ump
import mido
def test_pitch_bend():
    # Cria uma mensagem de pitch bend MIDI 1.0 com um valor específico (por exemplo, 2000).
    test_msg = mido.Message('pitchwheel', pitch=2000)

    # Converte o valor de pitch bend para MIDI 2.0 usando a função do converter.py.
    pitch32 = midi1_to_midi2_pitch(test_msg.pitch)

    # Cria a mensagem UMP de pitch bend usando a função do ump.py, passando o valor de pitch convertido e um canal (por exemplo, canal 0).
    ump_msg = create_midi2_pitch_bend(pitch32, channel=0)

    # Combina os dois words da mensagem UMP em um único valor de 64 bits para facilitar a exibição e o debug.
    ump64 = (ump_msg[0] << 32) | ump_msg[1]

    # Imprime as informações da mensagem MIDI original, o valor convertido e o valor hexadecimal da mensagem UMP, além de decodificar a mensagem UMP para mostrar seus componentes.
    print(f"Campo de pitch\n")
    print(f"[PITCH BEND] Pitch14: {test_msg.pitch} → Pitch32: {pitch32}")
    print(f"UMP HEX: {hex(ump64)}")
    print("Decodificando UMP...")
    decode_ump(ump64)