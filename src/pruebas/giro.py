import sys
import time

sys.path.append('/home/pi/robertite/src/pruebas/Mpu6050.py')

from Mpu6050 import Mpu6050

#giro = Mpu6050()

'''
while True:
    print(giro.get_accel())
    time.sleep(1)
'''

def datos_giro ():
    time.sleep(1)
    return(Mpu6050().get_accel())

