import RPi.GPIO as GPIO
import RPi_map

class Motor():
    
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(RPi_map.CLKWA0, GPIO.OUT)
        GPIO.setup(RPi_map.CLKWA1, GPIO.OUT)
        GPIO.setup(RPi_map.CLKWB0, GPIO.OUT)
        GPIO.setup(RPi_map.CLKWB1, GPIO.OUT)


        # Configura los pines GPIO como salidas PWM
        GPIO.setup(12, GPIO.OUT)
        GPIO.setup(33, GPIO.OUT)
        # Configura la frecuencia PWM (en Hz)
        pwm_frequency = 1000  # Puedes ajustar esta frecuencia según tus necesidades

        # Crea objetos PWM para los pines GPIO
        self.pwm_12 = GPIO.PWM(12, pwm_frequency)
        self.pwm_33 = GPIO.PWM(33, pwm_frequency)


    def avanzar(self,pwm1=50,pwm2=50):

        # Inicia el PWM con un ciclo de trabajo del pot% (máximo)
        self.pwm_12.start(abs(pwm1))
        self.pwm_33.start(abs(pwm2))

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
        self.avanzar(0,0)
