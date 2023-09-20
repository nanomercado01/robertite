import sys
from Mpu6050 import Mpu6050
import time
import RPi.GPIO as GPIO
import RPi_map
from threading import Lock
import matplotlib.pyplot as plt
import datetime
from giro import datos_giro
from funciones_lidar_main import datos_lidar
import datos_sensores
from encoder_coder import Encoder
from Rplidar import Rplidar

rplidar = Rplidar('/dev/ttyUSB0', scan_data_lock, display = True)


sys.path.append('/home/pi/robertite/src/pruebas/giro.py')
sys.path.append('/home/pi/robertite/src/pruebas/funciones_lidar_main.py')
sys.path.append('/home/pi/robertite/src/pruebas/datos_sensores.py')


encoder = Encoder()

dato_giro = datos_giro()
dato_lidar = datos_lidar()

datos_sensores.guardar_en_archivo(dato_giro,dato_lidar)

rplidar.cleanup()

#lidar.grafico_lidar(lidar.datos_lidar())
