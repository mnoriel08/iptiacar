#!/usr/bin/env python3
# This Python file uses the following encoding: utf-8
#=======================================================================
# Programa: iptiacar.py - Programa p/auto-robot p/participar en WRO-2022
# Este programa se desarrollo de acuerdo con los algoritmos definidos
# en las reglas publicadas para la competencia en la Categoria Futuros
# Ingenieros de la WRO.
#=======================================================================

#=======================================================================
# seccion 1 - importacion de librerias y modulos de Python
#=======================================================================
from picarx    import Picarx # funcionalidad basica del iptiacar
import time            # modulo p/acceder a funciones de fechas y tiempo
from vilib     import Vilib  # reconocimiento de color y de objetos
from robot_hat import TTS    # sintetizar textos a voz
#  from grayscale_module import Grayscale_Module
# 
#=======================================================================
# seccion 2 - variables globales
#=======================================================================

num   = 0
rojo  = None
verde = None
negro = None

# parametros del juego o carrera
juegoDireccion    = ""          # 0 sentido del reloj/1 contrareloj 
juegoMaxVueltas   = 3
juegoTiempo       = 0           # duracion en segundos (cronometro)
juegoTiempoMax    = 180         # limite maximo del juego en segundos
juegoVueltas      = 0           # cantidad de vueltas realizadas
juegoTTS          = ""          # texto para convertirlo a voz

# parametros de la pista
pistaX            = 300         # dimension X en centimetros
pistaY            = 300         # dimension Y en centimetros
pistaColorObjeto  = ""          # color de objeto encontrado en la pista
#pistaColorPiso    = white
pistaLineaNaranja = (0,60,100,0)
pistaLineaAzul    = (100,80,0,0)
obstaculoRojo     = (238,39,55)
obstaculoVerde    = (68,214,44)
pistaXYInfIzq     = (0,0)       # esquina inferior izquierda
pistaXYSupIzq     = (0,2.97)    # esquina superior izquierda
pistaXYSupDer     = (2.98,2.97) # esquina superior derecha
pistaXYInfDer     = (2.98,0)    # esquina inferior derecha

# parametros del auto-robot
operador          = ""
autoVelocidad     = 30          # velocidad del auto-robot
autoX             = 0           # coordenada X del auto-robot
autoY             = 0           # coordenada Y del auto-robot
autoAngulo        = 0           # angulo de giro del auto-robot
autoDistancia     = 0           # distancia del auto-robot al obstaculo

#=======================================================================
# seccion 3 - funciones
#=======================================================================

# mover auto en varias direcciones y detenerlo
def moverAuto(): 
	if operador == 'detener':
		ix.stop()
	else:
		if operador == 'avanzar':
			ix.set_dir_servo_angle(0)
			while True:
				ix.forward(autoVelocidad)
				time.sleep(0.5)
		elif operador == 'retroceder':
				ix.set_dir_servo_angle(0)
				while True:
					ix.backward(autoVelocidad)
					time.sleep(0.5)
		elif operador == 'izquierda':
				for angle in range(0,-30,-1):
					ix.set_dir_servo_angle(-30)
					ix.forward(autoVelocidad)
					time.sleep(0.01)
		elif operador == 'derecha':
				for angle in range(0,30,1):
					ix.set_dir_servo_angle(30)
					ix.forward(autoVelocidad)
					time.sleep(0.01)

def detectarColorRojo():
    Vilib.camera_start(vflip=False,hflip=False)
    Vilib.display(local=True,web=False)
    Vilib.color_detect("red")   # Set the color to be detected
    time.sleep(2)
    num = Vilib.detect_obj_parameter['color_n']
    print(num)
    if num == 0:
        print("no es rojo")
        rojo = False
    else:
        print("es rojo")
        rojo = True
    Vilib.camera_close()

def detectarColorVerde():
    Vilib.camera_start(vflip=False,hflip=False)
    Vilib.display(local=True,web=False)
    Vilib.color_detect("green") # Set the color to be detected
    time.sleep(2)
    num = Vilib.detect_obj_parameter['color_n']
    print(num)
    if num == 0:
        print("no es verde")
        verde = False
    else:
        print("es verde")
        verde = True
    Vilib.camera_close()

def posicionX(): # leer coordenada X del auto
	autoX = ix.ultrasonic.read()

def posicionY(): # leer coordenada Y del auto
	autoY = ix.ultrasonic.read()

# esquivar obstaculo por la izquierda
def esquivarIzquierda(autoAngulo):
	if autodDistancia < 25:
		ix.set_dir_servo_angle(autoAngulo)
		ix.forward(autoVelocidad)
		ix.set_dir_servo_angle(0)
		ix.forward(autoVelocidad)

# esquivar obstaculo por la derecha
def esquivarDerecha(autoAngulo):
	if autoDistancia < 25:
		ix.set_dir_servo_angle(autoAngulo)
		ix.forward(autoVelocidad)
		ix.set_dir_servo_angle(0)
		ix.forward(autoVelocidad)

def detectarObstaculo():
	while True:
		autoDistancia = ix.ultrasonic.read()
		if autoDistancia > 0 and autoDistancia < 300:
			if autoDistancia < 30 and detectarColor("red") != 0:
				esquivarDerecha()   # obstaculo era rojo
			else:
				esquivarIzquierda() # obstaculo era verde

def textAvoz(juegoTTS):
	tts_robot = TTS()
	for i in juegoTTS:
		print(i)
		tts_robot.say(i)

def detectarEsquina():
	try:
		while True:
			gm_val_list = ix.get_grayscale_data()
			print("gm_val_list:",gm_val_list)
			gm_status = ix.get_line_status(gm_val_list)
			print("gm_status:",gm_status)

			if gm_status == 'forward':
				print(1)
				ix.forward(autoVelocidad) 

			elif gm_status == 'left':
				ix.set_dir_servo_angle(12)
				ix.forward(autoVelocidad) 
			elif gm_status == 'right':
				ix.set_dir_servo_angle(-12)
				ix.forward(autoVelocidad) 
			else:
				ix.set_dir_servo_angle(0)
				ix.stop()
	finally:
		ix.stop()

def main():  # bucle principal del algoritmo
	time.sleep(2) # esperar a que arranque del programa
	print("iptiacar esta listo...")
	print("Detectar borde de pista frente al auto-robot...")

	# calcular a que distancia esta el borde negro de la pista
	num = 0
	detectarColorRojo() # color rojo ?
	if rojo:  # detecto el color rojo
		pass
	else:
		detectarColorVerde() # color verde ?
		if verde:  # detecto el color verde
			pass
		else: # no detecto el color verde, se asume color negro
			print("se asume color negro")
			negro = True
			autoDistancia = ix.ultrasonic.read() # mide distancia/borde
			print("Distancia al borde de pista fue: " + str(autoDistancia))

	if not negro:
		print("Auto-robot mal ubicado en posicion de salida...")
		for i in range(0,2):
			juegoTTS = ["Auto","robot","mal","ubicado","en","posicion","de","salida"]

			ix.stop()
			exit()

	# mover el auto-robot hacia adelante
	operador = "avanzar"
	moverAuto()

#=======================================================================
# seccion 4 - ventana principal del interfaz grafico de usuario (GUI)
#=======================================================================

#=======================================================================
# seccion 5 - ejecucion del bucle principal del programa iptiacar
#=======================================================================
if __name__ == "__main__":
	ix = Picarx() # crea instancia del objeto auto-robot iptiacar
	main()
