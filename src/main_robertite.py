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
'''
def recorrer_mapa(mapa, casilla_actual, belief, vector, vuelta):
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

    #Gaussiana del encoder
    convolucion = fb.convolucion(belief,movement)

    #Gaussiana del lidar
    model_sensor = fb.lidar_measure(datos_lidar)

    #Multiplicacion de las gausianas
    belief = fb.multiply_mov_sens()
    
    #Guarda el belief en el arreglo de avance
    resultlazo.append(belief)

    # Almacenar la distancia medida en el mapa
    casilla_actual = (int(casilla_actual[0] + vector[0] * np.argmax(belief) / 10), int(casilla_actual[1] + vector[1] * np.argmax(belief) / 10))
    mapa[casilla_actual] = 1
    print(casilla_actual)
    
    # Avanzar
    motor.avanzar(-40, -40)
    encoder.contador1 = 0
    while encoder.contador1 < 30 * vuelta:
        pass
    motor.stop()
    
    return casilla_actual
# Definir el tamaño del mapa
tamanio_mapa = 22
mapa = np.zeros((tamanio_mapa, tamanio_mapa), dtype=int)
casilla_actual = (tamanio_mapa // 2, tamanio_mapa // 2)
vector = (1,1)
vuelta = 1
# Repetir el proceso hasta que el 60% del mapa este explorado

# Inicializar el arreglo de vectores
arreglo_vectores = np.array([[0, 1], [1, 0], [0, -1], [-1, 0]])
with open("datos.txt", 'wb') as archivo:
    while (mapa.sum() / mapa.size) < 0.6:
        #Hace una medicion para cada lado e imprime el mapa
        for i in range(4):
            casilla_actual=recorrer_mapa(mapa, casilla_actual, belief, arreglo_vectores[i], vuelta)
            vuelta *= 1.2
        print(mapa)
        np.savetxt(archivo, mapa, fmt="%d", delimiter=",")

plt.xlim([0,200])
plt.title("Distribución Resultante")
plt.ylabel("Amplitude")
plt.xlabel("Posición")
plt.show()

print("La posicion final del robot es: ",np.argmax(resultlazo[len(resultlazo)-1]))

'''
motor.stop()
print("comenzando")

time.sleep(4)
datos_mapa = rplidar.get_data_polar_interval(0,360)
with open("datos.txt", 'a') as archivo:
    archivo.write(str(datos_mapa))
motor.avanzar(-40,-40)
while(encoder.contador1 < 100):
    pass
motor.stop()
time.sleep(1)
datos_mapa = rplidar.get_data_polar_interval(0,360)
with open("datos.txt", 'a') as archivo:
    archivo.write(str(datos_mapa) + "\n")
    archivo.write("\n 100 pulsos de encoder\n")
for i in range(3):
    motor.rotate(90)
    while(motor.rotating):
        pass
    motor.avanzar(-40,-40)
    encoder.contador1 = 0
    while(encoder.contador1 < 100):
        pass
    motor.stop()
    time.sleep(1)
    datos_mapa = rplidar.get_data_polar_interval(0,360)
    with open("datos.txt", 'a') as archivo:
        archivo.write("\n\n\n giro de 90 grados y avance de 100 pulsos\n")
        archivo.write(str(datos_mapa))

#guardar los datos en el archivo datos.txt
# Abrir el archivo en modo de escritura
    # guardar el mapa
rplidar.cleanup()


