import sys
from threading import Lock
import time
import matplotlib.pyplot as plt

sys.path.append('/home/pi/robertite/src/pruebas/rplidar')

from Rplidar import Rplidar

scan_data_lock = Lock()

rplidar = Rplidar('/dev/ttyUSB0', scan_data_lock, display = True)

time.sleep(1)
datos_mapa = rplidar.get_data_cartesian()
time.sleep(1)

print(datos_mapa)
print(len(datos_mapa))

for i in datos_mapa:
    plt.plot(i[0], i[1],'ro')

plt.show()

rplidar.cleanup()


