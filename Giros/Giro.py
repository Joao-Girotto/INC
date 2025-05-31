import socket
import pygame
import sys
import random

# Configurações da rede
UDP_IP = "192.168.61.2"
UDP_PORT = 5005

# Inicia o socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.setblocking(False)  # Evita travamento da aplicação

# Inicializa a janela do pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Controle via Giroscópio")

# Cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Posição inicial do círculo
x, y = 400, 300

# Caixa-alvo
box_width, box_height = 100, 100
box_x = random.randint(0, 800 - box_width)
box_y = random.randint(0, 600 - box_height)

# Pontuação
score = 0
scored = False
font = pygame.font.SysFont(None, 36)

clock = pygame.time.Clock()
vx, vy = 0, 0

print(f"Aguardando dados do giroscópio em {UDP_IP}:{UDP_PORT}...")

# Parâmetros de controle
GYRO_THRESHOLD_MOVEMENT = 0.1
MOVEMENT_SENSITIVITY = 0.8
DAMPING_FACTOR = 0.92
MAX_SPEED = 8

GYRO_X_INDEX = 3
GYRO_Y_INDEX = 4
GYRO_Z_INDEX = 5

# Função de interpolação linear
def lerp(a, b, t):
    return a + (b - a) * t

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Tentativa não bloqueante de ler dados
    try:
        data, _ = sock.recvfrom(1024)
        decoded_data = data.decode('utf-8').strip()
        parts = decoded_data.split(',')

        if len(parts) > max(GYRO_X_INDEX, GYRO_Y_INDEX, GYRO_Z_INDEX):
            gx = float(parts[GYRO_X_INDEX]) * -1
            gy = float(parts[GYRO_Y_INDEX]) * -1

            is_gyro_stationary = True

            if abs(gx) < GYRO_THRESHOLD_MOVEMENT:
                gx = 0
            else:
                is_gyro_stationary = False 

            if abs(gy) < GYRO_THRESHOLD_MOVEMENT:
                gy = 0
            else:
                is_gyro_stationary = False 

            if is_gyro_stationary:
                vx = 0
                vy = 0
            else:
                if abs(gx) > abs(gy):
                    gy = 0
                else:
                    gx = 0

                vx += gx * MOVEMENT_SENSITIVITY
                vy += gy * MOVEMENT_SENSITIVITY

                vx *= DAMPING_FACTOR
                vy *= DAMPING_FACTOR

            vx = max(-MAX_SPEED, min(vx, MAX_SPEED))
            vy = max(-MAX_SPEED, min(vy, MAX_SPEED))
    except BlockingIOError:
        pass  # Sem dados recebidos neste frame
    except Exception as e:
        print(f"Erro ao processar dados: {e}")

    # Suavização com interpolação
    target_x = x + int(vx)
    target_y = y + int(vy)
    x = lerp(x, target_x, 0.3)
    y = lerp(y, target_y, 0.3)

    # Limita dentro da tela
    x = max(0, min(x, 800))
    y = max(0, min(y, 600))

    # Verifica colisão com a caixa
    if (box_x < x < box_x + box_width and
        box_y < y < box_y + box_height):
        if not scored:
            score += 1
            if score == 5:
                print("Você Ganhou !!!!!")
                break
            scored = True
            box_x = random.randint(0, 800 - box_width)
            box_y = random.randint(0, 600 - box_height)
    else:
        scored = False

    # Desenha
    screen.fill(WHITE)
    pygame.draw.rect(screen, GREEN, (box_x, box_y, box_width, box_height))
    pygame.draw.circle(screen, RED, (int(x), int(y)), 20)

    score_text = font.render(f"Pontos: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)  # Mantém 60 FPS
