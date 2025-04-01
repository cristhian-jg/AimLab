# AimLab con Visión Artificial

Juego interactivo de puntería desarrollado en Python. Usa el dedo índice como puntero para destruir pelotas que van apareciendo en pantalla.

---

## ¿Cómo funciona?

- Utiliza **MediaPipe** para detectar la mano y el dedo índice.
- Las pelotas aparecen y desaparecen en pantalla de forma aleatoria.
- Apunta con tu dedo: si lo acercas a una pelota, la destruyes.

---

## Tecnologías usadas

- Python 3.9.21
- OpenCV (visualización y detección de colisiones)
- MediaPipe (detección de mano)
- PyGame (para efectos de sonido)

---

## Cómo ejecutar el juego

1. Clona o descarga este repositorio
2. Crea y activa un entorno virtual (recomendado):

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # en Mac o Linux
   .venv\Scripts\activate     # en Windows
3. Instala las dependencias
    ```bash 
    pip install -r requirements.txt
4. Ejecuta el juego
    ```bash
    python main.py

Desarrollado por @cristhian-jg como proyecto de visión artificial para un instituto.  