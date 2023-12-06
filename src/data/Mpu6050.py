import smbus
import time
import math
import RPi.GPIO as gpio

class Mpu6050:
    PWR_M   = 0x6B
    DIV     = 0x19
    CONFIG  = 0x1A
    GYRO_CONFIG  = 0x1B
    INT_EN   = 0x38
    ACCEL_X = 0x3B
    ACCEL_Y = 0x3D
    ACCEL_Z = 0x3F
    GYRO_X  = 0x43
    GYRO_Y  = 0x45
    GYRO_Z  = 0x47
    TEMP = 0x41
    
    def __init__(self, addr=0x68 ):
        self.AxCal=0
        self.AyCal=0
        self.AzCal=0
        self.GxCal=0
        self.GyCal=0
        self.GzCal=0
        self.Device_Address = addr
        self.bus = smbus.SMBus(1)
        self.bus.write_byte_data(self.Device_Address, self.DIV, 7)
        self.bus.write_byte_data(self.Device_Address, self.PWR_M, 1)
        self.bus.write_byte_data(self.Device_Address, self.CONFIG, 0)
        self.bus.write_byte_data(self.Device_Address, self.GYRO_CONFIG, 24)
        self.bus.write_byte_data(self.Device_Address, self.INT_EN, 1)
        #self.calibrate()
        time.sleep(1)

    def readMPU(self, addr):
        high = self.bus.read_byte_data(self.Device_Address, addr)
        low = self.bus.read_byte_data(self.Device_Address, addr+1)
        value = ((high << 8) | low)
        if(value > 32768):
            value = value - 65536
        return value
    
    def get_accel(self):
        x = self.readMPU(self.ACCEL_X)
        y = self.readMPU(self.ACCEL_Y)
        z = self.readMPU(self.ACCEL_Z)
        Ax = (x/16384.0-self.AxCal)
        Ay = (y/16384.0-self.AyCal)
        Az = (z/16384.0-self.AzCal)
        #print "X="+str(Ax)
        return [Ax,Ay,Az]

    def get_inclination (self):
        x = self.readMPU(self.ACCEL_X)
        y = self.readMPU(self.ACCEL_Y)
        z = self.readMPU(self.ACCEL_Z)
        Ax = (x/16384.0-self.AxCal)
        Ay = (y/16384.0-self.AyCal)
        Az = (z/16384.0-self.AzCal)
        x_rotation = math.degrees(math.atan2(float(Ay),math.sqrt((float(Ax)*float(Ax)) + (float(Az) * float(Az)))))
        y_rotation = -math.degrees(math.atan2(float(Ax),math.sqrt((float(Ay)*float(Ay)) + (float(Az) * float(Az)))))
        return [x_rotation,y_rotation]
    
    def get_gyro(self):
        x = self.readMPU(self.GYRO_X)
        y = self.readMPU(self.GYRO_Y)
        z = self.readMPU(self.GYRO_Z)
        Gx = x/131.0 - self.GxCal
        Gy = y/131.0 - self.GyCal
        Gz = z/131.0 - self.GzCal
        #print "X="+str(Gx)
        return [Gx,Gy,Gz]
    
    def get_temp(self):
        tempRow=self.readMPU(self.TEMP)
        tempC=(tempRow / 340.0) + 36.53
        tempC="%.2f" %tempC
        #print tempC
        return tempC
    
    
    def calibrate(self):
        x=0.
        y=0.
        z=0.
        for i in range(50):
            x = x + self.readMPU(self.ACCEL_X)
            y = y + self.readMPU(self.ACCEL_Y)
            z = z + self.readMPU(self.ACCEL_Z)
        x= x/50.0
        y= y/50.0
        z= z/50.0
        self.AxCal = x/16384.0
        self.AyCal = y/16384.0
        self.AzCal = z/16384.0
        
        x=0
        y=0
        z=0
        for i in range(50):
            x = x + self.readMPU(self.GYRO_X)
            y = y + self.readMPU(self.GYRO_Y)
            z = z + self.readMPU(self.GYRO_Z)
        x= x/50
        y= y/50
        z= z/50
        self.GxCal = x/131.0
        self.GyCal = y/131.0
        self.GzCal = z/131.0
