# Assistente de Voz Simples

Este projeto implementa um assistente de voz básico em Python, capaz de responder a comandos de voz específicos, como informar a hora atual e abrir o navegador da web. Ele utiliza bibliotecas para síntese de fala e reconhecimento de voz.

## Como Funciona

O script `assistente_voz.py` inicializa um motor de síntese de fala (`pyttsx3`) e configura uma voz em português, se disponível. Ele define duas funções principais: `falar()` para converter texto em fala e `ouvir()` para capturar áudio do microfone e convertê-lo em texto usando o reconhecimento de fala do Google.

A função `main()` entra em um loop contínuo, onde o assistente aguarda um comando de voz. Os comandos atualmente suportados são:
* "que horas são": o assistente informa a hora atual.
* "abrir navegador": o assistente abre o navegador da web padrão na página do Google.
* "sair": o assistente encerra o programa.

## Bibliotecas Utilizadas

* **`pyttsx3`**: Esta biblioteca é um motor de síntese de fala (text-to-speech) multiplataforma. É utilizada neste projeto para permitir que o assistente "fale" as respostas para o usuário.
* **`speech_recognition` (sr)**: Esta biblioteca fornece uma interface para vários motores e APIs de reconhecimento de fala. É usada aqui para:
    * Capturar áudio do microfone.
    * Reconhecer a fala do usuário e convertê-la em texto, utilizando a API de reconhecimento de fala do Google (requer conexão com a internet).
* **`datetime`**: Este módulo fornece classes para manipular datas e horas. É usado para obter a hora atual do sistema.
* **`webbrowser`**: Este módulo fornece uma interface de alto nível para exibir documentos da web. É usado para abrir o navegador da web padrão do sistema em um URL específico.

## Como Executar

1.  **Pré-requisitos:**
    * Python 3 instalado em seu sistema.
    * As bibliotecas `pyttsx3` e `SpeechRecognition` instaladas. Se você não as tiver, pode instalá-las via pip:
        ```bash
        pip install pyttsx3 SpeechRecognition
        ```
    * Para o `pyttsx3` funcionar, você pode precisar de um driver de fala (como o `sapi5` no Windows, `nsspeechsynthesizer` no macOS ou `espeak` no Linux). No Linux, você pode instalar o `espeak` com:
        ```bash
        sudo apt-get install espeak
        ```
    * Uma conexão ativa com a internet é necessária para o reconhecimento de fala do Google.

2.  **Permissões do Microfone:** Certifique-se de que seu sistema operacional concedeu permissão ao Python para acessar o microfone.

3.  **Executar o Assistente:**
    Navegue até o diretório onde você salvou `assistente_voz.py` e execute o script:
    ```bash
    python assistente_voz.py
    ```
