import cv2
import mediapipe as mp
import socket

UDP_IP = '127.0.0.1'
UDP_PORT = 65432

# Inicializa socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print(f"[UDP] Servidor pronto em {UDP_IP}:{UDP_PORT}")

# Inicializa FaceMesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# Estados para envio de comandos
boca_estado_atual = "FECHADA"
seta_direita_estado_atual = "UP"
seta_esquerda_estado_atual = "UP"

# Parâmetros de controle
THRESHOLD_BOCA_ABERTA = 0.04
LIMITE_MOVIMENTO_DIREITA = 0.58
LIMITE_MOVIMENTO_ESQUERDA = 0.42

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
    results = face_mesh.process(image_rgb)

    boca_aberta = False
    mover_para_direita = False
    mover_para_esquerda = False

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            mp_draw.draw_landmarks(image, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS)

            # Pontos da boca
            labio_superior = face_landmarks.landmark[13]
            labio_inferior = face_landmarks.landmark[14]
            dist_boca = abs(labio_inferior.y - labio_superior.y)

            boca_aberta = dist_boca > THRESHOLD_BOCA_ABERTA

            # Posição horizontal do nariz
            nariz = face_landmarks.landmark[1]
            nariz_x = nariz.x

            # INVERTENDO a direção
            if nariz_x > LIMITE_MOVIMENTO_DIREITA:
                mover_para_esquerda = True
            elif nariz_x < LIMITE_MOVIMENTO_ESQUERDA:
                mover_para_direita = True

    # Controle da boca
    if boca_aberta and boca_estado_atual == "FECHADA":
        send_udp_message("space_down")
        boca_estado_atual = "ABERTA"
    elif not boca_aberta and boca_estado_atual == "ABERTA":
        send_udp_message("space_up")
        boca_estado_atual = "FECHADA"

    # Movimento para a direita
    if mover_para_direita and seta_direita_estado_atual == "UP":
        send_udp_message("right_down")
        seta_direita_estado_atual = "DOWN"
    elif not mover_para_direita and seta_direita_estado_atual == "DOWN":
        send_udp_message("right_up")
        seta_direita_estado_atual = "UP"

    # Movimento para a esquerda
    if mover_para_esquerda and seta_esquerda_estado_atual == "UP":
        send_udp_message("left_down")
        seta_esquerda_estado_atual = "DOWN"
    elif not mover_para_esquerda and seta_esquerda_estado_atual == "DOWN":
        send_udp_message("left_up")
        seta_esquerda_estado_atual = "UP"

    cv2.imshow('Controle por Rosto', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

sock.close()
cap.release()
cv2.destroyAllWindows()