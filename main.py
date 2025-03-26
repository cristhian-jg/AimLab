# Librerías utilizadas para camámara, manos,
# colisiones, animaciones y tiempo

import cv2
import mediapipe as mp
import math
import random
import time
import numpy as np
import pyautogui

# Muestra la primera pantalla con un botón que se debe 
# pulsar con el dedo indice para comenzar a jugar.
def pantalla_inicio(hands, cap):
    cv2.namedWindow("Inicio", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Inicio", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    boton_ancho, boton_alto = 200, 70
    boton_x1 = screenWidth // 2 - boton_ancho // 2
    boton_y1 = screenHeight // 2 + 100
    boton_x2 = boton_x1 + boton_ancho
    boton_y2 = boton_y1 + boton_alto
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (screenWidth, screenHeight))
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(frame_rgb)

        # Dibujo del botón para comenzar a jugar
        cv2.rectangle(frame, (boton_x1, boton_y1), (boton_x2, boton_y2), (0, 255, 0), -1)
        cv2.putText(frame, "JUGAR", (boton_x1 + 55, boton_y1 + 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        # Detección del dedo cuando toca el botón
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                h, w, _ = frame.shape
                x = int(hand_landmarks.landmark[8].x * w)
                y = int(hand_landmarks.landmark[8].y * h)

                cv2.circle(frame, (x, y), 10, (255, 0, 0), -1)

                # Si el dedo está dentro del area del botón se cierra 
                # esta ventana y comienza el juego
                if boton_x1 <= x <= boton_x2 and boton_y1 <= y <= boton_y2:
                    return
        
        # Muestra la ventana
        cv2.imshow("Inicio", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            exit()

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
        "r": 60,
        "tiempo_creacion": time.time()
    }

def cuenta_regresiva(cap):
    for i in range(3, 0, -1):
        ret, frame = cap.read()
        if not ret:
            continue
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (screenWidth, screenHeight))
        cv2.putText(frame, str(i), (screenWidth // 2 - 50, screenHeight // 2), cv2.FONT_HERSHEY_DUPLEX, 5,  (0, 255, 0), 5)
        cv2.imshow("Camara", frame)
        cv2.waitKey(1000)

    ret, frame = cap.read()
    if ret:
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (screenWidth, screenHeight))
        cv2.putText(frame, "YA!", (screenWidth // 2 - 100, screenHeight // 2), cv2.FONT_HERSHEY_DUPLEX, 5, (0, 255, 255), 5)
        cv2.imshow("Camara", frame)
        cv2.waitKey(1000)

def calcultar_intervalo(tiempo_restante, duracion_juego):
    progreso = 1 - (tiempo_restante / duracion_juego)
    return max(0.2, 1 - progreso * 0.8)

def pantalla_final(score, hands, cap):
    cv2.namedWindow("AimLab - Fin del juego", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("AimLab - Fin del juego", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    boton_ancho, boton_alto = 200, 70
    boton_x1 = screenWidth // 2 - boton_ancho // 2
    boton_y1 = screenHeight // 2 + 100
    boton_x2 = boton_x1 + boton_ancho
    boton_y2 = boton_y1 + boton_alto

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (screenWidth, screenHeight))
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(frame_rgb)

        cv2.putText(frame, f"Puntuacion final: {score}", (130, 150), cv2.FONT_HERSHEY_COMPLEX, 1.2, (255, 255, 255), 2)
        cv2.putText(frame, "Pulsa Play para jugar otra vez", (110, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.rectangle(frame, (boton_x1, boton_y1), (boton_x2, boton_y2), (0, 255, 0), -1)
        cv2.putText(frame, "PLAY", (boton_x1 + 55, boton_y1 + 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                h, w, _ = frame.shape
                x = int(hand_landmarks.landmark[8].x * w)
                y = int(hand_landmarks.landmark[8].y * h)
                cv2.circle(frame, (x, y), 10, (255, 0, 0), -1)

                if boton_x1 <= x <= boton_x2 and boton_y1 <= y <= boton_y2:
                    # cv2.destroyAllWindows()
                    return

        cv2.imshow("AimLab - Fin del juego", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            exit()

screenWidth, screenHeight = pyautogui.size()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, screenWidth)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screenHeight)

while True:
    pantalla_inicio(hands, cap)
    cuenta_regresiva(cap)
    cv2.namedWindow("Camara", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Camara", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    pelotas = []
    vida_pelota = 3  # segundos
    score = 0
    duracion_juego = 30
    tiempo_inicio = time.time()
    ultimo_spawn = 0
    ret, frame = cap.read()
    h, w, _ = frame.shape

    while True:
      
        tiempo_actual = time.time()
        tiempo_restante = int(duracion_juego - (tiempo_actual - tiempo_inicio))

        intervalo_spawn = calcultar_intervalo(tiempo_restante, duracion_juego)
        if time.time() - ultimo_spawn > intervalo_spawn:
            pelotas.append(nueva_pelota(w, h))
            ultimo_spawn = time.time()

        if tiempo_restante <= 0:
            break

        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (screenWidth, screenHeight))

        for pelota in pelotas:
            tiempo_vida_usado = time.time() - pelota["tiempo_creacion"]
            factor = max(0, 1 - (tiempo_vida_usado / vida_pelota))
            radio_animado = max(1, int(pelota["r"] * factor))  # mínimo 1 px
            cv2.circle(frame, (pelota["x"], pelota["y"]), radio_animado, (0, 0 , 255), -1)
        
        for pelota in pelotas[:]:
            if time.time() - pelota["tiempo_creacion"] > 3:
                pelotas.remove(pelota)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(frame_rgb)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                h, w, _ = frame.shape
                x = int(hand_landmarks.landmark[8].x * w)
                y = int(hand_landmarks.landmark[8].y * h)
                cv2.circle(frame, (x, y), 10, (255, 0, 0), -1)

                print(hand_landmarks.landmark[8])

                centro_x = w // 2
                centro_y = h // 2

                distancia = math.hypot(x - centro_x, y - centro_y)

                color = (0, 255, 0) if distancia < 100 else (255, 0, 0)
                cv2.circle(frame, (x, y), 10, color, -1)

                for pelota in pelotas[:]:
                    dist = math.hypot(x - pelota["x"], y - pelota["y"])
                    if dist < pelota["r"]:
                        pelotas.remove(pelota)
                        score += 1

        # Puntuación
        cv2.putText(frame, f'Puntuacion: {score}', (10, 40), cv2.FONT_HERSHEY_COMPLEX, 1.2, (255, 255, 255), 2)
        
        # Tiempo restante
        cv2.putText(frame, f"Tiempo: {tiempo_restante}", (10, 80), cv2.FONT_HERSHEY_COMPLEX, 1.2, (0, 255, 255), 2)

        cv2.imshow("Camara", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    pantalla_final(score, hands, cap)

cap.release()
cv2.destroyAllWindows()