""" importa dos outros arquivos e as funções principais para rodar o programa. """
from converter import midi1_to_midi2_velocity
from ump import create_midi2_note_on, create_midi2_note_off, decode_ump
from midi_io import choose_input
""" chama a função para escolher a entrada MIDI e depois fica mostrando as entradas recebidas"""
port = choose_input()

print("Rodando... Pressione Ctrl+C para sair.")

for msg in port:
    if msg.type == 'note_on':
        if msg.velocity > 0:
            # NOTE ON
            v1 = msg.velocity
            v2 = midi1_to_midi2_velocity(v1) & 0xFFFF
            note = msg.note & 0x7F
            channel = msg.channel & 0x0F

            ump_msg = create_midi2_note_on(note, v2, channel)
            ump64 = (ump_msg[0] << 32) | ump_msg[1]

            print(f"[NOTE ON] Note: {msg.note} | V1: {v1} → V2: {v2}")
            print(f"UMP HEX: {hex(ump64)}")
            decode_ump(ump64)

        else:
            # NOTE OFF (velocity 0)

            note = msg.note & 0x7F
            channel = msg.channel & 0x0F
            ump_msg = create_midi2_note_off(note, 0, channel=channel)
            ump64 = (ump_msg[0] << 32) | ump_msg[1]

            print(f"[NOTE OFF] Note: {msg.note}")
            print(f"UMP HEX: {hex(ump64)}")
            decode_ump(ump64)

    elif msg.type == 'note_off':
        # NOTE OFF real
        note = msg.note & 0x7F
        channel = msg.channel & 0x0F
        ump_msg = create_midi2_note_off(note, 0, channel=channel)
        ump64 = (ump_msg[0] << 32) | ump_msg[1]

        print(f"[NOTE OFF] Note: {msg.note}")
        print(f"UMP HEX: {hex(ump64)}")
        decode_ump(ump64)
        