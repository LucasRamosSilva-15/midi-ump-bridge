def create_midi2_note_on(note, velocity16, channel=0, group=0):
    # ===== Word 1 =====
    mt = 0x4          # MIDI 2.0 Channel Voice
    status = 0x9      # Note On

    word1 = (
        (mt << 28) |
        (group << 24) |
        (status << 20) |
        (channel << 16)
    )

    # ===== Word 2 =====
    attribute_type = 0x00  # padrão (sem atributo extra)

    word2 = (
        (note << 24) |
        (attribute_type << 16) |
        (velocity16 & 0xFFFF)
    )

    return word1, word2
def create_midi2_note_off(note, velocity16=0, channel=0, group=0):
    mt = 0x4
    status = 0x8  # Note Off

    word1 = (mt << 28) | (group << 24) | (status << 20) | (channel << 16)

    attribute_type = 0x00

    word2 = (
        (note << 24) |
        (attribute_type << 16) |
        (velocity16 & 0xFFFF)
    )

    return word1, word2
def decode_ump(ump64):
    word1 = (ump64 >> 32) & 0xFFFFFFFF
    word2 = ump64 & 0xFFFFFFFF

    mt = (word1 >> 28) & 0xF
    group = (word1 >> 24) & 0xF
    status = (word1 >> 20) & 0xF
    channel = (word1 >> 16) & 0xF

    note = (word2 >> 24) & 0xFF
    velocity = word2 & 0xFFFF

    print(f"MT: {mt} | Group: {group} | Status: {status} | Channel: {channel}")
    print(f"Note: {note} | Velocity: {velocity}")