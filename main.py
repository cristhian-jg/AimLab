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
    cv2.namedWindow("Aimlab", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Aimlab", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
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
        resultado_segmentacion = segmentacion.process(frame_rgb)
        mascara = resultado_segmentacion.segmentation_mask
        condicion = mascara > 0.5
        fondo = fondo_personalizado.copy()
        fondo = cv2.GaussianBlur(fondo, (25, 25), 0)
        frame = np.where(condicion[..., None], frame, fondo)
        result = hands.process(frame_rgb)

        # Dibujo del botón para comenzar a jugar
        cv2.rectangle(frame, (boton_x1, boton_y1), (boton_x2, boton_y2), (0, 255, 0), -1)
        cv2.putText(frame, "JUGAR", (boton_x1 + 55, boton_y1 + 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        # Detección del dedo cuando toca el botón
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                h, w, _ = frame.shape
                x = int(hand_landmarks.landmark[8].x * screenWidth)
                y = int(hand_landmarks.landmark[8].y * screenHeight)

                cv2.circle(frame, (x, y), 10, (255, 0, 0), -1)

                # Si el dedo está dentro del area del botón se cierra 
                # esta ventana y comienza el juego
                if boton_x1 <= x <= boton_x2 and boton_y1 <= y <= boton_y2:
                    return
        
        # Muestra la ventana
        cv2.imshow("Aimlab", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            exit()

# Obliga al usuario a usar un gesto de apuntar con la mano para jugar, se ha decidido
# descartar está opción, ya que se expondrá en un instituto con menores de edad. 
def es_gesto_pistola(landmarks):
    dedos_arriba = []
    tips = [8, 12, 16, 20]

    # Se comprueba que dedos tiene levantados, si los landsmarks se corresponden
    # significa que está haciendo el gesto de pistola.
    for tip in tips:
        arriba = landmarks[tip].y < landmarks[tip - 2].y
        dedos_arriba.append(arriba)

    return dedos_arriba == [True, False, False, False]

# Crea una nueva pelota con un radio concreto y su tiempo de creación.
def nueva_pelota(w, h):
    # Devuelve un diccionario con la posición de la pelota, el radio y el momento de la creación. 
    return {
        "x": random.randint(100, w - 100),
        "y": random.randint(100, h - 100),
        "r": 60,
        "tiempo_creacion": time.time()
    }

def dibujar_pelota_degradada(frame, x, y, r, color_centro, color_borde):
    overlay = frame.copy()

    for i in range(r, 0, -5):
        alpha = i / r
        color = [
            int(color_borde[j] + (color_centro[j] - color_borde[j]) * alpha)
            for j in range(3)
        ]
        cv2.circle(overlay, (x, y), i, color, -1)

    # Mezclamos el overlay con el frame original
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

# Cuenta regresiva (3...2...1...YA!) que se ejecuta al señalar el botón
#  jugar, será util para que el jugador se prepare.
def cuenta_regresiva(cap):
    for i in range(3, 0, -1):
        frame = cap.read()[1]
        if frame is None:
            continue
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (screenWidth, screenHeight))
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resultado_segmentacion = segmentacion.process(frame_rgb)
        mascara = resultado_segmentacion.segmentation_mask
        condicion = mascara > 0.5
        fondo = fondo_personalizado.copy()
        fondo = cv2.GaussianBlur(fondo, (25, 25), 0)
        frame = np.where(condicion[..., None], frame, fondo)
        cv2.putText(frame, str(i), (screenWidth // 2 - 50, screenHeight // 2), cv2.FONT_HERSHEY_DUPLEX, 5,  (0, 255, 0), 5)
        
        inicio = time.time()
        while time.time() - inicio < 1:
            frame_loop = cap.read()[1]
            if frame_loop is None:
                continue
            frame_loop = cv2.flip(frame_loop, 1)
            frame_loop = cv2.resize(frame_loop, (screenWidth, screenHeight))
            frame_rgb = cv2.cvtColor(frame_loop, cv2.COLOR_BGR2RGB)
            resultado_segmentacion = segmentacion.process(frame_rgb)
            mascara = resultado_segmentacion.segmentation_mask
            condicion = mascara > 0.5
            fondo = fondo_personalizado.copy()
            fondo = cv2.GaussianBlur(fondo, (25, 25), 0)
            frame_loop = np.where(condicion[..., None], frame_loop, fondo)
            cv2.putText(frame_loop, str(i), (screenWidth // 2 - 50, screenHeight // 2), cv2.FONT_HERSHEY_DUPLEX, 5,  (0, 255, 0), 5)
            cv2.imshow("Aimlab", frame_loop)
            if cv2.waitKey(1) & 0xFF == 27:
                exit()

    frame = cap.read()[1]
    if frame is not None:
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (screenWidth, screenHeight))
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resultado_segmentacion = segmentacion.process(frame_rgb)
        mascara = resultado_segmentacion.segmentation_mask
        condicion = mascara > 0.5
        fondo = fondo_personalizado.copy()
        fondo = cv2.GaussianBlur(fondo, (25, 25), 0)
        frame = np.where(condicion[..., None], frame, fondo)
        cv2.putText(frame, "YA!", (screenWidth // 2 - 100, screenHeight // 2), cv2.FONT_HERSHEY_DUPLEX, 5, (0, 255, 255), 5)
        
        inicio = time.time()
        while time.time() - inicio < 1:
            frame_loop = cap.read()[1]
            if frame_loop is None:
                continue
            frame_loop = cv2.flip(frame_loop, 1)
            frame_loop = cv2.resize(frame_loop, (screenWidth, screenHeight))
            frame_rgb = cv2.cvtColor(frame_loop, cv2.COLOR_BGR2RGB)
            resultado_segmentacion = segmentacion.process(frame_rgb)
            mascara = resultado_segmentacion.segmentation_mask
            condicion = mascara > 0.5
            fondo = fondo_personalizado.copy()
            fondo = cv2.GaussianBlur(fondo, (25, 25), 0)
            frame_loop = np.where(condicion[..., None], frame_loop, fondo)
            cv2.putText(frame_loop, "YA!", (screenWidth // 2 - 100, screenHeight // 2), cv2.FONT_HERSHEY_DUPLEX, 5, (0, 255, 255), 5)
            cv2.imshow("Aimlab", frame_loop)
            if cv2.waitKey(1) & 0xFF == 27:
                exit()

# Hace que la velocidad de aparición de las pelotas aumente 
# con el paso del tiempo
def calcular_intervalo(tiempo_restante, duracion_juego):
    progreso = 1 - (tiempo_restante / duracion_juego)
    return max(0.2, 1 - progreso * 0.8)

# Muestra la ultima pantalla donde aparecen la puntuación
# obtenido y puedes volver a jugar.
def pantalla_final(score, hands, cap):
    cv2.namedWindow("Aimlab", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Aimlab", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

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
        resultado_segmentacion = segmentacion.process(frame_rgb)
        mascara = resultado_segmentacion.segmentation_mask
        condicion = mascara > 0.5
        fondo = fondo_personalizado.copy()
        fondo = cv2.GaussianBlur(fondo, (25, 25), 0)
        frame = np.where(condicion[..., None], frame, fondo)
        result = hands.process(frame_rgb)

        cv2.putText(frame, f"Puntuacion final: {score}", (130, 150), cv2.FONT_HERSHEY_COMPLEX, 1.2, (255, 255, 255), 2)
        cv2.putText(frame, "Pulsa Play para jugar otra vez", (110, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.rectangle(frame, (boton_x1, boton_y1), (boton_x2, boton_y2), (0, 255, 0), -1)
        cv2.putText(frame, "PLAY", (boton_x1 + 55, boton_y1 + 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                h, w, _ = frame.shape
                x = int(hand_landmarks.landmark[8].x * screenWidth)
                y = int(hand_landmarks.landmark[8].y * screenHeight)
                cv2.circle(frame, (x, y), 10, (255, 0, 0), -1)

                if boton_x1 <= x <= boton_x2 and boton_y1 <= y <= boton_y2:
                    # cv2.destroyAllWindows()
                    return

        cv2.imshow("Aimlab", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            exit()

screenWidth, screenHeight = pyautogui.size()
fondo_personalizado = cv2.imread("fondo.png")
fondo_personalizado = cv2.resize(fondo_personalizado, (screenWidth, screenHeight))

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

mp_selfie_segmentation = mp.solutions.selfie_segmentation
segmentacion = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, screenWidth)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screenHeight)

# Bucle principal del juego donde:
# - 1. Se muestra la pantalla de inicio
# - 2. Cuenta regresiva
# - 3. Ejecución del juego
# - 4. Se muestra la puntuación
# - 5. Se repite
while True:
    pantalla_inicio(hands, cap)
    cuenta_regresiva(cap)
    cv2.namedWindow("Aimlab", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Aimlab", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    pelotas = []
    vida_pelota = 3
    score = 0
    duracion_juego = 30
    tiempo_inicio = time.time()
    ultimo_spawn = 0
    ret, frame = cap.read()
    h, w, _ = frame.shape

    while True:

        # Las pelotas se dibujan y animan en pantalla. Si no se tocan 
        # en 3 segundos, desaparecen. Si el dedo las toca, suman puntos.
        tiempo_actual = time.time()
        tiempo_restante = int(duracion_juego - (tiempo_actual - tiempo_inicio))

        intervalo_spawn = calcular_intervalo(tiempo_restante, duracion_juego)
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

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resultado_segmentacion = segmentacion.process(frame_rgb)
        mascara = resultado_segmentacion.segmentation_mask
        condicion = mascara > 0.5
        fondo = fondo_personalizado.copy()
        fondo = cv2.GaussianBlur(fondo, (25, 25), 0)
        frame = np.where(condicion[..., None], frame, fondo)

        for pelota in pelotas:
            tiempo_vida_usado = time.time() - pelota["tiempo_creacion"]
            factor = max(0, 1 - (tiempo_vida_usado / vida_pelota))
            radio_animado = max(1, int(pelota["r"] * factor)) 
            dibujar_pelota_degradada(frame, pelota["x"], pelota["y"], radio_animado, (0, 0, 255), (0, 0, 100))      
              
        for pelota in pelotas[:]:
            if time.time() - pelota["tiempo_creacion"] > 3:
                pelotas.remove(pelota)

        result = hands.process(frame_rgb)

        # Buscamos que la punta del indice, referenciado como landmark[8] en
        # mediapipe, y busco la distancia a cada pelota para detectar colisiones.
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                x = int(hand_landmarks.landmark[8].x * screenWidth)
                y = int(hand_landmarks.landmark[8].y * screenHeight)

                cv2.circle(frame, (x, y), 10, (255, 0, 0), -1)

                for pelota in pelotas[:]:
                    dist = math.hypot(x - pelota["x"], y - pelota["y"])
                    if dist < pelota["r"]:
                        pelotas.remove(pelota)
                        score += 1

        # Puntuación
        cv2.putText(frame, f'Puntuacion: {score}', (10, 40), cv2.FONT_HERSHEY_COMPLEX, 1.2, (255, 255, 255), 2)
        
        # Tiempo restante
        cv2.putText(frame, f"Tiempo: {tiempo_restante}", (10, 80), cv2.FONT_HERSHEY_COMPLEX, 1.2, (0, 255, 255), 2)

        cv2.imshow("Aimlab", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    pantalla_final(score, hands, cap)