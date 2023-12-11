import sys
sys.path.append('../utils')

from threading import Lock
import time
import matplotlib.pyplot as plt
import numpy as np
from Rplidar import Rplidar

scan_data_lock = Lock()

rplidar = Rplidar(scan_data_lock,'/dev/ttyUSB0', display = True)

time.sleep(1)
datos_mapa = rplidar.get_data_polar_interval(165,195)
time.sleep(1)

x_sum = 0
y_sum = 0
for row in range(len(datos_mapa)):
    x_sum += datos_mapa[row][0]
    y_sum += datos_mapa[row][1]

coor_punto_prom = [x_sum/len(datos_mapa),y_sum/len(datos_mapa)]
distancia_prom = (((coor_punto_prom[0]**2)+(coor_punto_prom[1]**2))**(1/2))/10

print(distancia_prom)
print(len(datos_mapa))

for i in datos_mapa:
    plt.plot(i[0], i[1],'ro')

plt.xlim([-500,500])
plt.ylim([-500,500])
plt.show()

rplidar.cleanup()




