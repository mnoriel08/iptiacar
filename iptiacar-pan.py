 #!/usr/bin/env python3
# This Python file uses the following encoding: utf-8

#=======================================================================
# Programa: iptiacar-pan.py - Programa IPTIACAR p/participar en WRO-2022
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
import os			            # funciones del sistema operativo
from picarx     import Picarx   # funcionalidad basica del iptiacar
import time                     # modulo p/acceder a fechas y tiempo
from vilib      import Vilib    # reconocimiento color y de objetos
# 
#=======================================================================
# seccion 2 - variables globales
#=======================================================================

direccionReloj = False          # bandera booleana
direccionContraReloj = False    # bandera booleana
rojo  = None                    # bandera booleana
verde = None                    # bandera booleana
negro = None                    # bandera booleana

# parametros del juego o carrera
esquinas          = 0           # cantidad de esquinas
vueltas           = 0           # cantidad de vueltas realizadas
MaxVueltas        = 3           # max de vueltas permitidas
tiempoReal        = 0           # duracion en segundos (cronometro)
tiempoMax         = 180         # limite maximo del juego en segundos

# parametros de la pista
ladoPista         = 300         # lados X/Y en centimetros de la pista
bordeMin          = 50          # ancho minimo en cms al borde de pista

# parametros del auto-robot
velocidad         = 10          # velocidad del auto-robot
autoAngulo        = 0           # angulo de giro del auto-robot (timon)
distancia         = 0           # distancia del auto-robot al obstaculo
camaraAngulo      = 0           # angulo vertical de la camara
derDistancia      = 0           # distancia de auto a borde negro der
izqDistancia      = 0           # distancia de auto a borde negro izq

#=======================================================================
# seccion 3 - funciones
#=======================================================================

# inicializar video-camara del IPTIACAR
def initCamera():
    print("initCamera()")
    Vilib.camera_start(vflip=False,hflip=False)
    Vilib.display(local=True,web=False)
    return

# detectar objetos de color rojo
def detectarColorRojo():
    print("detectarColorRojo()")
    num = 0
    rojo = None
    Vilib.color_detect("red")   # color a detectar - rojo
    time.sleep(2)
    num = Vilib.detect_obj_parameter['color_n']
    print("objetos rojos = " + str(num))
    if num == 0:
        rojo = False
    else:
        rojo = True
    return rojo

# detectar objetos de color verde
def detectarColorVerde():
    print("detectarColorVerde()")
    num = 0
    verde = None
    Vilib.color_detect("green") # color a detectar - verde
    time.sleep(2)
    num = Vilib.detect_obj_parameter['color_n']
    print("objetos verdes = " + str(num))
    if num == 0:
        verde = False
    else:
        verde = True
    return verde
    
def izquierda90(): # giro de 90 grados a la izquierda
    print("izquierda90()")
    for angle in range(0,-90):
        ix.set_dir_servo_angle(angle)
        time.sleep(0.01) # suspende ejecucion por 0.01 segs
        ix.forward(velocidad)
    return

def izquierda00(): # retornar a posicion 0
    print("izquierda00()")
    for angle in range(90,0,-1):
        ix.set_dir_servo_angle(angle)
        time.sleep(0.01)
        ix.forward(velocidad)
    return  

def derecha90():   # giro de 90 grados a la derecha
    print("derecha90()")
    for angle in range(0,90):
        ix.set_dir_servo_angle(angle)
        time.sleep(0.01) # suspende ejecucion por 0.01 segs
        ix.forward(velocidad)
    return

def derecha00(): # retornar a posicion 0
    print("derecha00()")
    for angle in range(-90,0,1):
        ix.set_dir_servo_angle(angle)
        time.sleep(0.01)
        ix.forward(velocidad)
    return

# esquivar obstaculo por la izquierda
def esquivarIzquierda(autoDistancia, autoVelocidad):
    print("esquivarIzquierda()")
    if autoDistancia < 25:
        ix.set_dir_servo_angle(-35)
        ix.forward(autoVelocidad)
        ix.set_dir_servo_angle(0)
        ix.forward(autoVelocidad)
    return

# esquivar obstaculo por la derecha
def esquivarDerecha(autoDistancia, autoVelocidad):
    print("esquivarDerecha()")
    if autoDistancia < 25:
        ix.set_dir_servo_angle(35)
        ix.forward(autoVelocidad)
        ix.set_dir_servo_angle(0)
        ix.forward(autoVelocidad)
    return
    
# ver horizontalmente adelante
def verAdelante():
    print("verAdelante()")
    global rojo
    global verde
    global negro
    
    ix.set_dir_servo_angle(0)
    print("Angulo del timon ajustado a cero...")
    ix.set_camera_servo1_angle(0) # ajustar camara para ver al frente
    ix.set_camera_servo2_angle(0) # ajustar camara para ver horizonte
    print("Angulos de la camara ajustados a cero...")
    detectarColorRojo()  # detectar objetos de color rojo
    detectarColorVerde() # detectar objetos de color verde
    if not rojo and not verde: # no vio objetos rojos o verdes
        print("Asume que solo vio el borde negro de la pista...")
        negro = True
    else:
        print("IPTIACAR esta mal ubicado en posicion de salida...")
        negro = False
        ix.forward(0)
        ix.stop()
        exit() # cancelar ejecucion del programa
    return negro

# recorrer las 4 esquinas del circuito de la pista
def circuito():
    print("circuito()")
    global velocidad
    global bordeMin
    global distancia
    global esquinas
    
    # en recorrido del circuito se hacen 4 giros (esquinas)
    esquinas = 0
    for esquinas in range(0,4): # realizar cuatro giros
        ix.set_dir_servo_angle(0) # timon hacia adelante
        ix.forward(velocidad)   # avanzar de frente
        time.sleep(0.5)
        distancia = ix.ultrasonic.read() # lee distancia
        distancia = float(distancia)     # alfanum-float
        print("Distancia al borde negro de la pista: "+str(distancia))
        while distancia > bordeMin: # avanzar hacia el borde
            distancia = ix.ultrasonic.read() # lee distancia
            distancia = float(distancia)     # alfanum-float
            print("Distancia al borde negro de la pista: "+str(distancia))
            #detectarColorRojo()	# detecto objeto rojo ?
            #if rojo:		# si ?
                #esquivarDerecha()   # esquiva x derecha
            #detectarColorVerde()	# detecto objetos verdes ?
            #if verde:		# si ?
                #esquivarIzquierda() # esquiva x izquierd
        # si llego al limite bordeMin ?, detener el IPTIACAR
        ix.forward(0)		# detener el auto-robot
        if esquinas == 0: # es la primera esquina ?
            direccionDelAuto()  # si, averiguar direccion del auto
        ix.set_dir_servo_angle(0)
        if direccionReloj == True:  # girar 90 grados a derecha
            derecha90()
            izquierda00()
            ix.forward(velocidad)
        else: # girar 90 grados a la izquierda
            izquierda90()
            derecha00()
            ix.forward(velocidad)
        print("Vuelta = " + str(vueltas) + " Esquina = " + str(esquinas+1) + " ...")    
    ix.forward(0)
    ix.stop()
    

# determinar en que direccion se esta moviendo el auto-robot
def direccionDelAuto(): # en que direccion se mueve el auto-robot?
    print("direccionDelAuto()")
    global camaraAngulo
    global direccionReloj
    global direccionContraReloj
    global izqDistancia
    global derDistancia
    
    # mirar a derecha, medir distancia al borde negro de la pista
    for camaraAngulo in range(0,90,1):
        ix.set_camera_servo1_angle(camaraAngulo)
        time.sleep(0.01)    # suspende (espera) ejecucion por 0.01 segs
    derDistancia = ix.ultrasonic.read() # distancia al borde derecho
    derDistancia = float(derDistancia)
    print("Distancia hasta el borde negro derecho: " + str(derDistancia))
    
    ix.set_camera_servo1_angle(0)

    # mirar a izquierda, medir distancia al borde negro de la pista
    for camaraAngulo in range(0,-90,-1):
        ix.set_camera_servo1_angle(camaraAngulo)
        time.sleep(0.01)    # suspende (espera) ejecucion por 0.01 segs
    izqDistancia = ix.ultrasonic.read() # distancia al borde izquierdo
    izqDistancia = float(izqDistancia)
    print("Distancia hasta el borde negro izquierdo: " + str(izqDistancia))
    
    ix.set_camera_servo1_angle(0)

    # si distancia izquierda < distancia derecha, el IPTIACAR se esta
    # moviendo en el sentido de las manecillas del reloj
    if izqDistancia < derDistancia:
        direccionReloj = True   # segun las manecillas del reloj
        print("El auto-robot se mueve segun las manecillas de reloj...")
    else:   # IPTIACAR se esta moviendo en sentido contrario a las
            # manecillas del reloj
        direccionContraReloj = True # contra las manecillas del reloj
        print("IPTIACAR se mueve contra las manecillas del reloj...")

def main():  # bucle principal del programa=============================t
    print("main()")
    global velocidad
    global bordeMin
    global vueltas
    global esquinas
    
    time.sleep(2) # esperar a que arranque el programa
    print("Bitacora del recorrido...")
    print("iptiacar esta listo...")
    print("Detectar borde de pista frente al IPTIACAR...")
    verAdelante()
    if negro == True: # si se detecto el borde negro de la pista
        vueltas = vueltas + 1
        circuito() # buscar esquina # 1

    # la pista tiene cuatro esquinas las cuales debe recorrer el
    # auto-robot en cada vuelta, y el auto-robot debe hacer tres vueltas
    # en total recorrera 12 esquinas, en el menor tiempo posible
    vueltas = vueltas + 1
    circuito()  # buscar esquina # 2
    vueltas = vueltas + 1
    circuito()  # buscar esquina # 3

#=======================================================================
# seccion 4 - ventana principal del interfaz grafico de usuario (GUI)
#=======================================================================

#=======================================================================
# seccion 5 - ejecucion del bucle principal del programa iptiacar
#=======================================================================
if __name__ == "__main__":
    ix = Picarx()         # crea instancia de objeto auto-robot iptiacar
    main()                  # iniciar ejecucion de programa
    ix.forward(0)
    ix.stop()
    Vilib.camera_close()    # cerrar la camara del auto-robot
