def midi1_to_midi2_velocity(v):
    # Converte uma velocidade MIDI 1.0 (0-127) para MIDI 2.0 (0-65535).
    return int((v / 127) * 65535)
