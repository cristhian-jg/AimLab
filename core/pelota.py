import time
import random
import cv2

# Crea una nueva pelota con un radio concreto y su tiempo de creación.
def nueva_pelota(w, h):
    # Devuelve un diccionario con la posición de la pelota, el radio y el momento de la creación.    
    return {
        "x": random.randint(100, w - 100),
        "y": random.randint(100, h - 100),
        "r": 60,
        "tiempo_creacion": time.time()
    }

# Le da un estilo degradado a la pelota
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