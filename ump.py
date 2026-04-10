class UMPMessage:
    def __init__(self, word1, word2):
        self.word1 = word1
        self.word2 = word2

    @property
    def ump64(self):
        return (self.word1 << 32) | self.word2

    def decode(self):
        mt = (self.word1 >> 28) & 0xF
        group = (self.word1 >> 24) & 0xF
        status = (self.word1 >> 20) & 0xF
        channel = (self.word1 >> 16) & 0xF
        note = (self.word2 >> 24) & 0xFF
        velocity = self.word2 & 0xFFFF
        pitch = self.word2 & 0xFFFFFFFF
        index = (self.word2 >> 24) & 0xFF
        cc_value = self.word2 & 0xFFFFFFFF
        return mt, group, status, channel, note, velocity, pitch, index, cc_value

    def display(self):
        mt, group, status, channel, note, velocity, pitch, index, cc_value = self.decode()
        print(f"  [UMP 64-bit] HEX: {hex(self.ump64)}")
        
        if status == 0x9:
            print(f"  Decoded: Note On | Channel: {channel} | Note: {note} | Velocity: {velocity}")
        elif status == 0x8:
            print(f"  Decoded: Note Off | Channel: {channel} | Note: {note} | Velocity: {velocity}")
        elif status == 0xE:
            print(f"  Decoded: Pitch Bend | Channel: {channel} | Value: {pitch}")
        elif status == 0xB:
            print(f"  Decoded: Control Change | Index: {index} | Value: {cc_value}")

def create_midi2_note_on(note, velocity16, channel=0, group=0):
    mt = 0x4
    status = 0x9
    word1 = (mt << 28) | (group << 24) | (status << 20) | (channel << 16)
    
    attribute_type = 0x00
    word2 = (note << 24) | (attribute_type << 16) | (velocity16 & 0xFFFF)

    return UMPMessage(word1, word2)

def create_midi2_note_off(note, velocity16=0, channel=0, group=0):
    mt = 0x4
    status = 0x8
    word1 = (mt << 28) | (group << 24) | (status << 20) | (channel << 16)
    
    attribute_type = 0x00
    word2 = (note << 24) | (attribute_type << 16) | (velocity16 & 0xFFFF)

    return UMPMessage(word1, word2)

def create_midi2_pitch_bend(pitch32, channel=0, group=0):
    mt = 0x4
    status = 0xE
    word1 = (mt << 28) | (group << 24) | (status << 20) | (channel << 16)
    word2 = pitch32 & 0xFFFFFFFF

    return UMPMessage(word1, word2)

def create_midi2_control_change(index, value32, channel=0, group=0):
    mt = 0x4
    status = 0xB
    word1 = (mt << 28) | (group << 24) | (status << 20) | (channel << 16)
    word2 = value32 & 0xFFFFFFFF
    # Note: No MIDI 2.0 real, o index CC fica no word1, mas para manter a 
    # consistência com sua lógica de Note On, estamos usando o word2.
    return UMPMessage(word1, word2)

def decode_ump(ump64):
    word1 = (ump64 >> 32) & 0xFFFFFFFF
    word2 = ump64 & 0xFFFFFFFF
    mt = (word1 >> 28) & 0xF
    group = (word1 >> 24) & 0xF
    status = (word1 >> 20) & 0xF
    channel = (word1 >> 16) & 0xF
    note = (word2 >> 24) & 0xFF
    velocity = word2 & 0xFFFF
    pitch = word2 & 0xFFFFFFFF
    return mt, group, status, channel, note, velocity, pitch