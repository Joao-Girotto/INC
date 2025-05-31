# Jogo de Controle por Giroscópio

Este projeto implementa um jogo simples controlado por dados de giroscópio recebidos através de uma conexão de rede UDP. O objetivo é mover um círculo vermelho para colidir com uma caixa verde, ganhando pontos a cada colisão. O jogo termina quando 5 pontos são alcançados.

## Como Funciona

O script Python `Giro.py` configura um socket UDP para ouvir os dados recebidos, presumivelmente de um dispositivo com um giroscópio. Em seguida, ele usa a biblioteca Pygame para criar uma janela gráfica onde o jogo acontece.

Os dados do giroscópio (especificamente os componentes X e Y) são usados para controlar a velocidade de um círculo vermelho na tela. O movimento do círculo é suavizado usando interpolação linear e amortecido para evitar movimentos excessivamente erráticos. Quando o círculo vermelho colide com sucesso com a caixa alvo verde, o jogador marca um ponto e uma nova caixa alvo aparece em um local aleatório. O jogo exibe a pontuação atual e termina quando 5 pontos são acumulados.

## Bibliotecas Utilizadas

* **`socket`**: Esta biblioteca é usada para comunicação de rede. Neste projeto, ela é usada para criar um socket UDP para receber dados do giroscópio de uma fonte externa.
* **`pygame`**: Esta biblioteca é um conjunto de módulos Python projetados para escrever videogames. É usada aqui para:
    * Criar a janela do jogo e gerenciar a exibição.
    * Lidar com eventos do jogo (como fechar a janela).
    * Desenhar formas (círculo e retângulo) na tela.
    * Renderizar texto (para a exibição da pontuação).
    * Controlar a taxa de quadros do jogo.
* **`sys`**: Este módulo fornece acesso a parâmetros e funções específicas do sistema. Ele é usado aqui especificamente para sair do aplicativo graciosamente quando a janela do Pygame é fechada.
* **`random`**: Este módulo implementa geradores de números pseudoaleatórios. Ele é usado para posicionar aleatoriamente a caixa alvo na tela após cada colisão bem-sucedida.

## Como Executar

1.  **Pré-requisitos:**
    * Python 3 instalado em seu sistema.
    * A biblioteca Pygame instalada. Se você não a tiver, pode instalá-la via pip:
        ```bash
        pip install pygame
        ```

2.  **Fonte de Dados do Giroscópio:** Este script espera que os dados do giroscópio sejam enviados para `UDP_IP = "192.168.61.2"` e `UDP_PORT = 5005`. Você precisará de um aplicativo ou dispositivo separado configurado para enviar leituras do giroscópio (componentes X, Y, Z) como uma string separada por vírgulas para este endereço IP e porta. O script procura especificamente os valores X e Y do giroscópio nos índices 3 e 4 (base zero) dos dados separados por vírgulas.

3.  **Executar o Jogo:**
    Navegue até o diretório onde você salvou `Giro.py` e execute o script:
    ```bash
    python Giro.py
    ```

    Uma vez executado, uma janela do Pygame aparecerá e o jogo começará a ouvir os dados do giroscópio.
