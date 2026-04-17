from converter import midi1_to_midi2_pitch
from ump import create_midi2_pitch_bend

def test_pitch_bend():
    print("\n--- Iniciando Teste de Conversão (Centro Perfeito) ---")
    val_midi1 = 0
    p32 = midi1_to_midi2_pitch(val_midi1)
    ump = create_midi2_pitch_bend(p32)
    
    print(f"Entrada Mido: {val_midi1} (14-bit)")
    print(f"Saída UMP: {p32} (32-bit)")
    print(f"UMP HEX (Espera-se final 80000000): {hex(ump.ump64)}")