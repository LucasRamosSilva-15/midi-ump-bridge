def create_midi2_note_on(note, velocity16, channel=0, group=0):
    # ===== Word 1 =====
    # MIDI 2.0 UMP para Note On tem um formato específico, onde o Message Type (MT) é 0x4 para Channel Voice Messages, e o Status para Note On é 0x9.
    mt = 0x4          # MIDI 2.0 Channel Voice
    status = 0x9      # Note On
    # O canal é um valor de 4 bits (0-15) e o grupo também é um valor de 4 bits (0-15). Ambos são posicionados em Word 1.
    word1 = (
        (mt << 28) |
        (group << 24) |
        (status << 20) |
        (channel << 16)
    )

    # ===== Word 2 =====
    # Word 2 para Note On inclui a nota (7 bits), um campo de tipo de atributo (8 bits, que pode ser usado para coisas como aftertouch ou outros atributos, mas aqui vamos deixar como 0) e a velocity (16 bits).
    attribute_type = 0x00  # padrão (sem atributo extra)
    # A nota é um valor de 7 bits (0-127), e a velocity é um valor de 16 bits (0-65535). Ambos são posicionados em Word 2.
    word2 = (
        (note << 24) |
        (attribute_type << 16) |
        (velocity16 & 0xFFFF)
    )

    return word1, word2
def create_midi2_note_off(note, velocity16=0, channel=0, group=0):
    # A estrutura de Word 1 para Note Off é similar ao Note On, mas o Status é diferente (0x8 para Note Off).
    mt = 0x4
    status = 0x8  # Note Off
    # O canal e o grupo são os mesmos, então podemos usar a mesma lógica para construir Word 1.
    word1 = (mt << 28) | (group << 24) | (status << 20) | (channel << 16)
    # Para Word 2, a nota e a velocity são usadas da mesma forma, mas o campo de tipo de atributo ainda é 0 para simplificar.
    attribute_type = 0x00
    # A nota é um valor de 7 bits (0-127), e a velocity é um valor de 16 bits (0-65535). Ambos são posicionados em Word 2.
    word2 = (
        (note << 24) |
        (attribute_type << 16) |
        (velocity16 & 0xFFFF)
    )

    return word1, word2

def create_midi2_pitch_bend(pitch32, channel=0, group=0):
    mt = 0x4
    status = 0xE  # Pitch Bend

    word1 = (
        (mt << 28) |
        (group << 24) |
        (status << 20) |
        (channel << 16)
    )

    word2 = pitch32 & 0xFFFFFFFF

    return word1, word2

def decode_ump(ump64):
    # Para decodificar a mensagem UMP de 64 bits, precisamos extrair os dois words de 32 bits e depois interpretar os campos de acordo com o formato do MIDI 2.0.
    word1 = (ump64 >> 32) & 0xFFFFFFFF
    word2 = ump64 & 0xFFFFFFFF
    # A estrutura de Word 1 para mensagens de voz MIDI 2.0 inclui o Message Type (MT), Group, Status e Channel. Word 2 inclui a nota, tipo de atributo e velocity.
    mt = (word1 >> 28) & 0xF
    group = (word1 >> 24) & 0xF
    status = (word1 >> 20) & 0xF
    channel = (word1 >> 16) & 0xF
    # Para Word 2, a nota é um valor de 7 bits (0-127) e a velocity é um valor de 16 bits (0-65535). O campo de tipo de atributo é ignorado aqui, mas poderia ser extraído se necessário.
    note = (word2 >> 24) & 0xFF
    velocity = word2 & 0xFFFF
    # Imprime os campos decodificados para verificar se a mensagem foi interpretada corretamente.
    print(f"MT: {mt} | Group: {group} | Status: {status} | Channel: {channel}")
    print(f"Note: {note} | Velocity: {velocity}")