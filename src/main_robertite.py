import sys
sys.path.append("./data/")
sys.path.append("./utils/")
sys.path.append("./movement/")
sys.path.append("./fusion/")

import time
import matplotlib.pyplot as plt
import datetime

from threading import Lock
import RPi.GPIO as GPIO

from Mpu6050 import Mpu6050
from Encoder import Encoder
from Rplidar import Rplidar
from motor import Motor
from save_data import save
from ClaseFiltroBayesiano import FiltroBayesiano

# Desactivar las advertencias de pines GPIO en uso
GPIO.setwarnings(False)

scan_data_lock = Lock()

encoder = Encoder()
motor = Motor()
rplidar = Rplidar(scan_data_lock)
giro = Mpu6050()

#Avanzo 30cm(120 pulsos) y detengo el movimiento, de ahi obtengo los datos del encoder y los mando al filtro bayesiano

motor.avanzar(20,20)
while encoder.contador1 < 20:
    print(encoder.contador1)
motor.stop()

fb = FiltroBayesiano(52)
belief = fb.start()
movement = fb.movement(20)
convolucion = fb.convolucion(belief,movement)

time.sleep(1)
datos_lidar = rplidar.get_data_polar_interval(165,195)
time.sleep(1)
model_sensor = fb.lidar_measure(datos_lidar)

fb.multiply_mov_sens()

print(fb.posteriori)

#motor.rotate(20)

 
rplidar.cleanup()




''' ##Codigo comentado : prueba del miercoles 15/11, hace avanzar el motor, luego cambia direcciones 5 veces##

counter = 0
guardado = False  # Variable para rastrear si se ha guardado
#erase()
limit_pulse = 2
while encoder.contador1 <= limit_pulse +1:
    motor.avanzar(-20, 20)
    print(encoder.contador1)

    if encoder.contador1 % limit_pulse == 1 and not guardado:
        save(giro.get_accel(), rplidar.get_data())
        print("guardado " + str(counter) + " veces")
        counter += 1
        guardado = True  # Marcamos que se ha guardado

    if encoder.contador1 % 75 != 1:
        guardado = False  # Restablecemos el estado de guardado

motor1 = 20
motor2 = 20
for i in range(5):
    print("Cambio de direccion")
    time.sleep(1)
    motor1 *= -1
    motor.avanzar(motor1, motor2)
    print("Cambio de direccion")
    time.sleep(1)
    motor2 *= -1
    motor.avanzar(motor1, motor2)
print("terminado")
'''
