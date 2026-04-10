from converter import midi1_to_midi2_velocity, midi1_to_midi2_pitch
from ump import create_midi2_note_on, create_midi2_note_off, create_midi2_pitch_bend
import sys
from PyQt6.QtWidgets import QApplication
from gui import MainWindow
from midi_io import select_midi_input
from teste_pitch import test_pitch_bend

port = select_midi_input()
if not port:
    exit()
def main():
    port = select_midi_input()
    if not port:
        sys.exit()

print("Deseja rodar o teste de Pitch Bend antes de iniciar? (s/n)")
if input().strip().lower() == 's':
    test_pitch_bend()
    print("Deseja rodar o teste de Pitch Bend no terminal antes de iniciar a interface? (s/n)")
    if input().strip().lower() == 's':
        test_pitch_bend()

print("Rodando... Pressione Ctrl+C para sair.")
    # Inicializa a aplicação gráfica
    app = QApplication(sys.argv)
    window = MainWindow(port)
    window.show()
    
    sys.exit(app.exec())

try:
    for msg in port:
        ump_msg = None
        
        if msg.type == 'note_on' and msg.velocity > 0:
            v2 = midi1_to_midi2_velocity(msg.velocity) & 0xFFFF
            ump_msg = create_midi2_note_on(msg.note & 0x7F, v2, msg.channel & 0x0F)
            print(f"[NOTE ON] Note: {msg.note} | Vel1: {msg.velocity} -> Vel2: {v2}")

        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            ump_msg = create_midi2_note_off(msg.note & 0x7F, 0, msg.channel & 0x0F)
            print(f"[NOTE OFF] Note: {msg.note}")

        elif msg.type == 'pitchwheel':
            pitch32 = midi1_to_midi2_pitch(msg.pitch)
            ump_msg = create_midi2_pitch_bend(pitch32, channel=msg.channel & 0x0F)
            print(f"[PITCH BEND] Pitch14: {msg.pitch} -> Pitch32: {pitch32}")

        if ump_msg:
            ump_msg.display()

except KeyboardInterrupt:
    print("\nEncerrando o programa...")
finally:
    if 'port' in locals() and port:
        port.close()
if __name__ == "__main__":
    main()
