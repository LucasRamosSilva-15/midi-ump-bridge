# 🎹 Conversor e Analisador MIDI 1.0 para MIDI 2.0 (UMP)

Bem-vindo ao repositório do meu Trabalho de Conclusão de Curso (TCC) desenvolvido no **Instituto Federal da Paraíba (IFPB)**. 

Este projeto é uma prova de conceito (PoC) em software que captura mensagens de hardware baseadas no protocolo MIDI 1.0 (1983), realiza a conversão matemática de suas resoluções e encapsula os dados no novo padrão de alta definição **MIDI 2.0 Universal MIDI Packet (UMP)** de 64-bits.

**🌟 Assista à demonstração do sistema em tempo real: [Link para o Vídeo no YouTube/Drive]**

---

## 📋 Sumário

- [🎯 Sobre o Projeto](#-sobre-o-projeto)
- [🚀 Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [📸 Demonstração Visual](#-demonstração-visual)
- [🛠️ Arquitetura e Estrutura do Projeto](#️-arquitetura-e-estrutura-do-projeto)
- [💻 Guia de Execução (Windows 11)](#-guia-de-execução-windows-11)
- [🧪 Testes de Validação](#-testes-de-validação)
- [🎹 Equipamento de Teste](#-equipamento-de-teste)
- [📝 Padrão de Commits](#-padrão-de-commits)
- [👤 Autor](#-autor)

---

## 🎯 Sobre o Projeto

### O Desafio
O protocolo MIDI 1.0 domina a indústria musical há mais de 40 anos operando com limitações drásticas de resolução (geralmente 7 bits, permitindo apenas valores de 0 a 127). O futuro pertence ao **MIDI 2.0**, que traz resoluções de 16 e 32 bits, eliminando o "efeito escada" (*zipper noise*) em modulações de áudio. 

### A Solução
Este projeto implementa na prática a diretriz de retrocompatibilidade da *MIDI Association*. O software atua como um "tradutor" em tempo real:
1. **Escuta** sinais antigos.
2. **Converte** matematicamente (ex: Pitch Bend de 14-bit para 32-bit usando *bit shifting*).
3. **Encapsula** em pacotes UMP (Universal MIDI Packet).
4. **Decodifica** o pacote hexadecimal para exibição didática na interface gráfica.

---

## 🚀 Tecnologias Utilizadas

- **[Python 3.10+](https://www.python.org/)**: Linguagem base do projeto.
- **[PyQt6](https://riverbankcomputing.com/software/pyqt/)**: Framework para a construção da Interface Gráfica (GUI) reativa e uso de *Multithreading*.
- **[Mido](https://mido.readthedocs.io/) & [python-rtmidi](https://pypi.org/project/python-rtmidi/)**: Bibliotecas para interfaceamento e captura de portas MIDI (USB e Virtuais).
- **Matemática Computacional**: Operações *Bitwise* (Bit Shift, Máscaras Hexadecimais) para conversão e montagem de pacotes.

---

## 📸 Demonstração Visual

[Interface Principal]
https://github.com/LucasRamosSilva-15/programa-tcc-midi/blob/master/capturas/Captura%20de%20tela%202026-04-17%20154643.png

> *Interface gráfica processando eventos MIDI em tempo real, exibindo os dados originais (MIDI 1.0) lado a lado com os pacotes convertidos (UMP 64-bit).*

---

## 🛠️ Arquitetura e Estrutura do Projeto

O código foi modularizado aplicando o princípio de responsabilidade única (SRP) para facilitar a manutenção e avaliação acadêmica:
```text
/
├── main.py          # Ponto de entrada, inicialização e injeção de dependências
├── gui.py           # Interface gráfica PyQt6, tabelas e Threads de escuta
├── converter.py     # Núcleo matemático de conversão (7/14-bit → 16/32-bit)
├── ump.py           # Classes e fábricas para criação/decodificação de UMPs
├── midi_io.py       # Varredura e seleção segura de portas de hardware
├── teste_pitch.py   # Script de Prova de Conceito (PoC) e testes unitários
└── README.md        # Documentação do projeto
💻 Guia de Execução (Windows 11)
Para testar o projeto localmente (mesmo sem um teclado físico), siga o passo a passo de configuração do ambiente virtual:

1. Preparação do Ambiente
Bash
# Clone o repositório
git clone https://github.com/LucasRamosSilva-15/programa-tcc-midi.git

# Entre na pasta do projeto
cd programa-tcc-midi

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
venv\Scripts\activate

# Instale as dependências (requer Python instalado)
python -m pip install mido python-rtmidi PyQt6
2. Configurando o Teclado Virtual (Opcional)
Se você não possui um teclado MIDI físico conectado via USB:

Instale o loopMIDI, abra-o e crie uma porta chamada loopMIDI Port.

Instale o VMPK (Teclado de Piano MIDI Virtual).

No VMPK, vá em Edit > MIDI Connections e defina a saída (MIDI OUT) para a porta virtual criada.

3. Rodando o Analisador
Bash
python main.py
O terminal exibirá os dispositivos detectados. Digite o número da sua porta e pressione Enter. A interface gráfica será aberta e começará a escutar os eventos em tempo real.
```

🧪 Testes de Validação
O projeto inclui rotinas de validação baseadas nas especificações oficiais. Ao iniciar o main.py, o sistema perguntará se você deseja rodar o teste de unidade de Pitch Bend.

Este teste injeta o valor 0 (centro perfeito de repouso no MIDI 1.0) e valida se a matemática do converter.py e o encapsulador do ump.py geram exatamente o código Hexadecimal 0x80000000, conforme exigido pelo padrão UMP.

🎹 Equipamento de Teste
Durante o desenvolvimento deste TCC, o software foi homologado utilizando os seguintes hardwares/softwares:

Teclado físico: Yamaha PSR E383 (via USB-MIDI).

Controlador Virtual: VMPK (Virtual MIDI Piano Keyboard).

👤 Autor
Lucas Ramos Silva
Projeto desenvolvido como requisito para conclusão do curso técnico em informática no Instituto Federal da Paraíba (IFPB) 2026 - Campus Campina Grande.
