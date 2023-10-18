import sys
sys.path.append("./data/")
sys.path.append("./utils/")
from Mpu6050 import Mpu6050
import time
import RPi.GPIO as GPIO
from threading import Lock
import matplotlib.pyplot as plt
import datetime
from Encoder import Encoder
from Rplidar import Rplidar

scan_data_lock = Lock()

encoder = Encoder()
giro = Mpu6050()
rplidar = Rplidar(scan_data_lock)

rplidar.stop_motor()

