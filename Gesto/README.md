# Jogo de Controle com a Mão

Este projeto é um jogo simples onde o jogador controla uma bola com o movimento da mão (detecção de dedo indicador) através da webcam. O objetivo é mover a bola até uma caixa verde na tela. Ao acertar a caixa, o jogador ganha pontos até alcançar 20, momento em que o jogo é finalizado com uma vitória.

## O que o código faz

- Captura vídeo da webcam em tempo real.
- Usa a biblioteca MediaPipe para detectar a posição do dedo indicador da mão.
- Usa a biblioteca Pygame para criar a interface gráfica do jogo.
- Mapeia o movimento do dedo para movimentar uma bola na tela.
- Ao colidir com uma "caixa-alvo", o jogador ganha pontos.
- O jogo termina quando o jogador atinge 20 pontos.

## Bibliotecas utilizadas

| Biblioteca   | Finalidade                                                                 |
|--------------|---------------------------------------------------------------------------|
| OpenCV (`cv2`)      | Captura de vídeo em tempo real e manipulação de imagem.              |
| MediaPipe (`mediapipe`) | Detecção dos pontos de referência da mão, especialmente do dedo indicador. |
| Pygame       | Criação da interface do jogo, renderização de gráficos e controle de eventos. |
| random       | Geração de posições aleatórias para a caixa-alvo.                          |
| sys          | Encerramento seguro do programa.                                           |

## Como executar

### Pré-requisitos

Certifique-se de ter o Python 3 instalado e instale as dependências com:

```bash
pip install opencv-python mediapipe pygame
```

### Executando o jogo

1. Conecte uma webcam ao computador (caso não use embutida).
2. Execute o script Python:

```bash
python game.py
```

3. Mova seu dedo indicador em frente à câmera para controlar a bola.
4. A cada acerto na caixa verde, você ganha um ponto.
5. Ao atingir 20 pontos, o jogo exibe uma mensagem de vitória e se encerra.

## Observações

- A precisão da detecção pode variar dependendo da iluminação e da qualidade da câmera.
- O jogo exibe a imagem da webcam com os pontos da mão detectados usando OpenCV.

