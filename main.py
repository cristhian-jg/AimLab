import cv2
import mediapipe as mp
import math
import random

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

def es_gesto_pistola(landmarks):
    dedos_arriba = []
    tips = [8, 12, 16, 20]

    for tip in tips:
        arriba = landmarks[tip].y < landmarks[tip - 2].y
        dedos_arriba.append(arriba)

    return dedos_arriba == [True, False, False, False]

def nueva_pelota(w, h):
    return {
        "x": random.randint(100, w - 100),
        "y": random.randint(100, h - 100),
        "r": 30
    }

pelota = nueva_pelota(640, 480)
score = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)

    if result.multi_hand_landmarks:

        cv2.circle(frame, (pelota["x"], pelota["y"]), pelota["r"], (0, 0, 255), -1)

        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            h, w, _ = frame.shape
            x = int(hand_landmarks.landmark[8].x * w)
            y = int(hand_landmarks.landmark[8].y * h)
            cv2.circle(frame, (x, y), 10, (255, 0, 0), -1)

            x2= int(hand_landmarks.landmark[1].x * w)
            y2= int(hand_landmarks.landmark[1].y * h)
            cv2.circle(frame, (x2, y2), 10, (255, 0, 0), -1)

            print(hand_landmarks.landmark[8])

            centro_x = w // 2
            centro_y = h // 2

            distancia = math.hypot(x - centro_x, y - centro_y)

            color = (0, 255, 0) if distancia < 100 else (255, 0, 0)
            cv2.circle(frame, (x, y), 10, color, -1)

            if es_gesto_pistola(hand_landmarks.landmark):
                dist = math.hypot(x - pelota["x"], y - pelota["y"])
                if dist < pelota["r"]:
                    pelota = nueva_pelota(w, h)
                    score += 1
                print("Gesto de pistola detectado")

    cv2.putText(frame, f'Puntuacion: {score}', (10, 40), cv2.FONT_HERSHEY_COMPLEX, 1.2, (255, 255, 255), 2)

    cv2.imshow("Camara", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()