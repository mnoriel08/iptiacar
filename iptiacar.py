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
from grayscale_module import Grayscale_Module
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
# 
#=======================================================================
# seccion 2 - variables globales
#=======================================================================

# parametros del juego o carrera
juegoDireccion    = ""          # 0 sentido del reloj/1 contrareloj 
juegoMaxVueltas   = 3
juegoTiempo       = 0           # duracion en segundos (cronometro)
juegoTiempoMax    = 180         # limite maximo del juego en segundos
juegoVueltas      = 0           # cantidad de vueltas realizadas
juegoTTS          = ""          # texto para convertirlo a voz

# parametros de la pista
pistaX            = 2.98        # dimension X en metros
pistaY            = 2.98        # dimension Y en metros
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
autoVelocidad     = 10          # velocidad del auto-robot
autoX             = 0           # coordenada X del auto-robot
autoY             = 0           # coordenada Y del auto-robot
autoAngulo        = 0           # angulo de giro del auto-robot
autoDistancia     = 0           # distancia del auto-robot al obstaculo

#=======================================================================
# seccion 3 - funciones
#=======================================================================
ix = Picarx() # crea instancia del objeto auto-robot iptiacar
color_dict = {'red':[0,4],'orange':[5,18],'yellow':[22,37],'green':[42,85],'blue':[92,110],'purple':[115,165],'red_2':[165,180]}  #Here is the range of H in the HSV color space represented by the color

kernel_5 = np.ones((5,5),np.uint8) #Define a 5×5 convolution kernel with element values of all 1.

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

# detectar color que esta viendo el auto-robot al frente
def detectar_color(img,color_name):

    # The blue range will be different under different lighting conditions and can be adjusted flexibly.  H: chroma, S: saturation v: lightness
    resize_img = cv2.resize(img, (160,120), interpolation=cv2.INTER_LINEAR)  # In order to reduce the amount of calculation, the size of the picture is reduced to (160,120)
    hsv = cv2.cvtColor(resize_img, cv2.COLOR_BGR2HSV)              # Convert from BGR to HSV
    color_type = color_name
    
    mask = cv2.inRange(hsv,np.array([min(color_dict[color_type]), 60, 60]), np.array([max(color_dict[color_type]), 255, 255]) )           # inRange()：Make the ones between lower/upper white, and the rest black
    if color_type == 'red':
            mask_2 = cv2.inRange(hsv, (color_dict['red_2'][0],0,0), (color_dict['red_2'][1],255,255)) 
            mask = cv2.bitwise_or(mask, mask_2)

    morphologyEx_img = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_5,iterations=1)              # Perform an open operation on the image 

    # Find the contour in morphologyEx_img, and the contours are arranged according to the area from small to large.
    _tuple = cv2.findContours(morphologyEx_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)      
    # compatible with opencv3.x and openc4.x
    if len(_tuple) == 3:
        _, contours, hierarchy = _tuple
    else:
        contours, hierarchy = _tuple
    
    color_area_num = len(contours) # Count the number of contours

    if color_area_num > 0: 
        for i in contours:    # Traverse all contours
            x,y,w,h = cv2.boundingRect(i)      # Decompose the contour into the coordinates of the upper left corner and the width and height of the recognition object

            # Draw a rectangle on the image (picture, upper left corner coordinate, lower right corner coordinate, color, line width)
            if w >= 8 and h >= 8: # Because the picture is reduced to a quarter of the original size, if you want to draw a rectangle on the original picture to circle the target, you have to multiply x, y, w, h by 4.
                x = x * 4
                y = y * 4 
                w = w * 4
                h = h * 4
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)  # Draw a rectangular frame
                cv2.putText(img,color_type,(x,y), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2)# Add character description

    return img,mask,morphologyEx_img

with PiCamera() as camera:
    print("start color detect")
    camera.resolution = (640,480)
    camera.framerate = 24
    rawCapture = PiRGBArray(camera, size=camera.resolution)  
    time.sleep(2)

    for frame in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):# use_video_port=True
        img = frame.array
        img,img_2,img_3 =  color_detect(img,'red')  # Color detection function
        cv2.imshow("video", img)    # OpenCV image show
        cv2.imshow("mask", img_2)    # OpenCV image show
        cv2.imshow("morphologyEx_img", img_3)    # OpenCV image show
        rawCapture.truncate(0)   # Release cache
    
        k = cv2.waitKey(1) & 0xFF
        # 27 is the ESC key, which means that if you press the ESC key to exit
        if k == 27:
            break

    print('quit ...') 
    cv2.destroyAllWindows()
    camera.close()  

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

def detectar_esquina():
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
		px.stop()

def main():  # bucle principal del algoritmo
	time.sleep(2) # esperar a que arranque del programa
	print("iptiacar esta listo...")
	print("Detectar borde de pista frente al auto-robot...")

	# calcular a que distancia esta el borde negro de la pista
	#if detectarColor(img,"red"): # detectar color rojo ?
		# no detecto el color rojo
		#if detectarColor("green") == 0: # detectar color verde ?
			# no detecto el color verde, se asume color negro
			#autoDistancia = ix.ultrasonic.read() # mide distancia/borde
			#print("Distancia al borde de pista fue: " + autoDistancia)
		#else:
			#print("Auto-robot mal ubicado en posicion de salida...")
			#for i in range(0,2):
				#uegoTTS = ["Auto","robot","mal","ubicado","en","posicion","de","salida"]
			#ix.stop()
	for i in range(0,5):
		moverAuto('avanzar',autoVelocidad)
		moverAuto('detener',autoVelocidad)
		moverAuto('retroceder',autoVelocidad)
		moverAuto('detener',autoVelocidad)
		

#=======================================================================
# seccion 4 - ventana principal del interfaz grafico de usuario (GUI)
#=======================================================================

#=======================================================================
# seccion 5 - ejecucion del bucle principal del programa iptiacar
#=======================================================================

if __name__ == "__main__":
	try:
		main()
	except Exception as e:
			print("error:s"%e)
	finally:
		ix.stop()
