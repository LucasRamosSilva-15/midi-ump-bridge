from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QTableWidget, 
                             QTableWidgetItem, QProgressBar, QLabel, QHeaderView, QPushButton)
from PyQt6.QtCore import QThread, pyqtSignal
import converter
import ump

class MidiWorker(QThread):
    log_signal = pyqtSignal(dict)
    pitch_signal = pyqtSignal(int)

    def __init__(self, port):
        super().__init__()
        self.port = port
        self.last_note = 60 

    def run(self):
        for msg in self.port:
            ump_msg = None 
            original_str = "-"
            
            if msg.type == 'note_on' and msg.velocity > 0:
                self.last_note = msg.note
                original_str = f"Vel: {msg.velocity}"
                v2 = converter.midi1_to_midi2_velocity(msg.velocity)
                ump_msg = ump.create_midi2_note_on(msg.note, v2, msg.channel)
                
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                original_str = f"Vel: {msg.velocity}"
                v2 = converter.midi1_to_midi2_velocity(msg.velocity)
                ump_msg = ump.create_midi2_note_off(msg.note, v2, msg.channel)
                
            elif msg.type == 'pitchwheel':
                original_str = f"Pitch: {msg.pitch}"
                p32 = converter.midi1_to_midi2_pitch(msg.pitch)
                ump_msg = ump.create_midi2_pitch_bend(p32, msg.channel)
                self.pitch_signal.emit(int((p32 / 0xFFFFFFFF) * 100))

            elif msg.type == 'control_change':
                original_str = f"Val: {msg.value}"
                v32 = converter.midi1_to_midi2_32bit(msg.value)
                ump_msg = ump.create_midi2_control_change(msg.control, v32, msg.channel)

            if ump_msg:
                data = ump_msg.analyze()
                data["original"] = original_str
                self.log_signal.emit(data)


class MainWindow(QMainWindow):
    def __init__(self, port):
        super().__init__()
        self.setWindowTitle("Analisador MIDI 2.0 UMP - TCC IFPB")
        self.setMinimumSize(750, 450)
        
        layout = QVBoxLayout()
        
        self.table = QTableWidget(0, 6) 
        self.table.setHorizontalHeaderLabels([
            "Mensagem", "Ch", "Alvo", "Valor Original", "Valor Convertido", "Raw Words (UMP 64-bit)"
        ])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        
        self.bar = QProgressBar()
        
        self.btn_simular = QPushButton("Simular Pitch Bend (Teste de Software)")
        self.btn_simular.clicked.connect(self.simular_pitch_bend)
        
        layout.addWidget(QLabel(f"Hardware Conectado: {port.name}"))
        layout.addWidget(self.btn_simular)
        layout.addWidget(QLabel("Resolução Pitch Bend (32-bit):"))
        layout.addWidget(self.bar)
        layout.addWidget(QLabel("Analisador de Pacotes UMP em Tempo Real:"))
        layout.addWidget(self.table)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.worker = MidiWorker(port)
        self.worker.log_signal.connect(self.add_table_row)
        self.worker.pitch_signal.connect(self.bar.setValue)
        self.worker.start()

    def simular_pitch_bend(self):
        val_midi1 = 0
        p32 = converter.midi1_to_midi2_pitch(val_midi1)
        ump_msg = ump.create_midi2_pitch_bend(p32, 0)
        
        self.bar.setValue(int((p32 / 0xFFFFFFFF) * 100))
        
        data = ump_msg.analyze()
        data["original"] = f"Pitch: {val_midi1} (Simulado)"
        
        self.add_table_row(data)

    def add_table_row(self, data):
        row_pos = self.table.rowCount()
        self.table.insertRow(row_pos)
        
        self.table.setItem(row_pos, 0, QTableWidgetItem(data.get("type", "")))
        self.table.setItem(row_pos, 1, QTableWidgetItem(str(data.get("channel", ""))))
        self.table.setItem(row_pos, 2, QTableWidgetItem(data.get("target", "")))
        self.table.setItem(row_pos, 3, QTableWidgetItem(data.get("original", ""))) 
        self.table.setItem(row_pos, 4, QTableWidgetItem(data.get("value", "")))
        
        raw_words = f"{data.get('raw_w1', '')} | {data.get('raw_w2', '')}"
        self.table.setItem(row_pos, 5, QTableWidgetItem(raw_words))
        
        self.table.scrollToBottom()