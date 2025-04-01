# Librerías utilizadas para camámara, manos,
# colisiones, animaciones y tiempo

import cv2
import mediapipe as mp
# import pyautogui
# from screeninfo import get_monitors
from config import screenHeight, screenWidth
from core.interfaz import pantalla_inicio, pantalla_final
from core.game import ejecutar_juego

# Dimensiones de pantalla y fondo

#monitor = get_monitors()[0]
# fondo_personalizado = cv2.imread("fondo.png")
# fondo_personalizado = cv2.resize(fondo_personalizado, (screenWidth, screenHeight))

# Detección de manos
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Detección de cuerpos completos
# mp_selfie_segmentation = mp.solutions.selfie_segmentation
# segmentacion = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

# Captura de cámara
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
    score = ejecutar_juego(hands, cap, mp_draw, mp_hands)
    pantalla_final(score, hands, cap)