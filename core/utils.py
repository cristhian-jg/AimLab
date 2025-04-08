from config import screenHeight, screenWidth
import cv2
import time
import pygame
from config import color_pelota_centro_azul

# Reproducción de sonido
pygame.mixer.init()
start_sound = pygame.mixer.Sound("assets/audio/arcade-countdown.mp3")

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

# Cuenta regresiva (3...2...1...YA!) que se ejecuta al señalar el botón
#  jugar, será util para que el jugador se prepare.
def cuenta_regresiva(cap):
    start_sound.play()
    for i in range(3, 0, -1):
        frame = cap.read()[1]
        if frame is None:
            continue
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (screenWidth, screenHeight))
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # resultado_segmentacion = segmentacion.process(frame_rgb)
        # mascara = resultado_segmentacion.segmentation_mask
        # condicion = mascara > 0.5
        # fondo = fondo_personalizado.copy()
        # fondo = cv2.GaussianBlur(fondo, (25, 25), 0)
        # frame = np.where(condicion[..., None], frame, fondo)
        cv2.putText(frame, str(i), (screenWidth // 2 - 50, screenHeight // 2), cv2.FONT_HERSHEY_DUPLEX, 5,  (0, 255, 0), 5)

        inicio = time.time()
        while time.time() - inicio < 1:
            frame_loop = cap.read()[1]
            if frame_loop is None:
                continue
            frame_loop = cv2.flip(frame_loop, 1)
            frame_loop = cv2.resize(frame_loop, (screenWidth, screenHeight))
            frame_rgb = cv2.cvtColor(frame_loop, cv2.COLOR_BGR2RGB)
            # resultado_segmentacion = segmentacion.process(frame_rgb)
            # mascara = resultado_segmentacion.segmentation_mask
            # condicion = mascara > 0.5
            # fondo = fondo_personalizado.copy()
            # fondo = cv2.GaussianBlur(fondo, (25, 25), 0)
            # frame_loop = np.where(condicion[..., None], frame_loop, fondo)
            cv2.putText(frame_loop, str(i), (screenWidth // 2 - 50, screenHeight // 2), cv2.FONT_HERSHEY_DUPLEX, 5,  (0, 255, 0), 5)
            cv2.imshow("Aimlab", frame_loop)
            if cv2.waitKey(1) & 0xFF == 27:
                exit()

    frame = cap.read()[1]

    if frame is not None:
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (screenWidth, screenHeight))
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # resultado_segmentacion = segmentacion.process(frame_rgb)
        # mascara = resultado_segmentacion.segmentation_mask
        # condicion = mascara > 0.5
        # fondo = fondo_personalizado.copy()
        # fondo = cv2.GaussianBlur(fondo, (25, 25), 0)
        # frame = np.where(condicion[..., None], frame, fondo)
        cv2.putText(frame, "YA!", (screenWidth // 2 - 100, screenHeight // 2), cv2.FONT_HERSHEY_DUPLEX, 5, (0, 255, 255), 5)
        
        inicio = time.time()
        while time.time() - inicio < 1:
            frame_loop = cap.read()[1]
            if frame_loop is None:
                continue
            frame_loop = cv2.flip(frame_loop, 1)
            frame_loop = cv2.resize(frame_loop, (screenWidth, screenHeight))
            frame_rgb = cv2.cvtColor(frame_loop, cv2.COLOR_BGR2RGB)
            # resultado_segmentacion = segmentacion.process(frame_rgb)
            # mascara = resultado_segmentacion.segmentation_mask
            # condicion = mascara > 0.5
            # fondo = fondo_personalizado.copy()
            # fondo = cv2.GaussianBlur(fondo, (25, 25), 0)
            # frame_loop = np.where(condicion[..., None], frame_loop, fondo)
            cv2.putText(frame_loop, "YA!", (screenWidth // 2 - 100, screenHeight // 2), cv2.FONT_HERSHEY_DUPLEX, 5, (0, 255, 255), 5)

            cv2.imshow("Aimlab", frame_loop)
            if cv2.waitKey(1) & 0xFF == 27:
                exit()


# Hace que la velocidad de aparición de las pelotas aumente con el paso del tiempo
def calcular_intervalo(tiempo_restante, duracion_juego):
    progreso = 1 - (tiempo_restante / duracion_juego)
    return max(0.2, 1 - progreso * 0.8)
