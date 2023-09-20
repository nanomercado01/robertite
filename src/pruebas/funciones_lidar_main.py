import sys
from threading import Lock
import time
import matplotlib.pyplot as plt

sys.path.append('/home/pi/robertite/src/pruebas/rplidar')

from Rplidar import Rplidar

scan_data_lock = Lock()

def datos_lidar():
    
    
    rplidar = Rplidar('/dev/ttyUSB0', scan_data_lock, display = True)
    
    time.sleep(1)
    datos_mapa = get_data_polar(rplidar)
    time.sleep(1)

    return(datos_mapa)
    #print(datos_mapa)
    #print(len(datos_mapa))

def grafico_lidar(datos_mapa):
    
    for i in datos_mapa:
        plt.plot(i[0], i[1],'ro')

    plt.show()

    rplidar.cleanup()
    
def get_data_polar(rplidar):
    
    scan_data_polar = []
    for angle in range(360):
        distance = rplidar.scan_data[angle]
        scan_data_polar.append(distance)
    return scan_data_polar
