import datetime
import json

def save(data_giro, data_lidar):
    try:
        timestamp = int(time.time())  # Obtenemos el timestamp actual en segundos
        medicion = {
            "timestamp": timestamp,  # Agregamos el timestamp a la medición
            "dataGiro": data_giro,
            "dataLidar": data_lidar
        }
        with open("datos_sensados.json", "a") as archivo:
            json.dump({"medicion": medicion}, archivo)
            archivo.write('\n')
    except Exception as e:
        print(f"Error al guardar en el archivo: {e}")

def erase():
    with open("datos_sensados.txt", 'w') as archivo:
        archivo.write('')
        archivo.close()



