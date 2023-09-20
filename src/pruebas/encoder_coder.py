#75 pulsos por vuelta cada interrupcion
#60 mm de diametro c/ rueda
#2.512 mm avanzados de forma lineal por pulso medido

import RPi_map
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(RPi_map.ENCODER_A0, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RPi_map.ENCODER_A1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RPi_map.ENCODER_B0, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RPi_map.ENCODER_B1, GPIO.IN, pull_up_down=GPIO.PUD_UP)


contador1 = 0
contador2 = 0

def mi_funcion_interrupcion(channel):
    if channel == 31:
        global contador1
        contador1 += 1
        print("contador 1 = " + str(contador1))
    elif channel == 22:
        global contador2
        contador2 += 1
        print("contador 2 = " + str(contador2))
    
# Configurar la interrupción en el pin especificado (flanco de subida)
GPIO.add_event_detect(RPi_map.ENCODER_B0, GPIO.RISING, callback=mi_funcion_interrupcion)
GPIO.add_event_detect(RPi_map.ENCODER_B1, GPIO.RISING, callback=mi_funcion_interrupcion)
GPIO.add_event_detect(RPi_map.ENCODER_A0, GPIO.RISING, callback=mi_funcion_interrupcion)
GPIO.add_event_detect(RPi_map.ENCODER_A1, GPIO.RISING, callback=mi_funcion_interrupcion)


while True:
    time.sleep(1)
    print("Esperando interrupciones...")