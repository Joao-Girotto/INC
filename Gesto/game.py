import cv2
import mediapipe as mp
import pygame
import sys
import random  

# Inicializa MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Inicializa webcam
cap = cv2.VideoCapture(0)

# Inicializa Pygame
pygame.init()
screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Controle com a Mão")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Bola
ball_color = (255, 0, 0)
ball_radius = 20
ball_x, ball_y = 320, 240

# Caixa (alvo)
box_color = (0, 255, 0)
box_width, box_height = 100, 100
box_x = random.randint(0, screen_width - box_width)   
box_y = random.randint(0, screen_height - box_height)

# Pontuação
score = 0
scored = False  # Para evitar múltiplos pontos por quadro

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            pygame.quit()
            sys.exit()

    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            lm = hand_landmarks.landmark[8]
            h, w, _ = frame.shape
            finger_x, finger_y = int(lm.x * w), int(lm.y * h)
            ball_x = int(lm.x * screen_width)
            ball_y = int(lm.y * screen_height)
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Verifica se a bola está dentro da caixa
    if (box_x < ball_x < box_x + box_width and
        box_y < ball_y < box_y + box_height):
        if not scored:
            score += 1
            if score == 20:
                print("Você ganhou!")
                pygame.quit()
                sys.exit()
            scored = True
            box_x = random.randint(0, screen_width - box_width)
            box_y = random.randint(0, screen_height - box_height)
    else:
        scored = False  # Reseta quando a bola sai da caixa

    # Desenho
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, box_color, (box_x, box_y, box_width, box_height))
    pygame.draw.circle(screen, ball_color, (ball_x, ball_y), ball_radius)

    # Mostrar pontuação
    score_text = font.render(f"Pontos: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

    cv2.imshow("Webcam", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
