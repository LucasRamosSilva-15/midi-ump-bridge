def midi1_to_midi2_velocity(v: int) -> int:
    return int((v / 127) * 65535)

def midi1_to_midi2_pitch(pitch14: int) -> int:
    pitch14_unsigned = pitch14 + 8192
    return pitch14_unsigned << 18

def midi1_to_midi2_32bit(value7: int) -> int:
    return int((value7 / 127) * 0xFFFFFFFF)