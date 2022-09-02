#!/usr/bin/env python3
# This Python file uses the following encoding: utf-8
#=======================================================================

#=======================================================================
# seccion 1 - importacion de librerias y modulos de Python
#=======================================================================
from picarx    import Picarx # funcionalidad basica del iptiacar
from grayscale_module import Grayscale_Module # sensor de escala grises
# 
#=======================================================================
# seccion 2 - variables globales
#=======================================================================

#=======================================================================
# seccion 3 - funciones
#=======================================================================

def detectarLinea(): # detectar linea de esquina en la pista
	for i in range(0,10):
		# leer valores de sensores A0, A1, A2 del modulo grayscale
		gm_val_list = ix.get_grayscale_data()
		print("gm_val_list:",gm_val_list)
		gm_val_list_avg = sum(gm_val_list)/len(gm_val_list)
		print(gm_val_list)
		gm_status = ix.get_line_status(gm_val_list)
		print("gm_status:",gm_status)
		exit()

def main():  # bucle principal del programa
	time.sleep(2) # esperar a que arranque del programa
	print("iptiacar esta listo...")
	print("probar el sensor grayscale...")

	detectarLinea() # detectar parametros de la linea en la pista

#=======================================================================
# seccion 4 - ventana principal del interfaz grafico de usuario (GUI)
#=======================================================================

#=======================================================================
# seccion 5 - ejecucion del bucle principal del programa iptiacar
#=======================================================================
if __name__ == "__main__":
	ix = Picarx()
	main()					# iniciar ejecucion de programa
