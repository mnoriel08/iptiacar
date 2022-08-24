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
from picarx import Picarx # funcionalidad basica del iptiacar
import time            # modulo p/acceder a funciones de fechas y tiempo
import cv2			   # cv2 = OpenCV - biblioteca p/ visión artificial
from robot_hat import TTS # biblioteca p/convertir texto a voz
from picamera import PiCamera # Interfaz Python p/cámara Raspberry Pi
from picamera.array import PiRGBArray
from vilib import Vilib # biblioteca p/procesamiento visual de imágenes
                        # con funciones como reconocimiento de color,
                        # reconocimiento facial, detección de manos,
                        # clasificación imágenes, detección de objetos,
                        # transmisión inalámbrica de video, etc.
#=======================================================================
# seccion 2 - variables globales
#=======================================================================

# parametros del juego o carrera
juegoSentido      = 0           # 0 sentido del reloj/1 contrareloj 
juegoMaxVueltas   = 3
juegoTiempo       = 0           # duracion en segundos (cronometro)
juegoTiempoMax    = 180         # limite maximo del juego en segundos
juegoVueltas      = 0           # cantidad de vueltas realizadas
juegoTTS          = ""          # texto para convertirlo a voz

# parametros de la pista
pistaX            = 2.98        # dimension X en metros
pistaY            = 2.98        # dimension Y en metros
#pistaColorBorde   = black
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
autoVelocidad     = 10          # velocidad del auto-robot
autoX             = 0           # coordenada X del auto-robot
autoY             = 0           # coordenada Y del auto-robot
autoAngulo        = 0           # angulo de giro del auto-robot
autoDistancia     = 0           # distancia del auto-robot al obstaculo

#=======================================================================
# seccion 3 - funciones
#=======================================================================

# mover auto en varias direcciones y detenerlo
def moverAuto(operador, autoVelocidad): 
	
	if operador == 'detener':
		ix.stop()
	else:
		if operador == 'avanzar':
			ix.set_dir_servo_angle(0)
			ix.forward(autoVelocidad)
		elif operador == 'retroceder':
				ix.set_dir_servo_angle(0)
				ix.backward(autoVelocidad)
		elif operador == 'girar_izquierda':
				ix.set_dir_servo_angle(-30)
				ix.forward(autoVelocidad)
		elif operador == 'girar derecha':
				ix.set_dir_servo_angle(30)
				ix.forward(autoVelocidad)

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

# emitir textos en sonidos
def texto_a_voz(juegoTTS):
	for i in juegoTTS:
		ttsRobot.say(i)

def detectarObstaculo():
	while True:
		autoDistancia = ix.ultrasonic.read()
		if autoDistancia > 0 and autoDistancia < 300:
			if autoDistancia < 30 and detectarColor() == "rojo":
				esquivarIzquierda()
			else:
				esquivarDerecha()

def main():  # bucle principal
	time.sleep(2) # esperar a que arranque
	print("iptiacar esta listo")
	detectarObstaculo()

#=======================================================================
# seccion 4 - ventana principal del interfaz grafico de usuario (GUI)
#=======================================================================

#=======================================================================
# seccion 5 - ejecucion del bucle principal del programa iptiacar
#=======================================================================

if __name__ == "__main__":
	try:
		ix = Picarx()             # instancia objeto auto-robot iptiacar
		ttsRobot = TTS()          # instancia objeto robot_hat
		main()
	except Exception as e:
			print("error:s"%e)
	finally:
		ix.stop()
