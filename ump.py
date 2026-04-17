class UMPMessage:
    def __init__(self, word1, word2=0):
        self.word1 = word1
        self.word2 = word2

    @property
    def ump64(self):
        return (self.word1 << 32) | self.word2

    def analyze(self):
        mt = (self.word1 >> 28) & 0xF
        status = (self.word1 >> 20) & 0xF
        channel = (self.word1 >> 16) & 0xF
        
        data = {
            "channel": channel,
            "raw_w1": f"0x{self.word1:08X}",
            "raw_w2": f"0x{self.word2:08X}"
        }
        
        if mt == 4:
            if status == 0x9:
                data["type"] = "Note On"
                data["target"] = f"Nota {((self.word2 >> 24) & 0xFF)}"
                data["value"] = f"Vel: {self.word2 & 0xFFFF}"
            elif status == 0x8:
                data["type"] = "Note Off"
                data["target"] = f"Nota {((self.word2 >> 24) & 0xFF)}"
                data["value"] = f"Vel: {self.word2 & 0xFFFF}"
            elif status == 0xE:
                data["type"] = "Pitch Bend"
                data["target"] = "-"
                data["value"] = f"Val: {self.word2 & 0xFFFFFFFF}"
            elif status == 0xB: # NOVO: Decodificador de Control Change
                data["type"] = "Control Change"
                idx = (self.word1 >> 8) & 0x7F
                data["target"] = f"CC {idx}"
                data["value"] = f"Val: {self.word2 & 0xFFFFFFFF}"
            elif status == 0xA:
                data["type"] = "Per-Note Ctrl"
                nota = (self.word1 >> 8) & 0xFF
                idx = self.word1 & 0xFF
                data["target"] = f"Nota {nota} (Idx {idx})"
                data["value"] = f"Val: {self.word2 & 0xFFFFFFFF}"
            else:
                data["type"] = f"Desconhecido (0x{status:X})"
                data["target"] = "-"
                data["value"] = "-"
        else:
            data["type"] = f"MT Desconhecido ({mt})"
            data["target"] = "-"
            data["value"] = "-"
            
        return data

def create_midi2_note_on(note, vel16, channel=0, group=0):
    word1 = (0x4 << 28) | (group << 24) | (0x9 << 20) | (channel << 16)
    word2 = (note << 24) | vel16
    return UMPMessage(word1, word2)

def create_midi2_note_off(note, vel16, channel=0, group=0):
    word1 = (0x4 << 28) | (group << 24) | (0x8 << 20) | (channel << 16)
    word2 = (note << 24) | vel16
    return UMPMessage(word1, word2)

def create_midi2_pitch_bend(pitch32, channel=0, group=0):
    word1 = (0x4 << 28) | (group << 24) | (0xE << 20) | (channel << 16)
    return UMPMessage(word1, pitch32)

def create_midi2_control_change(index, val32, channel=0, group=0):
    word1 = (0x4 << 28) | (group << 24) | (0xB << 20) | (channel << 16) | (index << 8)
    return UMPMessage(word1, val32)

def create_midi2_per_note_controller(note, index, val32, channel=0, group=0):
    word1 = (0x4 << 28) | (group << 24) | (0xA << 20) | (channel << 16) | (note << 8) | index
    return UMPMessage(word1, val32)