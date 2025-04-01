# Guarda en un archivo las 5 mejores puntuaciones
def guardar_puntuacion(archivo, puntuacion):
    try:
        with open(archivo, "r") as f:
            puntuaciones = [int(line.strip()) for line in f.readlines()]
    except FileNotFoundError:
        puntuaciones = []

    puntuaciones.append(puntuacion)
    puntuaciones = sorted(puntuaciones, reverse=True)[:5]
    
    with open(archivo, "w") as f:
        for puntuacion in puntuaciones:
            f.write(f"{puntuacion}\n")

    return puntuaciones
