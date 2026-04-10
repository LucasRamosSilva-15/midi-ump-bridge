def midi1_to_midi2_velocity(v):
    return int((v / 127) * 65535)

def midi1_to_midi2_pitch(pitch14):
    pitch14_unsigned = pitch14 + 8192
    pitch32 = int((pitch14_unsigned / 16383) * 0xFFFFFFFF)
    return pitch32

def midi1_to_midi2_cc(value7):
    return int((value7 / 127) * 0xFFFFFFFF)