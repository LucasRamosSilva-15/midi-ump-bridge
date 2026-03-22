# importa dos outros arquivos e as funções principais para rodar o programa. 
from converter import midi1_to_midi2_velocity
from ump import create_midi2_note_on, create_midi2_note_off, decode_ump
from midi_io import select_midi_input
# chama a função para escolher a entrada MIDI e depois fica mostrando as entradas recebidas 
port = select_midi_input()

print("Rodando... Pressione Ctrl+C para sair.")
""" Escutar continuamente todas as mensagens MIDI que chegam do dispositivo e processá-las uma a uma em tempo real,
    ficando em loop infinito até que o usuário decida parar o programa usando Ctrl+C. """
for msg in port:
    # começa a processar as mensagens MIDI recebidas, verificando o tipo de mensagem e convertendo para UMP conforme necessário
    if msg.type == 'note_on':
        # acontece que em MIDI 1.0, um Note On com velocity 0 é interpretado como Note Off, então verificamos isso primeiro
        if msg.velocity > 0:
            # NOTE ON
            v1 = msg.velocity # é o comando usado para receber a velocity da mensagem MIDI 1.0, que é um valor entre 0 e 127.
            v2 = midi1_to_midi2_velocity(v1) & 0xFFFF # converte a velocity para MIDI 2.0 usando a função do converter.py e garante que seja um valor de 16 bits (0-65535).
            note = msg.note & 0x7F # garante que a nota seja um valor de 7 bits (0-127), embora isso seja geralmente garantido pelo próprio mido.
            channel = msg.channel & 0x0F # garante que o canal seja um valor de 4 bits (0-15), embora isso também seja geralmente garantido pelo mido.

            ump_msg = create_midi2_note_on(note, v2, channel) # cria a mensagem UMP de Note On usando a função do ump.py, passando a nota, a velocity convertida e o canal.
            ump64 = (ump_msg[0] << 32) | ump_msg[1] # combina os dois words da mensagem UMP em um único valor de 64 bits para facilitar a exibição e o debug.
            # imprime as informações da mensagem MIDI original, a velocity convertida e o valor hexadecimal da mensagem UMP, além de decodificar a mensagem UMP para mostrar seus componentes.
            print(f"[NOTE ON] Note: {msg.note} | V1: {v1} → V2: {v2}")
            print(f"UMP HEX: {hex(ump64)}")
            decode_ump(ump64)

        else:
            # NOTE OFF (velocity 0)

            note = msg.note & 0x7F
            channel = msg.channel & 0x0F
            ump_msg = create_midi2_note_off(note, 0, channel=channel) # cria a mensagem UMP de Note Off usando a função do ump.py, passando a nota, velocity 0 e o canal.
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
        