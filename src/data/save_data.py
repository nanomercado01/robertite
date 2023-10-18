import datetime

def guardar_en_archivo(dato_giro, dato_lidar):
    try:
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("datos_sensados.txt", "a") as archivo:
            archivo.write(f"{fecha_actual},giroscopio: {dato_giro}, \n lidar: {dato_lidar} \n")
            archivo.close()
    except Exception as e:
        print(f"Error al guardar en el archivo: {e}")
        

def borrar_contenido():
    with open("datos_sensados.txt", 'w') as archivo:
        archivo.write('')
        archivo.close()



