# VRChat Piano Chatbox 🎹

Este projeto é um script em Python que lê as notas tocadas num teclado MIDI (ou piano digital), identifica os acordes e envia tudo em tempo real para o balão de texto (Chatbox) acima da sua cabeça no VRChat usando o protocolo OSC.

## ✨ Funcionalidades
* **Divisão Inteligente:** Separa automaticamente a Mão Esquerda (acordes) da Mão Direita (notas soltas).
* **Motor Harmônico:** Reconhece dezenas de acordes, incluindo inversões, sétimas, nonas e acordes suspensos.
* **Compatibilidade com MagicChatbox:** O script entra em modo de silêncio automaticamente quando não está a tocar, libertando o espaço do Chatbox para outros programas (como Spotify ou monitorização do PC).
* **Antispam Integrado:** Agrupa as notas e respeita os limites de envio do VRChat para evitar que o Chatbox bloqueie.

## 🛠️ Pré-requisitos
Antes de começar, precisa de ter instalado no seu computador:
* **[Python 3.13](https://www.python.org/downloads/)** (Certifique-se de marcar a opção "Add Python to PATH" durante a instalação).
* **[loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html)** (Para criar a porta virtual).
* Um software de áudio/DAW (como FL Studio) para rotear o sinal do seu piano.

---

## 🚀 Como Instalar e Configurar

### Passo 1: Configurar o Cabo Virtual (loopMIDI)
Como o Windows não permite que dois programas leiam o mesmo dispositivo MIDI em simultâneo, precisamos de criar uma ponte.
1. Abra o **loopMIDI**.
2. No campo "New port-name", escreva exatamente: `Piano Chat`
3. Clique no botão **+** para criar a porta. Pode minimizar o programa (ele deve ficar a correr em segundo plano).

### Passo 2: Rotear o Sinal (Exemplo no FL Studio)
1. Abra o FL Studio e vá a **Options > MIDI Settings** (F10).
2. Na lista superior (**Output**), selecione a porta `Piano Chat` e defina um **Port Number** (ex: 10).
3. Adicione o plugin nativo **MIDI Out** ao seu Channel Rack e defina a porta (Port) dele para o mesmo número (ex: 10).
4. **Trancar as entradas:** Clique com o botão direito no seu instrumento de Piano VST > **Receive notes from** > Selecione o seu teclado. Faça o mesmo no plugin **MIDI Out**. Isto garante que não perde o sinal OSC ao clicar noutra janela do FL Studio.

### Passo 3: Configurar o Python
1. Faça o download deste repositório e abra a pasta no terminal (ou no VS Code).
2. Crie um ambiente virtual para não misturar as bibliotecas com o resto do sistema executando: `python -m venv venv`
3. Ative o ambiente virtual executando: `.\venv\Scripts\activate`
4. Instale as bibliotecas necessárias usando o ficheiro incluído executando: `pip install -r requirements.txt`

### Passo 4: Ativar o OSC no VRChat
1. Abra o VRChat.
2. Abra o **Action Menu** (menu radial).
3. Navegue até **Options > OSC > Enabled** e certifique-se de que está ligado.

---

## 🎮 Como Usar
Com o loopMIDI a rodando de fundo e o VRChat aberto, abra o terminal na pasta do projeto (## certifique-se de que o `(venv)` está ativado) e execute o comando:

`python main.py`

Sempre que colocar as mãos nas teclas, os acordes vão aparecer instantaneamente no jogo. Quando soltar todas as teclas, o texto desaparece automaticamente para não entrar em conflito com outros programas OSC.

## ⚙️ Personalização
Pode editar as variáveis no topo do ficheiro `main.py` para ajustar o sistema ao seu estilo de tocar:
* `PONTO_DIVISAO_MIDI = 60`: Define a nota de corte entre a mão esquerda e direita. O padrão é 60 (Dó Central). Se os seus acordes da mão esquerda forem muito abertos, tente aumentar para `64` ou `65`.
* `ATRASO_ATUALIZACAO = 0.3`: Controla o intervalo de atualização para não sobrecarregar o Chatbox.
