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

scan_data_lock = Lock()

encoder = Encoder()
motor = Motor()

motor.avanzar()

while encoder.contador1<40:
    #print("Avanzando")
    pass

print ("terminado")

motor.avanzar(0,0)
#giro = Mpu6050()
#rplidar = Rplidar(scan_data_lock)

#rplidar.stop_motor()
#rplidar.cleanup()

