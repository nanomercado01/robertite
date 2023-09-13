import sys
import time

sys.path.append('/home/pi/robertite/src/pruebas/Mpu6050.py')

from Mpu6050 import Mpu6050

giro = Mpu6050()

while True:
    print(giro.get_accel())
    time.sleep(1)


