import cv2
from core.utils import cuenta_regresiva, calcular_intervalo
import time
from core.pelota import nueva_pelota, dibujar_pelota_degradada
from config import screenHeight, screenWidth, vida_pelota, duracion_juego, color_pelota_borde_azul, color_pelota_centro_azul
import math
import pygame

# Ejecuta el juego y devuelve la puntación obtenida
def ejecutar_juego(hands, cap):
    cuenta_regresiva(cap)
    cv2.namedWindow("Aimlab", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Aimlab", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    pop_sound = pygame.mixer.Sound("assets/audio/pop-sound-effect.mp3")
    pelotas = []
    score = 0
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
        # resultado_segmentacion = segmentacion.process(frame_rgb)
        # mascara = resultado_segmentacion.segmentation_mask
        # condicion = mascara > 0.5
        # fondo = fondo_personalizado.copy()
        # fondo = cv2.GaussianBlur(fondo, (25, 25), 0)
        # frame = np.where(condicion[..., None], frame, fondo)

        for pelota in pelotas:
            tiempo_vida_usado = time.time() - pelota["tiempo_creacion"]
            factor = max(0, 1 - (tiempo_vida_usado / vida_pelota))
            radio_animado = max(1, int(pelota["r"] * factor))

            if pelota["tipo"] == "normal":
                color_pelota_centro = color_pelota_centro_azul
                color_pelota_borde = color_pelota_borde_azul
            elif pelota["tipo"] == "dorada":
                color_pelota_centro = (0, 215, 255)
                color_pelota_borde = (0, 150, 200)
            elif pelota["tipo"] == "roja":
                color_pelota_centro = (0, 0, 255)
                color_pelota_borde = (0, 0, 255)

            dibujar_pelota_degradada(frame, pelota["x"], pelota["y"], radio_animado, color_pelota_centro, color_pelota_borde)      
              
        for pelota in pelotas[:]:
            if time.time() - pelota["tiempo_creacion"] > vida_pelota:
                pelotas.remove(pelota)

        result = hands.process(frame_rgb)

        # Buscamos que la punta del indice, referenciado como landmark[8] en
        # mediapipe, y busco la distancia a cada pelota para detectar colisiones.
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                # Pasar por la función mp_draw y mp_hands si lo voy a utilizar
                # mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                x = int(hand_landmarks.landmark[8].x * screenWidth)
                y = int(hand_landmarks.landmark[8].y * screenHeight)

                cv2.circle(frame, (x, y), 10, (255, 0, 0), -1)

                for pelota in pelotas[:]:
                    dist = math.hypot(x - pelota["x"], y - pelota["y"])
                    if dist < pelota["r"]:
                        if pelota["tipo"] == "normal":
                            score += 1
                            pop_sound.play()
                        elif pelota["tipo"] == "dorada":
                            # Añadir sonido de oro
                            score += 3
                            pop_sound.play()
                        elif pelota["tipo"] == "roja":
                            score -= 1
                            # Añadir sonido de fallo
                            pop_sound.play()
                        
                        pelotas.remove(pelota)

        # Puntuación
        cv2.putText(frame, f'Puntuacion: {score}', (10, 40), cv2.FONT_HERSHEY_COMPLEX, 1.2, (255, 255, 255), 2)
        
        # Tiempo restante
        cv2.putText(frame, f"Tiempo: {tiempo_restante}", (10, 80), cv2.FONT_HERSHEY_COMPLEX, 1.2, (0, 255, 255), 2)

        # Leyenda de tipos de pelotas
        cv2.circle(frame, (screenWidth - 250, 30), 20, color_pelota_centro_azul, -1)
        cv2.putText(frame, "+1", (screenWidth - 230, 37), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.circle(frame, (screenWidth - 250, 70), 20, (0, 215, 255), -1)
        cv2.putText(frame, "+3", (screenWidth - 230, 77), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.circle(frame, (screenWidth - 250, 110), 20, (0, 0, 255), -1)
        cv2.putText(frame, "-1", (screenWidth - 230, 117), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)


        cv2.imshow("Aimlab", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    
    return score