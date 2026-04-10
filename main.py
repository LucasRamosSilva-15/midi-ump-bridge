import sys
from PyQt6.QtWidgets import QApplication
from midi_io import select_midi_input
from gui import MainWindow
from teste_pitch import test_pitch_bend

def main():
    port = select_midi_input()
    if not port:
        print("Nenhum dispositivo selecionado. Saindo...")
        return

    print("Rodar teste de unidade? (s/n)")
    if input() == 's': test_pitch_bend()

    app = QApplication(sys.argv)
    win = MainWindow(port)
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()