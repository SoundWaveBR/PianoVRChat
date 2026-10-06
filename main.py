import os
# Esconde aquela mensagem chata de boas vindas que o pygame solta no terminal
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" 

import mido
# A LINHA MÁGICA: Avisa o mido para usar o pygame em vez do rtmidi
mido.set_backend('mido.backends.pygame')

from pythonosc import udp_client
import time

# --- CONFIGURAÇÕES PRINCIPAIS ---
NOME_PORTA_MIDI = "Piano Chat"  # Nome exato da porta no loopMIDI
IP_VRCHAT = "127.0.0.1"         # ID LOCALHOST
PORTA_OSC_VRCHAT = 9000         # Porta padrão do VRChat
ATRASO_ATUALIZACAO = 0.22        # Intervalo para não dar spam (em segundos)
PONTO_DIVISAO_MIDI = 62         # Mi Central (E4) - Divide Mão Esq e Mão Dir

# NOTAS MÚSICAIS
# Motor harmónico de intervalos (em semitons) Master / Jazz
TIPOS_ACORDE = {
    # --- TRÍADES ---
    (0, 4, 7): "Maior",
    (0, 3, 7): "Menor",
    (0, 3, 6): "Dim",       
    (0, 4, 8): "Aum",       
    
    # --- ACORDES SUSPENSOS ---
    (0, 5, 7): "sus4",
    (0, 2, 7): "sus2",
    
    # --- TÉTRADES (Sétimas) ---
    (0, 4, 7, 10): "7",             # Dominante
    (0, 4, 7, 11): "7M",            # Maior com 7ª Maior
    (0, 3, 7, 10): "m7",            # Menor com 7ª
    (0, 3, 7, 11): "m(7M)",         # Menor com 7ª Maior
    (0, 3, 6, 10): "m7b5",          # Meio-diminuto
    (0, 3, 6, 9): "dim7",           # Diminuto completo
    (0, 4, 8, 10): "7#5",           # Aumentado com 7ª
    (0, 4, 6, 10): "7b5",           # Dominante com 5ª diminuta
    (0, 5, 7, 10): "7sus4",         # Sétima com 4ª suspensa

    # --- SEXTAS ---
    (0, 4, 7, 9): "6",              # Maior com 6ª
    (0, 3, 7, 9): "m6",             # Menor com 6ª

    # --- NONAS (Intervalo 2) ---
    (0, 2, 4, 7): "add9",           # Adicionada de 9ª
    (0, 2, 3, 7): "m(add9)",        # Menor adicionada de 9ª
    (0, 2, 4, 7, 10): "9",          # Dominante com 9ª
    (0, 2, 3, 7, 10): "m9",         # Menor com 9ª
    (0, 2, 4, 7, 11): "7M(9)",      # Maior com 7ªM e 9ª
    (0, 2, 4, 9): "6/9",            # 6/9 sem a quinta
    (0, 2, 4, 7, 9): "6/9",         # 6/9 com a quinta
    (0, 2, 3, 7, 9): "m6/9",        # Menor 6/9
    
    # --- NONAS ALTERADAS ---
    (0, 1, 4, 7, 10): "7(b9)",      # Dominante com 9ª bemol
    (0, 3, 4, 7, 10): "7(#9)",      # Dominante com 9ª sustenida (acorde Hendrix)

    # --- DÉCIMAS PRIMEIRAS (Intervalo 5) ---
    (0, 2, 4, 5, 7, 10): "11",      # Dominante com 11ª e 9ª
    (0, 2, 3, 5, 7, 10): "m11",     # Menor com 11ª
    (0, 4, 5, 7, 10): "7(11)",      # Sétima e 11ª (sem a 9ª)
    (0, 3, 5, 7, 10): "m7(11)",     # Menor 7ª e 11ª
    (0, 4, 6, 7, 10): "7(#11)",     # Lídio dominante (11ª aumentada)

    # --- DÉCIMAS TERCEIRAS (Intervalo 9) ---
    (0, 4, 7, 9, 10): "13",         # Dominante com 13ª (sem a 9ª)
    (0, 2, 4, 7, 9, 10): "13",      # Dominante com 13ª completa
    (0, 3, 7, 9, 10): "m13",        # Menor com 13ª
    (0, 2, 3, 7, 9, 10): "m13",     # Menor com 13ª completa
    (0, 4, 7, 8, 10): "7(b13)",     # Dominante com 13ª menor
}


def numero_para_nota(numero_midi):
    oitava = (numero_midi // 12) - 1
    nota = NOTAS_PT[numero_midi % 12]
    return f"{nota}{oitava}"

def identificar_acorde(notas_midi):
    if not notas_midi:
        return ""
    
    notas_unicas = list(set([n % 12 for n in notas_midi]))
    
    if len(notas_unicas) < 3:
        return "-".join([NOTAS_PT[n] for n in sorted(notas_unicas)])

    for raiz in notas_unicas:
        intervalos = tuple(sorted([(n - raiz) % 12 for n in notas_unicas]))
        if intervalos in TIPOS_ACORDE:
            nome_raiz = NOTAS_PT[raiz]
            tipo = TIPOS_ACORDE[intervalos]
            return f"{nome_raiz} {tipo}"
            
    return "-".join([NOTAS_PT[n] for n in sorted(notas_unicas)])

def iniciar():
    cliente_osc = udp_client.SimpleUDPClient(IP_VRCHAT, PORTA_OSC_VRCHAT)
    portas_disponiveis = mido.get_input_names()
    
    porta_alvo = next((p for p in portas_disponiveis if NOME_PORTA_MIDI.lower() in p.lower()), None)
# Avisos de erros
    if not porta_alvo:
        print(f"❌ Erro: Porta '{NOME_PORTA_MIDI}' não encontrada.")
        print(f"Portas ativas no momento: {portas_disponiveis}")
        print("Você esqueceu de abrir o loopMIDI?")
        return

    print(f"✅ Conectado com sucesso na porta: {porta_alvo}")
    print("✅ Motor de Acordes e Divisão de Mãos: ATIVADOS")
    print("✅ Modo MagicChatbox (Silêncio Automático): ATIVADO")
    print("🎹 Aguardando você tocar... (Pressione Ctrl+C no terminal para sair)")

    notas_esq = set()
    notas_dir = set()
    ultimo_envio = 0
    enviou_silencio = True

    with mido.open_input(porta_alvo) as porta_entrada:
        for mensagem in porta_entrada:
            teve_mudanca = False

            if getattr(mensagem, 'type', None) == 'note_on' and getattr(mensagem, 'velocity', 0) > 0:
                if mensagem.note < PONTO_DIVISAO_MIDI:
                    notas_esq.add(mensagem.note)
                else:
                    notas_dir.add(mensagem.note)
                teve_mudanca = True
            
            elif getattr(mensagem, 'type', None) == 'note_off' or (getattr(mensagem, 'type', None) == 'note_on' and getattr(mensagem, 'velocity', 1) == 0):
                if mensagem.note in notas_esq:
                    notas_esq.remove(mensagem.note)
                    teve_mudanca = True
                if mensagem.note in notas_dir:
                    notas_dir.remove(mensagem.note)
                    teve_mudanca = True

            tempo_atual = time.time()
            
            if teve_mudanca and (tempo_atual - ultimo_envio) >= ATRASO_ATUALIZACAO:
                texto_esq = identificar_acorde(notas_esq)
                notas_dir_formatadas = [numero_para_nota(n) for n in sorted(notas_dir)]
                texto_dir = " - ".join(notas_dir_formatadas)

                if texto_esq or texto_dir:
                    if texto_esq and texto_dir:
                        texto_chatbox = f"🎹 Esq: {texto_esq} | Dir: {texto_dir}"
                    elif texto_esq:
                        texto_chatbox = f"🎹 Esq: {texto_esq}"
                    elif texto_dir:
                        texto_chatbox = f"🎹 Dir: {texto_dir}"
                    
                    cliente_osc.send_message("/chatbox/input", [texto_chatbox, True, False])
                    print(texto_chatbox)
                    enviou_silencio = False
                
                else:
                    if not enviou_silencio:
                        cliente_osc.send_message("/chatbox/input", ["", True, False])
                        print("🤫 Silêncio... (Controle devolvido ao MagicChatbox)")
                        enviou_silencio = True

                ultimo_envio = tempo_atual

if __name__ == "__main__":
    try:
        iniciar()
    except KeyboardInterrupt:
        print("\n🛑 Script encerrado.")
