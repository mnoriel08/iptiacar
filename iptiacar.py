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
from picarx		import Picarx		# funcionalidad basica del iptiacar
import time			   # modulo p/acceder a funciones de fechas y tiempo
from vilib		import Vilib		# reconocimiento color y de objetos
from robot_hat	import TTS			# sintetizar textos a voz
# 
#=======================================================================
# seccion 2 - variables globales
#=======================================================================

num   = 0
rojo  = None					# bandera booleana
verde = None					# bandera booleana
negro = None					# bandera booleana
direccionReloj = False			# bandera booleana
direccionContraReloj = False	# bandera booleana

# parametros del juego o carrera
juegoVueltas      = 0			# cantidad de vueltas realizadas
juegoMaxVueltas   = 3			# max de vueltas permitidas
juegoTiempoReal   = 0			# duracion en segundos (cronometro)
juegoTiempoMax    = 180			# limite maximo del juego en segundos
juegoTTS          = ""			# texto para convertirlo a voz

# parametros de la pista
pistaX            = 300			# dimension X en centimetros
pistaY            = 300			# dimension Y en centimetros
pistaBordeMin     = 40			# ancho minimo borde de pista


pistaXYInfIzq     = (0,0)		# esquina inferior izquierda
pistaXYSupIzq     = (0,2.97)	# esquina superior izquierda
pistaXYSupDer     = (2.98,2.97)	# esquina superior derecha
pistaXYInfDer     = (2.98,0)	# esquina inferior derecha

# parametros del auto-robot
operador          = ""			# operador de movimiento del auto-robot
autoVelocidad     = 10			# velocidad del auto-robot
autoX             = 0			# coordenada X del auto-robot
autoY             = 0			# coordenada Y del auto-robot
autoAngulo        = 0			# angulo de giro del auto-robot (timon)
autoDistancia     = 0			# distancia del auto-robot al obstaculo
camaraAngulo      = 0			# angulo vertical de la camara
derDistancia      = 0			# distancia de auto a borde negro der
izqDistancia      = 0			# distancia de auto a borde negro izq

#=======================================================================
# seccion 3 - funciones
#=======================================================================

# inicializar camara del auto-robot
def initCamera():
	Vilib.camera_start(vflip=False,hflip=False)
	Vilib.display(local=True,web=False)

# mover auto en varias direcciones y detenerlo
def moverAuto():
	global operador
	global autoVelocidad
	global autoAngulo
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
		print("es verde")
		verde = True

# esquivar obstaculo por la izquierda
def esquivarIzquierda(autoAngulo):
	global autoDistancia
	if autodDistancia < 25:
		ix.set_dir_servo_angle(autoAngulo)
		ix.forward(autoVelocidad)
		ix.set_dir_servo_angle(0)
		ix.forward(autoVelocidad)

# esquivar obstaculo por la derecha
def esquivarDerecha(autoAngulo):
	global autoDistancia
	if autoDistancia < 25:
		ix.set_dir_servo_angle(autoAngulo)
		ix.forward(autoVelocidad)
		ix.set_dir_servo_angle(0)
		ix.forward(autoVelocidad)

def avanzarAProxEsquina():
	global autoVelocidad
	global autoDistancia
    
	# mide distancia desde camara hasta borde negro de la pista
	autoDistancia = ix.ultrasonic.read()
	autoDistancia = float(autoDistancia)
	print("Distancia hasta el borde negro de la pista: " + str(autoDistancia))

	# avanza en linea recta y mide distancia hasta el borde negro
	while autoDistancia > pistaBordeMin:
		ix.forward(autoVelocidad)
		time.sleep(0.5)
		autoDistancia = ix.ultrasonic.read()
		autoDistancia = float(autoDistancia)
		print("Distancia hasta el borde negro de la pista: " + str(autoDistancia))

	# si llego al limite, detener el auto-robot
	autoVelocidad = 0
	ix.forward(autoVelocidad)
	
	direccionDelAuto()
	
def direccionDelAuto():	# en que direccion se mueve el auto-robot?
	global camaraAngulo
	global direccionReloj
	global direccionContraReloj
	global operador
	global izqDistancia
	global derDistancia
	
	# mirar a izquierda, medir distancia al borde negro de la pista
	for camaraAngulo in range(0,-90,-1):
		ix.set_camera_servo1_angle(camaraAngulo)
		time.sleep(0.01)	# suspende (espera) ejecucion por 0.01 segs
		izqDistancia = ix.ultrasonic.read()
		izqDistancia = float(izqDistancia)
		print("Distancia hasta el borde negro izquierdo: " + str(izqDistancia))

	# mirar a derecha, medir distancia al borde negro de la pista
	for camaraAngulo in range(-90,90,1):
		ix.set_camera_servo1_angle(camaraAngulo)
		time.sleep(0.01)	# suspende (espera) ejecucion por 0.01 segs
		derDistancia = ix.ultrasonic.read()
		derDistancia = float(derDistancia)
		print("Distancia hasta el borde negro derecho: " + str(derDistancia))

	# si distancia izquierda < distancia derecha, el auto-robot se mueve
	if izqDistancia < derDistancia:
		direccionReloj = True	# segun las manecillas del reloj
		print("El auto-robot se mueve segun las manecillas de reloj...")
		operador = "detener"
		moverAuto()
		operador = "derecha"	# auto-robot gira a la derecha
		moverAuto()
	else:
		direccionContraReloj	# contra las manecillas del reloj
		print("El auto-robot se mueve contra las manecillas del reloj...")
		operador = "detener"
		moverAuto()
		operador = "izquierda"# auto-robot gira a la izquierda
		moverAuto()

def main():  # bucle principal del programa
	global num
	global rojo
	global verde
	global autoDistancia
	global autoVelocidad
	global camaraAngulo
	global pistaBorderMin

	time.sleep(2) # esperar a que arranque el programa
	print("iptiacar esta listo...")
	print("Detectar borde negro de pista frente al auto-robot...")

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
	# en total, en el menor tiempo posible
	
	avanzarAProxEsquina()	# primera esquina
	avanzarAProxEsquina()	# segunda esquina
	avanzarAProxEsquina()	# tercera esquina
	avanzarAProxEsquina()	# cuarta  esquina

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
