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
datos_mapa = rplidar.get_data_polar_interval(150,210)
time.sleep(1)

print(datos_mapa)
print(len(datos_mapa))

for i in datos_mapa:
    plt.plot(i[0], i[1],'ro')

plt.xlim([-2000,2000])
plt.ylim([-2000,2000])
plt.show()

rplidar.cleanup()




