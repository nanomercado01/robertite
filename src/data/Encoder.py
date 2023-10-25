#75 pulsos por vuelta cada interrupcion
#60 mm de diametro c/ rueda
#2.512 mm avanzados de forma lineal por pulso medido

import RPi_map
import RPi.GPIO as GPIO
import time

class Encoder():


    def __init__(self):
        
        self.contador1 = 0
        self.contador2 = 0    
    
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(RPi_map.ENCODER_A0, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(RPi_map.ENCODER_A1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(RPi_map.ENCODER_B0, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(RPi_map.ENCODER_B1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # Configurar la interrupción en el pin especificado (flanco de subida)
        GPIO.add_event_detect(RPi_map.ENCODER_B0, GPIO.RISING, callback=self.funcion_interrupcion)
        GPIO.add_event_detect(RPi_map.ENCODER_B1, GPIO.RISING, callback=self.funcion_interrupcion)
        GPIO.add_event_detect(RPi_map.ENCODER_A0, GPIO.RISING, callback=self.funcion_interrupcion)
        GPIO.add_event_detect(RPi_map.ENCODER_A1, GPIO.RISING, callback=self.funcion_interrupcion)

    def funcion_interrupcion(self,channel):
        if channel == 31:
            self.contador1 += 1
        elif channel == 22:
            self.contador2 += 1
