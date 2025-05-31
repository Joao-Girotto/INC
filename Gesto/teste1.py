import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
cap = cv2.VideoCapture(0)

# Dedo indicadores para comparação (exceto polegar)
finger_tips = [8, 12, 16, 20]
finger_pips = [6, 10, 14, 18]

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks and result.multi_handedness:
        for hand_landmarks, handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            hand_label = handedness.classification[0].label  # "Left" ou "Right"
            finger_count = 0

            # Polegar: comparar eixo X (muda com base na mão)
            thumb_tip = hand_landmarks.landmark[4]
            thumb_ip = hand_landmarks.landmark[3]
            thumb_cmc = hand_landmarks.landmark[2]

            if hand_label == "Right":
                if thumb_tip.x > thumb_ip.x and thumb_tip.x > thumb_cmc.x:
                    finger_count += 1
            else:  # Left
                    thumb_tip = hand_landmarks.landmark[4]
                    index_tip = hand_landmarks.landmark[8]
                    middle_tip = hand_landmarks.landmark[12]
                    ring_tip = hand_landmarks.landmark[16]
                    pinky_tip = hand_landmarks.landmark[20]

                    middle_pip = hand_landmarks.landmark[10]
                    ring_pip = hand_landmarks.landmark[14]
                    pinky_pip = hand_landmarks.landmark[18]

                    # Distância entre polegar e indicador
                    dist = calcular_distancia(thumb_tip, index_tip)

                    # Verifica se os dedos estão fechados
                    outros_dedos_fechados = (
                        middle_tip.y > middle_pip.y and
                        ring_tip.y > ring_pip.y and
                        pinky_tip.y > pinky_pip.y
                    )

    # Verifica distância apropriada para o "C"
        if 0.08 < dist < 0.18 and outros_dedos_fechados:
            cv2.putText(frame, "Letra C Detectada!", (10, 180),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

            # Outros dedos (y menor = levantado)
            for tip, pip in zip(finger_tips, finger_pips):
                if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
                    finger_count += 1

            # Posicionamento visual
            if hand_label == "Right":
                x, y = 10, 50
            else:
                x, y = 10, 120

            # Exibir dados
            cv2.putText(frame, f"{hand_label} Hand - Dedos: {finger_count}", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)

            # Detectar joinha
            if finger_count == 1:
                if thumb_tip.y < thumb_ip.y and thumb_tip.y < thumb_cmc.y:
                    cv2.putText(frame, f"{hand_label} - JOINHA!", (x, y + 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow("Gestos com Duas Maos", frame)
    if cv2.waitKey(10) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()