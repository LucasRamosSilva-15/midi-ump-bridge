from converter import midi1_to_midi2_pitch
from ump import create_midi2_pitch_bend, decode_ump
import mido
def test_pitch_bend():
    test_msg = mido.Message('pitchwheel', pitch=2000)

    pitch32 = midi1_to_midi2_pitch(test_msg.pitch)

    ump_msg = create_midi2_pitch_bend(pitch32, channel=0)

    print(f"Campo de pitch\n")
    print(f"[PITCH BEND] Pitch14: {test_msg.pitch} → Pitch32: {pitch32}")
    print(f" PITCH BEND UMP HEX: {hex(ump_msg.ump64)}")
    print("Decodificando UMP...")
    ump_msg.display()