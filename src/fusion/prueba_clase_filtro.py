import sys
sys.path.append("../movement/")
sys.path.append("../data/")

from ClaseFiltroBayesiano import FiltroBayesiano 
import numpy as np
from scipy import signal
from scipy.fftpack import fft, fftshift
import matplotlib.pyplot as plt
from scipy.stats import norm
from motor import Motor
from Encoder import Encoder
from save_data import save
from Rplidar import Rplidar
from threading import Lock
import time

print(time.time())

scan_data_lock = Lock()
rplidar = Rplidar(scan_data_lock)

fb = FiltroBayesiano(52)
belief = fb.start()
movement = fb.movement(20)
convolucion = fb.convolucion(belief,movement)

time.sleep(1)
datos_lidar = rplidar.get_data_polar_interval(165,195)
time.sleep(1)

model_sensor = fb.lidar_measure(datos_lidar)

fb.multiply_mov_sens()

print(time.time())
