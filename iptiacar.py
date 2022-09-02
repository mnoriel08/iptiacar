#!/usr/bin/env python3
# This Python file uses the following encoding: utf-8
#=======================================================================
# Programa: iptiacar.py - Programa p/auto-robot p/participar en WRO-2022
# Programadores: Noriel Alexis Madrid Navarro (estudiante)
#                Alexis Javier Acuna Manzane  (estudiante)
#                Jose Javier Rosario Ceitu    (tutor)
# Este programa se desarrollo de acuerdo con los algoritmos definidos
# en las reglas publicadas para la competencia en la Categoria Futuros
# Ingenieros de la WRO 2022
#=======================================================================

#=======================================================================
# seccion 1 - importacion de librerias y modulos de Python
#=======================================================================
from picarx    import Picarx # funcionalidad basica del iptiacar
import time            # modulo p/acceder a funciones de fechas y tiempo
from vilib     import Vilib  # reconocimiento de color y de objetos
from robot_hat import TTS    # sintetizar textos a voz
from grayscale_module import Grayscale_Module # sensor de escala grises
# 
#=======================================================================
# seccion 2 - variables globales
#=======================================================================

num   = 0
rojo  = None			# bandera booleana
verde = None			# bandera booleana
negro = None			# bandera booleana
direccionReloj			# bandera booleana
direccionContraReloj	# bandera booleana

# parametros del juego o carrera
juegoVueltas      = 0			# cantidad de vueltas realizadas
juegoMaxVueltas   = 3			# max de vueltas permitidas
juegoTiempoReal   = 0			# duracion en segundos (cronometro)
juegoTiempoMax    = 180			# limite maximo del juego en segundos
juegoTTS          = ""			# texto para convertirlo a voz

# parametros de la pista
pistaX            = 300         # dimension X en centimetros
pistaY            = 300         # dimension Y en centimetros
pistaColorObjeto  = ""          # color de objeto encontrado en la pista
pistaLineaNaranja = (0,60,100,0)
pistaLineaAzul    = (100,80,0,0)
pistaXYInfIzq     = (0,0)       # esquina inferior izquierda
pistaXYSupIzq     = (0,2.97)    # esquina superior izquierda
pistaXYSupDer     = (2.98,2.97) # esquina superior derecha
pistaXYInfDer     = (2.98,0)    # esquina inferior derecha

# parametros del auto-robot
global operador
operador          = ""			# operador de movimiento del auto-robot
autoVelocidad     = 30          # velocidad del auto-robot
autoX             = 0           # coordenada X del auto-robot
autoY             = 0           # coordenada Y del auto-robot
autoAngulo        = 0           # angulo de giro del auto-robot
autoDistancia     = 0           # distancia del auto-robot al obstaculo

#=======================================================================
# seccion 3 - funciones
#=======================================================================

# inicializar camara del auto-robot
def initCamera():
	Vilib.camera_start(vflip=False,hflip=False)
	Vilib.display(local=True,web=False)

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

def detectarColorVerde():
    Vilib.color_detect("green") # color a detectar - verde
    time.sleep(2)
    num = Vilib.detect_obj_parameter['color_n']
    print(num)
    if num == 0:
        print("no es verde")
        verde = False
    else:
        print("es verde")
        verde = True

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

def textAvoz(juegoTTS): # auto-robot envia mensaje de voz
	tts_robot = TTS()
	for i in juegoTTS:
		print(i)
		tts_robot.say(i)

def detectarEsquina(): # detectar proxima esquina en la pista
	try:
		while True:
			# leer valores de sensores A0, A1, A2 del modulo grayscale
			gm_val_list = ix.get_grayscale_data()
			print("gm_val_list:",gm_val_list)
			gm_status = ix.get_line_status(gm_val_list)
			print("gm_status:",gm_status)

			if gm_status == 'forward': # sensor A1
				print(1)
				ix.forward(autoVelocidad) 

			elif gm_status == 'left': # sensor A0
				ix.set_dir_servo_angle(12)
				ix.forward(autoVelocidad) 
			elif gm_status == 'right': # sensores A1 y A2
				ix.set_dir_servo_angle(-12)
				ix.forward(autoVelocidad) 
			else:
				ix.set_dir_servo_angle(0) # detenet el auto-robot
				ix.stop()
	finally:
		ix.stop() # detener el auto-robot

def main():  # bucle principal del programa
	time.sleep(2) # esperar a que arranque del programa
	print("iptiacar esta listo...")
	print("Detectar borde de pista frente al auto-robot...")

	# calcular a que distancia esta el borde negro de la pista
	num = 0
	detectarColorRojo()  # detectar objetos de color rojo
	detectarColorVerde() # detectar objetos de color verde

	# si no detecto objetos rojos o verdes, asume que vio color negro
	if not rojo and not verde:
		print("asume que vio borde negro de la pista")
		negro = True

		# mide distancia desde camara hasta borde negro de la pista
		autoDistancia = ix.ultrasonic.read()
		print("Distancia hasta el borde negro de la pista: " + str(autoDistancia))
	else:
		# si en salida vio objetos rojos/verdes mala posicion de salida
		print("Auto-robot mal ubicado en posicion de salida...")
		for i in range(0,2): # avisar mala posicion de salida y abortar
			juegoTTS = ["Auto","robot","mal","ubicado","en","posicion","de","salida"]
			ix.stop()
			exit()

	detectarEsquina() # avanzar hasta encontrar la 1ra esquina y girar
	detectarEsquina() # avanzar hasta encontrar la 2da esquina y girar
	detectarEsquina() # avanzar hasta encontrar la 3ra esquina y girar
	detectarEsquina() # avanzar hasta encontrar la 4ta esquina y girar

#=======================================================================
# seccion 4 - ventana principal del interfaz grafico de usuario (GUI)
#=======================================================================

#=======================================================================
# seccion 5 - ejecucion del bucle principal del programa iptiacar
#=======================================================================
if __name__ == "__main__":
	ix = Picarx()		# crea instancia del objeto auto-robot iptiacar
	main()					# iniciar ejecucion de programa
	Vilib.camera_close()	# cerrar la camara del auto-robot
