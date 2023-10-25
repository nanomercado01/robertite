import sys
sys.path.append("./data/")
sys.path.append("./utils/")
sys.path.append("./movement/")

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

# Desactivar las advertencias de pines GPIO en uso
GPIO.setwarnings(False)

scan_data_lock = Lock()

encoder = Encoder()
motor = Motor()
rplidar = Rplidar(scan_data_lock)
giro = Mpu6050()

counter = 0
guardado = False  # Variable para rastrear si se ha guardado
erase()

while encoder.contador1 <= 75 +1:
    motor.avanzar(60, 60)
    print(encoder.contador1)

    if encoder.contador1 % 75 == 1 and not guardado:
        save(giro.get_accel(), rplidar.get_data())
        print("guardado " + str(counter) + " veces")
        counter += 1
        guardado = True  # Marcamos que se ha guardado

    if encoder.contador1 % 75 != 1:
        guardado = False  # Restablecemos el estado de guardado

print("terminado")

motor.stop()

