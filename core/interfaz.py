from config import screenWidth, screenHeight, color_pelota_centro, color_pelota_borde
import cv2
import random
from core.pelota import dibujar_pelota_degradada
from core.puntuacion import guardar_puntuacion
import numpy as np
import pygame

# pygame.mixer.init()
# pygame.mixer.music.load("assets/audio/main_music.mp3") 
# pygame.mixer.music.set_volume(0.05)
# pygame.mixer.music.play(-1)

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

    # Arreglo y bucle para generar pelotas de fondo en la pantalla de inicio
    pelotas_fondo = []
    for _ in range(20):
        pelota = {
            "x": random.randint(0, screenWidth),
            "y": random.randint(0, screenHeight),
            "vx": random.choice([-1, 1]) * random.uniform(3.5, 6.0),
            "vy": random.choice([-1, 1]) * random.uniform(3.5, 6.0),
            "r": random.randint(20, 40)
        }
        pelotas_fondo.append(pelota)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Las pelotas que generé antes las dibujo de 
        # manera que roboten en la pantalla
        for pelota in pelotas_fondo:
            pelota["x"] += pelota["vx"]
            pelota["y"] += pelota["vy"]

            if pelota["x"] < 0 or pelota["x"] > screenWidth:
                pelota["vx"] *= -1
            if pelota["y"] < 0 or pelota["y"] > screenHeight:
                pelota["vy"] *= -1
            dibujar_pelota_degradada(frame, int(pelota["x"]), int(pelota["y"]), pelota["r"], color_pelota_centro, color_pelota_borde)

        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (screenWidth, screenHeight))
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # resultado_segmentacion = segmentacion.process(frame_rgb)
        # mascara = resultado_segmentacion.segmentation_mask
        # condicion = mascara > 0.5
        # fondo = fondo_personalizado.copy()
        # fondo = cv2.GaussianBlur(fondo, (25, 25), 0)
        # frame = np.where(condicion[..., None], frame, fondo)
        
        result = hands.process(frame_rgb)

        cv2.putText(frame, "AimLab", (screenWidth // 2 - 200, 100), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 0, 0), 4)

        cv2.putText(frame, "Toca 'JUGAR' con tu dedo", (screenWidth // 2 - 200, screenHeight // 2 - 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(frame, "Elimina todas las pelotas que puedas", (screenWidth // 2 - 250, screenHeight // 2 - 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.putText(frame, "Desarrollado por C.J Gonzalez", (20, screenHeight - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        try:
            with open("ranking.txt", "r") as f:
                record = int(f.readline().strip())
                cv2.putText(frame, f"Record del Instituto: {record} pts", (screenWidth - 500, 80), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)
        except:
            pass

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
                    # FADE OUT
                    for alpha in range(0, 255, 5):
                        fade = frame.copy()
                        negro = np.zeros_like(frame)
                        fade = cv2.addWeighted(fade, 1 - alpha / 255, negro, alpha / 255, 0)
                        cv2.imshow("Aimlab", fade)
                        if cv2.waitKey(30) & 0xFF == 27:
                            exit()
                    return
        
        # Muestra la ventana
        cv2.imshow("Aimlab", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            exit()

# Muestra la ultima pantalla donde aparecen la puntuación
# obtenido y puedes volver a jugar.
def pantalla_final(score, hands, cap):
    cv2.namedWindow("Aimlab", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Aimlab", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    puntuaciones = guardar_puntuacion("ranking.txt", score)

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
        # resultado_segmentacion = segmentacion.process(frame_rgb)
        # mascara = resultado_segmentacion.segmentation_mask
        # condicion = mascara > 0.5
        # fondo = fondo_personalizado.copy()
        # fondo = cv2.GaussianBlur(fondo, (25, 25), 0)
        # frame = np.where(condicion[..., None], frame, fondo)
        result = hands.process(frame_rgb)

        cv2.putText(frame, f"Puntuacion final: {score}", (130, 150), cv2.FONT_HERSHEY_COMPLEX, 1.2, (255, 255, 255), 2)
        cv2.putText(frame, "Pulsa Play para jugar otra vez", (110, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # Mostrar el ranking de puntuaciones (top 5)
        cv2.putText(frame, "Ranking:", (130, 250), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
        for i, p in enumerate(puntuaciones):
            texto = f"{i + 1}. {p} puntos"
            cv2.putText(frame, texto, (130, 290 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 255, 255), 2)

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