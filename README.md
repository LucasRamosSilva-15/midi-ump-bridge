# Projeto de TCC - Conversão MIDI 1.0 para MIDI 2.0 (UMP)

Este projeto tem como objetivo demonstrar, na prática, a conversão de mensagens do protocolo MIDI 1.0 (1983) para o formato MIDI 2.0 Universal MIDI Packet (UMP), introduzido em 2020.

O sistema captura mensagens MIDI em tempo real, realiza a conversão dos dados (como velocity e pitch bend) e gera as mensagens no formato UMP, permitindo a visualização e análise em hexadecimal.

## Objetivo

Implementar e demonstrar a lógica de conversão entre os padrões MIDI 1.0 e MIDI 2.0, mostrando:

- Diferenças de resolução (7 bits vs 16/32 bits)
- Estrutura das mensagens MIDI
- Representação em nível de bits
- Funcionamento do formato UMP

## Justificativa

Embora o padrão MIDI 2.0 já defina mecanismos de compatibilidade com MIDI 1.0, sua implementação prática não é trivial. Este projeto busca demonstrar esse processo de forma clara, servindo como ferramenta de estudo e análise do protocolo.

## Funcionalidades

- Leitura de mensagens MIDI em tempo real
- Conversão de velocity (MIDI 1 → MIDI 2)
- Conversão de pitch bend (14 bits → 32 bits)
- Geração de mensagens UMP
- Exibição em formato hexadecimal
- Decodificação das mensagens UMP

## Tecnologias utilizadas

- Python
- Biblioteca Mido
- PyQt6 para Interface Gráfica
  
## Equipamento utilizado

- Teclado Arranjador Yamaha PSR E383
- Virtual MIDI Piano Keyboard (VMPK) para testes virtuais

## Autor

- Lucas Ramos Silva