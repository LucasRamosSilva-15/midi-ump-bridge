def midi1_to_midi2_velocity(v):
    # Converte uma velocidade MIDI 1.0 (0-127) para MIDI 2.0 (0-65535).
    return int((v / 127) * 65535)
def midi1_to_midi2_pitch(pitch14):
    """
    Converte pitch bend MIDI 1 (14 bits: -8192 a +8191)
    para MIDI 2 (32 bits: 0 a 4294967295)
    """

    # Normaliza de (-8192 a +8191) → (0 a 16383)
    pitch14_unsigned = pitch14 + 8192

    # Expande para 32 bits
    pitch32 = int((pitch14_unsigned / 16383) * 0xFFFFFFFF)

    return pitch32