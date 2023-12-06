import sys
sys.path.append('../utils')
from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import ThreadHandler
import time
from math import cos, sin, pi, floor
import matplotlib.animation as animation

### TODO: Display in Thread


class Rplidar:
    def __init__(self, scan_data_lock, PORT='/dev/ttyUSB0', display=False):

        self.display = display

        self.scan_data_lock = scan_data_lock
        self.lidar = RPLidar(PORT)

        self.scan_data = [0.]*360
        self.iterator = self.lidar.iter_scans(1000, 5)

        # Initial data
        info = self.lidar.get_info()
        print(info)
        health = self.lidar.get_health()
        print(health)

        # Start get data thread
        self.thread_data = ThreadHandler.ThreadHandler(
            self.get_periodic_data, "RPlidar data acquisition thread")
        self.thread_data.start()
        time.sleep(0.05)

    def stop_motor(self):
        self.lidar.stop_motor()

    def get_periodic_data(self):
        temp_iter = next(self.iterator)
        self.scan_data_lock.acquire()
        for i in temp_iter:
            self.scan_data[min([359, floor(i[1])])] = i[2]
        time.sleep(0.01)
        self.scan_data_lock.release()

    def get_data(self):
        return self.scan_data

    def get_data_polar(self):
        scan_data_cartesian = []
        max_distance = 0  # Escalado
        for angle in range(360):
            distance = self.scan_data[angle]
            if distance > 0:                  # ignore initially ungathered data points
                max_distance = max([min([5000, distance]), max_distance])
                radians = angle * pi / 180.0
                #print("Grados: %f, Radianes: %f, Distancia: %f"%(angle,radians,distance))
                scan_data_cartesian.append(
                    [distance * cos(radians), distance * sin(radians)])
                #print("Medicion %f %f"%(distance * cos(radians),distance * sin(radians)))
        return scan_data_cartesian
    
    ''' La siguiente funcion toma los datos de una apertura determinada entre 0-360. El grado cero corresponde al semieje que va desde
        el centro del lidar hacia el centro del motor del lidar. A partir de esa referencia podemos tomar los datos de la apertura que
        desee.'''
    def get_data_polar_interval(self,phi1,phi2):
        scan_data_cartesian = []
        max_distance = 0  # Escalado
        for angle in range(phi1,phi2):
            distance = self.scan_data[angle]
            if distance > 0:                  # ignore initially ungathered data points
                max_distance = max([min([1000, distance]), max_distance])
                radians = angle * pi / 180.0
                #print("Grados: %f, Radianes: %f, Distancia: %f"%(angle,radians,distance))
                scan_data_cartesian.append(
                    [distance * cos(radians), distance * sin(radians)])
                #print("Medicion %f %f"%(distance * cos(radians),distance * sin(radians)))
        return scan_data_cartesian
        
    
    def cleanup(self):
        self.thread_data.stop_thread()
        time.sleep(0.5)
        print("Cleanup RPlidar")
        self.lidar.stop()
        self.lidar.disconnect()

#    def grafico_lidar(self):

#        for i in self.scan_data:
#            plt.plot(i[0], i[1], 'ro')

#        plt.show()

#        rplidar.cleanup()


