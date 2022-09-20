#!/usr/bin/env python3
# This Python file uses the following encoding: utf-8

#=======================================================================
# Programa: iptiacar.py - Programa p/auto-robot p/participar en WRO-2022
# Programadores: Noriel Alexis Madrid Navarro (estudiante)
#                Alexis Javier Acuna Manzane  (estudiante)
#                Luis Sevillano               (tutor)
# Este programa se desarrollo de acuerdo con los algoritmos definidos
# en las reglas publicadas para la competencia en la Categoria Futuros
# Ingenieros de la WRO 2022
#=======================================================================

#=======================================================================
# seccion 1 - importacion de librerias y modulos de Python
#=======================================================================
import os
#import logging                  # funcionalidad de manejo de bitacora
from picarx     import Picarx   # funcionalidad basica del iptiacar
import time                     # modulo p/acceder a fechas y tiempo
from vilib      import Vilib    # reconocimiento color y de objetos
from robot_hat  import TTS      # sintetizar textos a voz
# 
#=======================================================================
# seccion 2 - variables globales
#=======================================================================

num   = 0
rojo  = None                    # bandera booleana
verde = None                    # bandera booleana
negro = None                    # bandera booleana
direccionReloj = False          # bandera booleana
direccionContraReloj = False    # bandera booleana
primeraEsquina = True

# parametros del juego o carrera
juegoVueltas      = 0           # cantidad de vueltas realizadas
juegoMaxVueltas   = 3           # max de vueltas permitidas
juegoEsquinas     = 0			# esquinas en una vuelta
juegoTiempoReal   = 0           # duracion en segundos (cronometro)
juegoTiempoMax    = 180         # limite maximo del juego en segundos
juegoTTS          = ""          # texto para convertirlo a voz

# parametros de la pista
pistaX            = 300         # dimension X en centimetros
pistaY            = 300         # dimension Y en centimetros
pistaBordeMin     = 75          # ancho minimo borde de pista


pistaXYInfIzq     = (0,0)       # esquina inferior izquierda
pistaXYSupIzq     = (0,2.97)    # esquina superior izquierda
pistaXYSupDer     = (2.98,2.97) # esquina superior derecha
pistaXYInfDer     = (2.98,0)    # esquina inferior derecha

# parametros del auto-robot
operador          = ""          # operador de movimiento del auto-robot
autoVelocidad     = 20          # velocidad del auto-robot
autoX             = 0           # coordenada X del auto-robot
autoY             = 0           # coordenada Y del auto-robot
autoAngulo        = 0           # angulo de giro del auto-robot (timon)
autoDistancia     = 0           # distancia del auto-robot al obstaculo
camaraAngulo      = 0           # angulo vertical de la camara
derDistancia      = 0           # distancia de auto a borde negro der
izqDistancia      = 0           # distancia de auto a borde negro izq

#=======================================================================
# seccion 3 - funciones
#=======================================================================

# inicializar camara del auto-robot
def initCamera():
    Vilib.camera_start(vflip=False,hflip=False)
    Vilib.display(local=True,web=False)

def detectarColorRojo():
    global num
    global rojo
    Vilib.color_detect("red")   # color a detectar - rojo
    time.sleep(2)
    num = Vilib.detect_obj_parameter['color_n']
    print(num)
    if num == 0:
        print("no es rojo")
        rojo = False
    else:
        print("es rojo")
        rojo = True
        
    return rojo

def detectarColorVerde():
    global num
    global verde
    Vilib.color_detect("green") # color a detectar - verde
    time.sleep(2)
    num = Vilib.detect_obj_parameter['color_n']
    print(num)
    if num == 0:
        print("no es verde")
        verde = False
    else:
        print("no es verde")
        verde = True
        
    return verde

# esquivar obstaculo por la izquierda
def esquivarIzquierda():
    global autoDistancia
    if autodDistancia < 25:
        ix.set_dir_servo_angle(-35)
        ix.forward(autoVelocidad)
        ix.set_dir_servo_angle(0)
        ix.forward(autoVelocidad)

# esquivar obstaculo por la derecha
def esquivarDerecha():
    global autoDistancia
    if autoDistancia < 25:
        ix.set_dir_servo_angle(35)
        ix.forward(autoVelocidad)
        ix.set_dir_servo_angle(0)
        ix.forward(autoVelocidad)

# recorrer el circuito de la pista tres veces, avanzado hasta llegar a
# la siguiente esquina cuatro veces, para completar un circuito y
# recorriendo tres circuitos, para competar el recorrido completo
# de la prueba. Dependiendo de la direccion en que viaja el
# auto-robot (sigiendo las manecillas del reloj o contra-reloj)
def ejecutarCircuito():
    global autoVelocidad    # lee distancia en formato alfanumerico 
    global autoDistancia    # convierte distancia a formato numerico
    global rojo
    global verde
    
    if juegoVueltas < juegoMaxVueltas: # realizar tres vueltas
		# mide distancia desde camara hasta borde negro de la pista
        autoDistancia = ix.ultrasonic.read()
        autoDistancia = float(autoDistancia)
        print("Distancia hasta el borde negro de la pista: " + str(autoDistancia))
        
        # avanza en linea recta y mide distancia hasta el borde negro
        while autoDistancia > pistaBordeMin:
            ix.forward(autoVelocidad)   # avanzar
            time.sleep(0.5)
            autoDistancia = ix.ultrasonic.read()    # leer distancia
            autoDistancia = float(autoDistancia)
            print("Distancia hasta el borde negro de la pista: " + str(autoDistancia))
            
            detectarColorRojo()		# objeto rojo ?
            if rojo:
				esquivarDerecha()

            detectarColorVerde()	# objeto verde ?
            if verde:
				esquivarIzquierda()

            
        # si llego al limite pistaBordeMin ?, detener el auto-robot
        #ix.forward(0)		# detener el auto-robot
        if primeraEsquina == True:
            direccionDelAuto()  # averiguar en que direccion se mueve el auto
            
        ix.set_dir_servo_angle(0)
        if direccionReloj == True:  # girar 90 grados a la derecha
            for angle in range(0,90):
                ix.set_dir_servo_angle(angle)
                ix.forward(1)
                juegoEsquinas = juegoEsquinas + 1
        else:
            # girar 90 grados a la izquierda
            for angle in range(0,-90):
                ix.set_dir_servo_angle(angle)
                ix.forward(1)
                juegoEsquinas = juegoEsquinas + 1 
    else:
		ix.forward(0)
		ix.stop()
		print("Fin del recorrido")

# determinar en que direccion se esta moviendo el auto-robot
def direccionDelAuto(): # en que direccion se mueve el auto-robot?
    global camaraAngulo
    global direccionReloj
    global direccionContraReloj
    global operador
    global izqDistancia
    global derDistancia
    global primeraEsquina
    
    primeraEsquina = False
    
    # mirar a derecha, medir distancia al borde negro de la pista
    for camaraAngulo in range(0,90,1):
        ix.set_camera_servo1_angle(camaraAngulo)
        time.sleep(0.01)    # suspende (espera) ejecucion por 0.01 segs
    derDistancia = ix.ultrasonic.read() # distancia al borde derecho
    derDistancia = float(derDistancia)
    print("Distancia hasta el borde negro derecho: " + str(derDistancia))
    
    camaraAngulo = 0
    ix.set_camera_servo1_angle(camaraAngulo)

    # mirar a izquierda, medir distancia al borde negro de la pista
    for camaraAngulo in range(0,-90,-1):
        ix.set_camera_servo1_angle(camaraAngulo)
        time.sleep(0.01)    # suspende (espera) ejecucion por 0.01 segs
    izqDistancia = ix.ultrasonic.read() # distancia al borde izquierdo
    izqDistancia = float(izqDistancia)
    print("Distancia hasta el borde negro izquierdo: " + str(izqDistancia))
    
    camaraAngulo = 0
    ix.set_camera_servo1_angle(camaraAngulo)

    # si distancia izquierda < distancia derecha, el auto-robot se esta
    # moviendo en el sentido de las manecillas del reloj
    if izqDistancia < derDistancia:
        direccionReloj = True   # segun las manecillas del reloj
        print("El auto-robot se mueve segun las manecillas de reloj...")
    else:   # el auto se esta moviendo en sentido contrario a las
            # menecillas del reloj
        direccionContraReloj = True # contra las manecillas del reloj
        print("El auto-robot se mueve contra las manecillas del reloj...")

def main():  # bucle principal del programa=============================
    global num
    global rojo
    global verde
    global autoDistancia
    global autoVelocidad
    global camaraAngulo
    global pistaBorderMin

    time.sleep(2) # esperar a que arranque el programa
    print("Bitacora de la prueba...")
    
    print("iptiacar esta listo...")
    
    print("Detectar borde de pista frente al auto-robot...")

    # ajustar angulo horizontal de la camara a cero para mirar al frente
    camaraAngulo = 0
    ix.set_camera_servo1_angle(camaraAngulo)

    # ajustar angulo vertical de la camara a cero para mirar horizonte
    camaraAngulo = 0
    ix.set_camera_servo2_angle(camaraAngulo)

    print("Angulos de la camara ajustados...")

    # detectar objetos en la pista frente al auto robot
    num = 0
    detectarColorRojo()  # detectar objetos de color rojo
    detectarColorVerde() # detectar objetos de color verde

    # si no detecto objetos rojos o verdes, asume que vio color negro
    if not rojo and not verde:
        print("asume que vio borde negro de la pista")
        negro = True
    else:
        # si en salida vio objetos rojos/verdes mala posicion de salida
        print("Auto-robot mal ubicado en posicion de salida...")
        for i in range(0,2): # avisar mala posicion de salida y abortar
            juegoTTS = ["Auto","robot","mal","ubicado","en","posicion","de","salida"]
            ix.stop()
            exit()

    # la pista tiene cuatro esquinas las cuales debe recorrer el
    # auto-robot en cada vuelta, y el auto-robot debe hacer tres vueltas
    # en total recorrera 12 esquinas, en el menor tiempo posible
    
    ejecutarCircuito()  # recorrer tres vueltas del recorrido

#=======================================================================
# seccion 4 - ventana principal del interfaz grafico de usuario (GUI)
#=======================================================================

#=======================================================================
# seccion 5 - ejecucion del bucle principal del programa iptiacar
#=======================================================================
if __name__ == "__main__":
    #if os.path.exists("/home/pi/picar-x/iptiacar-main/iptiacar.log"):
        #os.remove("/home/pi/picar-x/iptiacar-main/iptiacar.log")
        #print("Borrando archivo de bitacora...")
    #logging.basicConfig(level=logging.INFO, filename="/home/pi/picar-x/iptiacar-main/iptiacar.log", filemode='w', format='%(name)s - %(levelname)s  %(message)s')
    ix = Picarx()       # crea instancia del objeto auto-robot iptiacar
    main()                  # iniciar ejecucion de programa
    ix.forward(0)
    ix.stop()
    Vilib.camera_close()    # cerrar la camara del auto-robot
