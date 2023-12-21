import RPi.GPIO as GPIO
import RPi_map
import sys
sys.path.append("../data/")
from Mpu6050 import Mpu6050
import math
import threading
from Encoder import Encoder



 # en segundos

class Motor():
    
    def __init__(self,giro,encoder):
        GPIO.setmode(GPIO.BOARD)
        
        GPIO.setwarnings(False)
        GPIO.setup(RPi_map.CLKWA0, GPIO.OUT)
        GPIO.setup(RPi_map.CLKWA1, GPIO.OUT)
        GPIO.setup(RPi_map.CLKWB0, GPIO.OUT)
        GPIO.setup(RPi_map.CLKWB1, GPIO.OUT)
        

        #Sensores
        self.giro = giro
        self.encoder = encoder
        
        # Configura los pines GPIO como salidas PWM
        GPIO.setup(32, GPIO.OUT)
        GPIO.setup(33, GPIO.OUT)
        # Configura la frecuencia PWM (en Hz)
        pwm_frequency = 1000  # Puedes ajustar esta frecuencia según tus necesidades

        # Crea objetos PWM para los pines GPIO
        self.pwm_32 = GPIO.PWM(32, pwm_frequency)
        self.pwm_33 = GPIO.PWM(33, pwm_frequency)

    
        self.rotating = False
        self.moving = False
        self.rotacion = 0.0
        
        self.TIME_INT0    = 0.1
        self.time_thread = threading.Timer(self.TIME_INT0,self.timer_interrupt)
        self.time_thread.start()

    def avanzar(self,pwm1=50,pwm2=50):

        # Inicia el PWM con un ciclo de trabajo del pot% (máximo)
        self.pwm_32.start(abs(pwm1))
        self.pwm_33.start(abs(pwm2))
        
        self.moving = True

        if (pwm1 > 0):
            GPIO.output(RPi_map.CLKWA0,1)
            GPIO.output(RPi_map.CLKWA1,0)
        else:
            GPIO.output(RPi_map.CLKWA0,0)
            GPIO.output(RPi_map.CLKWA1,1) 
            
        if (pwm2 > 0):
            GPIO.output(RPi_map.CLKWB0,1)
            GPIO.output(RPi_map.CLKWB1,0)
        else:
            GPIO.output(RPi_map.CLKWB0,0)
            GPIO.output(RPi_map.CLKWB1,1)


    def stop(self):
        self.pwm_32.start(0)
        self.pwm_33.start(0)
        GPIO.output(RPi_map.CLKWA1,0)
        GPIO.output(RPi_map.CLKWA0,0)
        GPIO.output(RPi_map.CLKWB1,0)
        GPIO.output(RPi_map.CLKWB0,0)
        
        self.rotating = False
        self.moving = False
    
    
    def polar_control(self,phi1,fase):
        self.stop()
        cant_pul = round((fase*10)/2.512)
        self.rotate(phi1)
        while(self.rotating):
            pass
        self.encoder.contador1 = 0
        while(self.encoder.contador1<cant_pul):
            self.avanzar(-50,-50)
        self.stop()
        
    
    def rotate(self, orientation):

        self.rotacion_target = orientation
        self.rotacion = 0
        if ( (self.rotacion_target - self.rotacion) < 0 ):
            self.avanzar(70,-70)
        else:
            self.avanzar(-70,70)

        
        self.rotating = True
        

    def timer_interrupt(self):

        # Rotacion
        # print("Rotacion Temp: %f"%gyro[2])
        # print("Rotacion accum: %f"%self.rotacion)
        velocidades = self.giro.get_gyro()
        #print(velocidades)
        if (abs(velocidades[2]) > 0.1 ): # FIXME: Filtra el cambio de grados chicos, puede llevar a drifs #Umbral de error = 1
            self.rotacion += velocidades[2] * self.TIME_INT0 * 1.15 #Intervalo de tiempo en cada interrupcion(delta t)

        if ( self.rotating == True ):
             if ( abs(self.rotacion - self.rotacion_target) < 10  ): #Umbral de error para acercarse al target: 5 grados
                 self.stop()

        '''if ( LOG_CONTROL == True ):
            self.log_control_file.write("%f %f %f %f %f %f %f %f %f\n"%(process_time(),self.distancia_target,self.distancia_tmp,self.rotacion,self.rotacion_target,gyro[2],self.vel_motor_A,self.vel_motor_B,self.moving))
        '''         
        self.time_thread.cancel()
        self.time_thread = threading.Timer(self.TIME_INT0,self.timer_interrupt)
        self.time_thread.start()

