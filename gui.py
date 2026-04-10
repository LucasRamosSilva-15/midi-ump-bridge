import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLabel
from PyQt6.QtCore import QThread, pyqtSignal
from midi_io import select_midi_input
from converter import midi1_to_midi2_velocity, midi1_to_midi2_pitch, midi1_to_midi2_cc
from ump import create_midi2_note_on, create_midi2_note_off, create_midi2_pitch_bend, create_midi2_control_change

class MidiWorker(QThread):
    message_received = pyqtSignal(str)

    def __init__(self, port):
        super().__init__()
        self.port = port

    def run(self):
        for msg in self.port:
            ump_msg = None
            display_text = ""

            if msg.type == 'note_on' and msg.velocity > 0:
                v2 = midi1_to_midi2_velocity(msg.velocity)
                ump_msg = create_midi2_note_on(msg.note, v2, msg.channel)
                display_text = f"[NOTE ON] Note: {msg.note} | Vel: {v2}"
            
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                ump_msg = create_midi2_note_off(msg.note, 0, msg.channel)
                display_text = f"[NOTE OFF] Note: {msg.note}"

            elif msg.type == 'pitchwheel':
                p32 = midi1_to_midi2_pitch(msg.pitch)
                ump_msg = create_midi2_pitch_bend(p32, msg.channel)
                display_text = f"[PITCH] Value: {p32}"

            elif msg.type == 'control_change':
                c32 = midi1_to_midi2_cc(msg.value)
                ump_msg = create_midi2_control_change(msg.control, c32, msg.channel)
                display_text = f"[CC] Control: {msg.control} | Value: {c32}"

            if ump_msg:
                full_log = f"{display_text}\nUMP HEX: {hex(ump_msg.ump64)}\n" + "-"*30
                self.message_received.emit(full_log)

class MainWindow(QMainWindow):
    def __init__(self, port):
        super().__init__()
        self.setWindowTitle("Tradutor MIDI 1.0 para MIDI 2.0 UMP")
        self.setMinimumSize(500, 400)

        self.layout = QVBoxLayout()
        self.label = QLabel(f"Conectado em: {port.name}")
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.log_area)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.worker = MidiWorker(port)
        self.worker.message_received.connect(self.update_log)
        self.worker.start()

    def update_log(self, text):
        self.log_area.append(text)

if __name__ == "__main__":
    port = select_midi_input()
    if port:
        app = QApplication(sys.argv)
        window = MainWindow(port)
        window.show()
        sys.exit(app.exec())