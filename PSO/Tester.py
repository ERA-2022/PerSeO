import subprocess
import time
from PSO.commands import clear_screen, wait_to_read, read_data
# MENU DE PRUEBAS
# 1. EJECUCIÓN DE UN SCRIPT DE DISEÑO
# 2. EXCEPCIÓN FORZADA (DIVISIÓN EN 0)
# 3. LECTURA DEL ARCHIVO DE CONFIGURACIÓN DESDE EL ARCHIVO PARAMETROS
# 4. USO DE LA FUNCIÓN LEER DATOS DEL ARCHIVO FITNESS CON INDICE 1000, 1000
def launch_tester():
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
            print(f"Archivo -> {modelName}")
            #subprocess.run([data['setup']['ansys_exe'],"-RunScript", modelName])
            time.sleep(5)

        elif test == '2':    
            print(f"{1/0}")   

        elif test == '3':
            clear_screen()
            print("valor de propiedades abierto desde parametros: ")
            for key, value in read_data().items():
                print(f"{key}:")
                for key2, value2 in value.items():
                    print(f"    {key2} --> {value2}")
            wait_to_read("")
        elif test == '4':
            print("Fintess")

        elif test == '5':
            break

        else:
            wait_to_read("\nError, digite una opción valida\n")