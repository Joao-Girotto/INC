import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1)  # detecta apenas uma mão

cap = cv2.VideoCapture(0)

# Lista de dedos (exceto polegar, que é tratado separadamente)
finger_tips = [8, 12, 16, 20]
finger_pips = [6, 10, 14, 18]

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            finger_count = 0

            # Polegar (compara eixo X em vez de Y)
            thumb_tip = hand_landmarks.landmark[4]
            thumb_ip = hand_landmarks.landmark[3]
            thumb_cmc = hand_landmarks.landmark[2]
            if thumb_tip.x > thumb_ip.x and thumb_tip.x > thumb_cmc.x:
                finger_count += 1  # mão direita (para esquerda inverta o sinal)

            # Outros dedos (indicador, médio, anelar, mínimo)
            for tip, pip in zip(finger_tips, finger_pips):
                if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
                    finger_count += 1

            # Exibir número de dedos levantados
            # cv2.putText(frame, f"Dedos: {finger_count}", (10, 50),
            #             cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 0), 2)
            if finger_count == 2:
                cv2.putText(frame, f"TUDO 2, EH O CV PAI", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 0), 2)

            # Detectar joinha: só o polegar levantado
            if finger_count == 1:
                if thumb_tip.y < thumb_ip.y and thumb_tip.y < thumb_cmc.y:
                    cv2.putText(frame, "👍 JOINHA DETECTADO!", (10, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    cv2.imshow("Reconhecimento de Gestos", frame)
    if cv2.waitKey(10) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()