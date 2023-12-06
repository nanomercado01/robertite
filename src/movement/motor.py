import RPi.GPIO as GPIO
import RPi_map
import sys
sys.path.append("../data/")
from Mpu6050 import Mpu6050
import math
import threading

giro = Mpu6050()

TIME_INT0    = 0.1 # en segundos

class Motor():
    
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(RPi_map.CLKWA0, GPIO.OUT)
        GPIO.setup(RPi_map.CLKWA1, GPIO.OUT)
        GPIO.setup(RPi_map.CLKWB0, GPIO.OUT)
        GPIO.setup(RPi_map.CLKWB1, GPIO.OUT)


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
        
        self.time_thread = threading.Timer(TIME_INT0,self.timer_interrupt)
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
    
    def polar_control(self, distancia, angulo, potencia = 50):
        potencia /= 2 #Esto hago para  que la funcion reciba un % de potencia entre 0%-100% donde el 100% corresponde a un pwm de 50.
        #giro.calibrate()
        # Obtener lecturas del acelerómetro
        lecturas = giro.get_accel()

        # Calcular el ángulo de inclinación en radianes
        angulo = math.atan2(lecturas['y'], math.sqrt(lecturas['x']**2 + lecturas['z']**2))

        # Convertir el ángulo a grados
        angulo_grados = math.degrees(angulo)

        # Imprimir el ángulo
        print(f"Ángulo de inclinación: {angulo_grados} grados")


    def stop(self):
        self.pwm_32.start(0)
        self.pwm_33.start(0)
        GPIO.output(RPi_map.CLKWA1,0)
        GPIO.output(RPi_map.CLKWA0,0)
        GPIO.output(RPi_map.CLKWB1,0)
        GPIO.output(RPi_map.CLKWB0,0)
        
        rotating = False
        
    def rotate(self, orientation):

        self.vel_motor_A = float(35)
        self.vel_motor_B = float(35)
        
        if ( (orientation - self.rotacion) < 0 ):
            GPIO.output(RPi_map.CLKWA0,1)
            GPIO.output(RPi_map.CLKWA1,0)        
            GPIO.output(RPi_map.CLKWB0,1)
            GPIO.output(RPi_map.CLKWB1,0)
        else:
            GPIO.output(RPi_map.CLKWA0,0)
            GPIO.output(RPi_map.CLKWA1,1)        
            GPIO.output(RPi_map.CLKWB0,0)
            GPIO.output(RPi_map.CLKWB1,1)

        self.pwm_32.start(self.vel_motor_A)
        self.pwm_33.start(self.vel_motor_B)

        self.rotating = True
        

    def timer_interrupt(self):

        # Rotacion
        # print("Rotacion Temp: %f"%gyro[2])
        # print("Rotacion accum: %f"%self.rotacion)
        velocidades = giro.get_gyro()
        print(velocidades)
        if (abs(velocidades[2]) > 1 ): # FIXME: Filtra el cambio de grados chicos, puede llevar a drifs #Umbral de error = 1
            self.rotacion += gyro[2] * 0.1 #Intervalo de tiempo en cada interrupcion(delta t)
            print(self.rotacion)

        if ( rotating == True ):
             if ( abs(self.rotacion - self.rotacion_target) < 5  ): #Umbral de error para acercarse al target: 5 grados
                 self.stop()

        '''if ( LOG_CONTROL == True ):
            self.log_control_file.write("%f %f %f %f %f %f %f %f %f\n"%(process_time(),self.distancia_target,self.distancia_tmp,self.rotacion,self.rotacion_target,gyro[2],self.vel_motor_A,self.vel_motor_B,self.moving))
        '''         
        self.time_thread.cancel()
        self.time_thread = threading.Timer(TIME_INT0,timer_interrupt)
        self.time_thread.start()

