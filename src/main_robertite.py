import sys
sys.path.append("./data/")
sys.path.append("./utils/")
sys.path.append("./movement/")
sys.path.append("./fusion/")

import time
import matplotlib.pyplot as plt
import datetime
import numpy as np

from threading import Lock
import RPi.GPIO as GPIO

from Mpu6050 import Mpu6050
from Encoder import Encoder
from Rplidar import Rplidar
from motor import Motor
from save_data import save
from ClaseFiltroBayesiano import FiltroBayesiano
import numpy as np

# Desactivar las advertencias de pines GPIO en uso
GPIO.setwarnings(False)

scan_data_lock = Lock()

encoder = Encoder()
giro = Mpu6050()
motor = Motor(giro, encoder)
rplidar = Rplidar(scan_data_lock)

resultlazo = []
fb = FiltroBayesiano(160)
belief = fb.start()
time.sleep(1)
def recorrer_mapa(mapa, casilla_actual, belief, vector):
    print("Recorriendo mapa")
    motor.stop()

    #Gira 90 grados
    motor.rotate(-90)

    #Espera a que deje de rotar
    while motor.rotating:
        pass
    #Lee los datos del sensor de distancia
    time.sleep(1)
    datos_lidar = rplidar.get_data_polar_interval(165,195)
    time.sleep(1)

    #Analiza cuanto avanzo segun los encoders
    movement = fb.movement(encoder.contador1)
    encoder.contador1 = 0

    #Gausiana del encoder
    convolucion = fb.convolucion(belief,movement,True)

    #Gausiana del lidar
    model_sensor = fb.lidar_measure(datos_lidar)

    #Multiplicacion de las gausianas
    belief = fb.multiply_mov_sens(True)
    
    #Guarda el belief en el arreglo de avance
    resultlazo.append(belief)

    # Almacenar la distancia medida en el mapa
    casilla_actual = (int(casilla_actual[0] + vector[0] * belief / 10), int(casilla_actual[1] + vector[1] * belief / 10))
    mapa[casilla_actual] = 1

    print(casilla_actual)
    
    # Avanzar
    motor.avanzar(-50, -50)
    encoder.contador1 = 0
    while encoder.contador1 < 100:
        pass
    motor.stop()


with open("datos2.txt", 'w') as archivo:
    archivo.write("\nPrimer mapeo del espacio\n")
    archivo.write(str(rplidar.get_data_polar()) + "\n\n")

    def registrar_movimiento(descripcion, angulo_rotacion, pulsos_encoder):
        archivo.write(f"{descripcion}\n")
        motor.rotate(angulo_rotacion)
        while motor.rotating:
            pass
        archivo.write(str(rplidar.get_data_polar()) + "\n\n")
        
        archivo.write(f"Avance de {pulsos_encoder} pulsos de encoder\n")
        encoder.contador1 = 0
        motor.avanzar(-70, -70)
        while encoder.contador1 < pulsos_encoder:
            pass
        motor.stop()
        archivo.write(str(rplidar.get_data_polar()) + "\n\n")

    registrar_movimiento("giro de 35 grados", -35, 150)
    registrar_movimiento("giro de 90 grados", -90, 200)

    archivo.write("Fin de movimiento\n")




rplidar.cleanup()
