# -*- coding: utf-8 -*-
"""
	Authors: German Chaparro, Jorge Cardenas,Oscar Restrepo, Sergio Mora, Jhon Vera, and Jaime Angel
	Year: 2022
"""
# MENU DE PRUEBAS
# 1. EJECUCIÓN DE UN SCRIPT DE DISEÑO
# 2. EXCEPCIÓN FORZADA (DIVISIÓN EN 0)
# 3. LECTURA DEL ARCHIVO DE CONFIGURACIÓN DESDE EL ARCHIVO PARAMETROS
# 4. USO DE LA FUNCIÓN LEER DATOS DEL ARCHIVO FITNESS CON INDICE 1000, 1000

import subprocess
from .commands import clear_screen, wait_to_read, Y_N_question,read_data

def launch_tester(fitness):
    while True:
        clear_screen()
        print("\n-----\TEST MODE\n")
        print("1> Ejecutar un script de diseño")
        print("2> Interrupción forzada")
        print("3> Lectura del archivo de configuración")
        print("4> Prueba fitness")
        print("5> volver")
        test = input("Digite una opción: ")

        if test == '1':
            modelName = input("Digite el nombre del archivo: ")
            if len(modelName) == 0:
                modelName = "dibuja.py"
            elif '.py' not in modelName:
                modelName += ".py"
            print("Archivo -> "+modelName)

            if Y_N_question("¿El script digitado se encuentra en la carpeta por defecto (models)?") == "S":
                modelName = "models/"+modelName
                subprocess.run([read_data()['setup']['ansys_exe'],"-RunScript", modelName])
            else:
                path_file = input("Digite la ruta completa donde se encuentra el archivo: ")+"/"+modelName
                subprocess.run([read_data()['setup']['ansys_exe'],"-RunScript", path_file])

        elif test == '2':    
            print(1/0)   

        elif test == '3':
            clear_screen()
            print("valor de propiedades abierto desde parametros: ")
            for key, value in read_data().items():
                print(key+":")
                for key2, value2 in value.items():
                    print("\t"+key2+" --> "+value2)
            wait_to_read("")
        elif test == '4':
            clear_screen()
            val = int(input("Digite el valor del primer párametro: "))
            fitness(val)
            wait_to_read("")

        elif test == '5':
            break

        else:
            wait_to_read("\nError, digite una opción valida\n")