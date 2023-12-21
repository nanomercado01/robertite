import sys
sys.path.append("../movement/")
sys.path.append("../data/")

import numpy as np
from scipy import signal
from scipy.fftpack import fft, fftshift
import matplotlib.pyplot as plt
from scipy.stats import norm
from motor import Motor
from Encoder import Encoder
from save_data import save

class FiltroBayesiano():
    
    def __init__(self,posinicio=0):

        """## 1. Modelo de Movimiendo

        ### 1.1 Distribución Uniforme Inicial

        Consideramos como suposición inicial que el robot está en la posicion 0
        """
        self.posinicio = posinicio
        
        self.N_SAMPLES = 200
        self.var_posinicio = 1
    
    def start(self, verbose = False):
        #belief = np.array([1/N_SAMPLES]*N_SAMPLES)
        belief = norm(self.posinicio,self.var_posinicio)
        x = np.linspace(0,self.N_SAMPLES,self.N_SAMPLES)
        belief = belief.pdf(x)
        belief = belief/sum(belief)
                
        if(verbose==True):
            print(belief) #Distribucion de la posicion inicial media posinicio y varianza 1
            
        return belief
    
    def movement(self,counter_encoder1, verbose = False):
        """### 1.2 Movimiento representado por Gaussiana"""

        movimiento = (counter_encoder1*2.512)/10 # mu de la gaussiana, las interrupciones del encoder 1 multiplicado por el avance en mm de pulso (2.512mm) multiplicado por 10 para pasar a cm
        varianza_mov = 2.5 # varianza del movimiento
        movement = norm(movimiento,varianza_mov)
        x = np.linspace(0,self.N_SAMPLES,self.N_SAMPLES)
        movement = movement.pdf(x)
        movement /= sum(movement)
        
        if(verbose == True):
            print(movement)
        
        return movement
    
    def convolucion(self, mat1, mat2,verbose = False, plot = False):
        """### 1.3 Convolución entre el estado inicial y el movimiento"""
        self.result = np.convolve(mat1,mat2)
        self.result = self.result/sum(self.result)
        
        if(verbose == True):
            print("El resultado entre la convolucion del estado inicial y el movimiento medido por el encoder es: ",np.argmax(self.result))

        if(plot == True):
            plt.stem(self.result)
            plt.title(r"Distribución Resultante")
            plt.ylabel("Amplitude")
            plt.xlabel("Posición")
            plt.xlim([np.argmax(self.result)-50,np.argmax(self.result)+50])
            plt.show()
        
        return self.result
    

    def lidar_measure(self, lidar_info, obstacles_pos, verbose = False, plot = False):
        """## 2. Modelo de observación

        Tomamos como referencia un obstáculo en la posición X. Usamos la distribución
        estimada del estado para determinar la distribución de la medición esperada.
        """
        x_sum = 0
        y_sum = 0
        for row in range(len(lidar_info)):
            x_sum += lidar_info[row][0]
            y_sum += lidar_info[row][1]

        coor_punto_prom = [x_sum/len(lidar_info),y_sum/len(lidar_info)]
        distancia_prom = (((coor_punto_prom[0]**2)+(coor_punto_prom[1]**2))**(1/2))/10 #la division por 10 es para pasar de mm a cm
        
         # Posicion del obstáculo (viene del mapa) (puse esta distancia para que la medicion del lidar me de parecida a los 30cm que nos movimos)

        """### 2.1 Medida del sensor con el modelado de la adquisición

        El modelo del sensor se representa con una Gaussiana.
        """
        # Gaussiana decribiendo el sensor
        varianza_sens = distancia_prom * 0.05 #Segun el datasheet del rplidar A1 que usamos, el error para distancia mayores a 1.5m es del 1%, para menores es del 0.5%. el rango max es de 12m.
        dato_sensado = distancia_prom #mu de la gaussiana
        media = obstacles_pos - dato_sensado # Uso el mapa para pasar del eje de mediciones al de posicion
        sensor_meas = norm(media,varianza_sens)
        x = np.linspace(0,len(self.result),len(self.result))
        sensor_meas = sensor_meas.pdf(x)
        self.result_act = sensor_meas
        
        if(verbose == True):
            print('La distancia al punto promedio captado por el lidar es: ',distancia_prom)
        
        if(plot == True):
            markerline, stemlines, baseline = plt.stem(sensor_meas,markerfmt='ro')
            plt.setp(stemlines, 'color', plt.getp(markerline,'color'))
            plt.xlim([np.argmax(sensor_meas)-50,np.argmax(sensor_meas)+50])
            plt.title("Modelo del sensor")
            plt.ylabel("Amplitud")
            plt.xlabel("Posición medida")
            plt.show()
        
        return sensor_meas

    def plot_mov_vs_sen(self):
        """### 2.2 Ploteo de enconder con posicion(result) y del lidar en simultaneo"""

        result_act = sensor_meas
        result_act /= sum(result_act)
       
        markerline, stemlines, baseline = plt.stem(self.result_act,markerfmt='ro') #Plotea la posicion sensado
        plt.setp(stemlines, 'color', plt.getp(markerline,'color'))
        plt.stem(result) #Plotea el resultado de movimiento
        plt.title(r"Modelo del sensor vs movimiento")
        plt.ylabel("Amplitude")
        plt.xlabel("Posición")
        plt.show()

    def multiply_mov_sens(self, verbose = False, plot = False):

        self.posteriori = np.multiply(self.result_act,self.result)
        # Normalizar la distribucion
        self.posteriori = self.posteriori/sum(self.posteriori)

        if(verbose==True):
            #print(self.posteriori)
            print("La posicion mas probable luego de la multiplicacion del sensado por el movimiento es: ",np.argmax(self.posteriori))
        
        pos_fin= np.argmax(self.posteriori)        

        if(plot == True):
            markerline, stemlines, baseline = plt.stem(self.posteriori,markerfmt='go')
            plt.setp(stemlines, 'color', plt.getp(markerline,'color'))
            markerline, stemlines, baseline = plt.stem(self.result_act,markerfmt='ro')
            plt.setp(stemlines, 'color', plt.getp(markerline,'color'))
            plt.stem(self.result)
            plt.xlim([pos_fin-50,pos_fin+50])
            plt.title(r"Posteriori")
            plt.ylabel("Amplitud")
            plt.xlabel("Posición")
            plt.show()
        
        return self.posteriori