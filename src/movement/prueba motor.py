from motor import Motor
from Mpu6050 import Mpu6050
import time
from Encoder import Encoder

encoder = Encoder()
giro = Mpu6050()

giro.calibrate()
motor = Motor(giro,encoder)
motor.polar_control(-720,30)