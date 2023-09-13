import RPi_map
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(RPi_map.ENCODER_A0, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RPi_map.ENCODER_A1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RPi_map.ENCODER_B0, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RPi_map.ENCODER_B1, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def mi_funcion_interrupcion(channel):
    print("Interrupción detectada en el pin", channel)
    
# Configurar la interrupción en el pin especificado (flanco de subida)
GPIO.add_event_detect(RPi_map.ENCODER_B0, GPIO.RISING, callback=mi_funcion_interrupcion)
GPIO.add_event_detect(RPi_map.ENCODER_B1, GPIO.RISING, callback=mi_funcion_interrupcion)
GPIO.add_event_detect(RPi_map.ENCODER_A1, GPIO.RISING, callback=mi_funcion_interrupcion)

while True:
    time.sleep(1)
    print("Esperando interrupciones...")