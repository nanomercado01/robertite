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


def filtro_bayesiano(counter_encoder1,lidar_info, OBSTACLES_POS):    

    """## 1. Modelo de Movimiendo

    ### 1.1 Distribución Uniforme Inicial

    Consideramos como suposición inicial que el robot está en la posicion 0
    """

    N_SAMPLES = 200
    posinicio = 0
    var_posinicio = 1
    #belief = np.array([1/N_SAMPLES]*N_SAMPLES)
    belief = norm(posinicio,var_posinicio)
    x = np.linspace(0,N_SAMPLES,N_SAMPLES)
    belief = belief.pdf(x)
    belief = belief/sum(belief)
    #print(belief) #Distribucion de la posicion inicial media 0 y varianza 1


    """### 1.2 Movimiento representado por Gaussiana"""

    movimiento = (counter_encoder1*2.512)/10 # mu de la gaussiana, las interrupciones del encoder 1 multiplicado por el avance en mm de pulso (2.512mm) multiplicado por 10 para pasar a cm
    varianza_mov = 5 # varianza del movimiento
    movement = norm(movimiento,varianza_mov)
    x = np.linspace(0,N_SAMPLES,N_SAMPLES)
    movement = movement.pdf(x)
    movement /= sum(movement)

    #print(movement)

    """### 1.3 Convolución entre el estado inicial y el movimiento"""

    result = np.convolve(belief,movement)
    result = result/sum(result)
    print("El resultado entre la convolucion del estado inicial y el movimiento medido por el encoder es: ",np.argmax(result))

    plt.stem(result)
    plt.title(r"Distribución Resultante")
    plt.ylabel("Amplitude")
    plt.xlabel("Posición")
    #plt.show()

    """## 2. Modelo de observación

    Tomamos como referencia un obstáculo en la posición 150. Usamos la distribución
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
    media = OBSTACLES_POS - dato_sensado # Uso el mapa para pasar del eje de mediciones al de posicion
    sensor_meas = norm(media,varianza_sens)
    x = np.linspace(0,len(result),len(result))
    sensor_meas = sensor_meas.pdf(x)

    markerline, stemlines, baseline = plt.stem(sensor_meas,markerfmt='ro')
    plt.setp(stemlines, 'color', plt.getp(markerline,'color'))
    plt.xlim([0,OBSTACLES_POS])
    plt.title("Modelo del sensor")
    plt.ylabel("Amplitud")
    plt.xlabel("Posición medida")

    """### 2.2 Valor sensado"""

    result_act = sensor_meas
    result_act /= sum(result_act)

    markerline, stemlines, baseline = plt.stem(result_act,markerfmt='ro') #Plotea la posicion sensado
    plt.setp(stemlines, 'color', plt.getp(markerline,'color'))
    plt.stem(result) #Plotea el resultado de movimiento
    plt.title(r"Modelo del sensor vs movimiento")
    plt.ylabel("Amplitude")
    plt.xlabel("Posición")
    #plt.show()


    def pos_mas_prob(array):
      for i in range(len(array)): #Posicion mas probable redondeada al entero
       if array[i] == maximo:
        print("La posicion mas probable luego de la multiplicacion del sensado por el movimiento es: ",i)
    
    #print(result_act)
    posteriori = np.multiply(result_act,result)
    #print(posteriori)
    #print(sum(posteriori))
    #print(type(posteriori))
    # Normalizar la distribucion
    posteriori = posteriori/sum(posteriori)
    #print(sum(posteriori))
    maximo = max(posteriori)

    #pos_mas_prob(posteriori)
    print("La posicion mas probable luego de la multiplicacion del sensado por el movimiento es: ",np.argmax(posteriori))

    markerline, stemlines, baseline = plt.stem(posteriori,markerfmt='go')
    plt.setp(stemlines, 'color', plt.getp(markerline,'color'))
    markerline, stemlines, baseline = plt.stem(result_act,markerfmt='ro')
    plt.setp(stemlines, 'color', plt.getp(markerline,'color'))
    plt.stem(result)
    plt.xlim([0,15])
    plt.title(r"Posteriori")
    plt.ylabel("Amplitud")
    plt.xlabel("Posición")
    plt.show()

    """### 2.3 Lazo gral #HASTA ACA LLEGUE EL 23/11. LAS GAUSSIANA RESULTANTE DE LO MEDIDO DEL LIDAR Y EL ENCODER YA ESTA LISTA

    """
    
    result_now = np.array(result_act)
    print(result_act)
    #len(result_now)

    """Prestar atencion al result act, hay que actualizar la medicion del sensor, en realidad el obstaculo se esta acercando, porque el robot va avanzando 25 a 25 y el obs esta a 150"""

    repetition = 10 #Cantidad de lazos generales
    start = posteriori
    movementlazo = movement
    resultlazo2 = []

    for i in range(repetition):
      convolucion = np.convolve(start,movementlazo,mode='same')
      convolucion /= sum(convolucion)

      multiplicacion = np.multiply(convolucion, result_act)
      multiplicacion /= sum(multiplicacion)

      start = multiplicacion
      resultlazo2.append(multiplicacion)

      media = OBSTACLES_POS - (110-i*15)
      x = np.linspace(0,len(result),len(result))
      #belief = belief.pdf(x)
      result_act = norm(media,varianza_sens).pdf(x)

      plt.stem(resultlazo2[i])


    plt.xlim([0,200])
    plt.title(r"Distribución Resultante")
    plt.ylabel("Amplitude")
    plt.xlabel("Posición")

    arreglo = resultlazo2[len(resultlazo2)-1]
    maximo2 = max(arreglo)
    for i in range(len(arreglo)):
      if  arreglo[i] == maximo2:
        print(i)
