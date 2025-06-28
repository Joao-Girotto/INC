import cv2
import mediapipe as mp
import socket
import math

UDP_IP = '127.0.0.1'
UDP_PORT = 65432

# Inicializa socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print(f"[UDP] Servidor pronto em {UDP_IP}:{UDP_PORT}")

def get_hand_orientation(hand_landmarks):
    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
    middle_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
    return middle_finger_mcp.x - wrist.x

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

espaco_estado_atual = "UP"
seta_direita_estado_atual = "UP"
seta_esquerda_estado_atual = "UP"

# Parâmetros de controle
THRESHOLD_FINGER_BENT = 0.08
LIMITE_INCLINACAO_DIREITA = -0.05
LIMITE_INCLINACAO_ESQUERDA = 0.05

def send_udp_message(message):
    try:
        sock.sendto(message.encode('utf-8'), (UDP_IP, UDP_PORT))
        print(f"[UDP] Enviado: {message}")
    except Exception as e:
        print(f"[ERRO UDP] {e}")

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    detected_hand_closed = False
    detected_right_tilt = False
    detected_left_tilt = False

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Pontas dos dedos
            tips = [
                mp_hands.HandLandmark.INDEX_FINGER_TIP,
                mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                mp_hands.HandLandmark.RING_FINGER_TIP,
                mp_hands.HandLandmark.PINKY_TIP,
            ]
            mcps = [
                mp_hands.HandLandmark.INDEX_FINGER_MCP,
                mp_hands.HandLandmark.MIDDLE_FINGER_MCP,
                mp_hands.HandLandmark.RING_FINGER_MCP,
                mp_hands.HandLandmark.PINKY_MCP,
            ]

            # Contar dedos dobrados
            finger_bent_count = 0
            for tip, mcp in zip(tips, mcps):
                tip_point = hand_landmarks.landmark[tip]
                mcp_point = hand_landmarks.landmark[mcp]
                dist = math.sqrt(
                    (tip_point.x - mcp_point.x)**2 +
                    (tip_point.y - mcp_point.y)**2 +
                    (tip_point.z - mcp_point.z)**2
                )
                if dist < THRESHOLD_FINGER_BENT:
                    finger_bent_count += 1

            detected_hand_closed = finger_bent_count >= 3

            # Detectar inclinação
            if not detected_hand_closed:
                orientation = get_hand_orientation(hand_landmarks)
                if orientation < LIMITE_INCLINACAO_DIREITA:
                    detected_right_tilt = True
                elif orientation > LIMITE_INCLINACAO_ESQUERDA:
                    detected_left_tilt = True

    # Envio UDP
    if detected_hand_closed and espaco_estado_atual == "UP":
        send_udp_message("space_down")
        espaco_estado_atual = "DOWN"
    elif not detected_hand_closed and espaco_estado_atual == "DOWN":
        send_udp_message("space_up")
        espaco_estado_atual = "UP"

    if detected_right_tilt and seta_direita_estado_atual == "UP":
        send_udp_message("right_down")
        seta_direita_estado_atual = "DOWN"
    elif not detected_right_tilt and seta_direita_estado_atual == "DOWN":
        send_udp_message("right_up")
        seta_direita_estado_atual = "UP"

    if detected_left_tilt and seta_esquerda_estado_atual == "UP":
        send_udp_message("left_down")
        seta_esquerda_estado_atual = "DOWN"
    elif not detected_left_tilt and seta_esquerda_estado_atual == "DOWN":
        send_udp_message("left_up")
        seta_esquerda_estado_atual = "UP"

    cv2.imshow('Controle por Gestos', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

sock.close()
cap.release()
cv2.destroyAllWindows()