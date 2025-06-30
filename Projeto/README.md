# Projeto de Controle por Gestos com Godot e Python

Este projeto demonstra a integração de controle facial e gestual via câmera com um jogo desenvolvido na engine **Godot 4.4.1**. Utiliza Python (com OpenCV e MediaPipe) para detectar movimentos e enviar comandos ao jogo via UDP.

## Requisitos

- **Godot 4.4.1** (versões diferentes podem apresentar incompatibilidades)
- Python 3.10+
- Bibliotecas Python:
  - `opencv-python`
  - `mediapipe`
  - `socket`

## Estrutura do Projeto

- `Face_udp.py`: envia comandos baseados na movimentação do rosto.
- `hand_udp.py`: envia comandos baseados em gestos com as mãos.
- `interfaces_jogo/projeto/`: contém o jogo desenvolvido em Godot.
  - `project.godot`: arquivo principal do projeto Godot.
  - `game_controller.gd`, `game_init.gd`, `GestureInput.gd`: scripts que controlam a lógica do jogo.
  - `camera_utils.gd`: funções auxiliares para o uso de câmera.
  - `devjogosassetsparaaaula.zip`: pacote de assets utilizado no jogo.

## Como Executar

1. **Instale as dependências Python**:
   ```bash
   pip install opencv-python mediapipe
   ```

2. **Execute um dos scripts Python** (por exemplo, controle por rosto):
   ```bash
   python Face_udp.py
   ```

3. **Abra o projeto no Godot 4.4.1**:
   - Navegue até `interfaces_jogo/projeto/`.
   - Abra `project.godot` com o Godot.

4. **Execute o jogo** na Godot. Ele se comunicará via UDP com os scripts Python para receber comandos.

## Observações

- Certifique-se de que a câmera está conectada e funcionando.
- O endereço IP e porta podem ser ajustados nos scripts `Face_udp.py` e `hand_udp.py`.

