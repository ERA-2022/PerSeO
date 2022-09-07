# -*- coding: utf-8 -*-
import PSO_core.Tester as Tester
from PSO_core.commands import *
from PSO_functions.optimizate import main, only_fit
from PSO_functions.simulate import init_model

def ops_main_menu():
    op = ""
    clear_screen()
    while(op != '1' and op != '2' and op != '3' and op != '4' and op != '5' and op != '6'):
        print("\n-------->PSO APP<---------")
        print("-----\Menú")
        print("1> Optimizate")
        print("2> Fitness function test")
        print("3> Graphics tools")
        print("4> Run script")
        print("5> Set up")
        print("6> Salir ")
        op = input("Digite una opción del menú: ")

        if op != '1' and op != '2' and op != '3' and op != '4' and op != '5' and op != '6':
            wait_to_read("Error, digite una opción valida!")
    return int(op)

def ops_set_up_menu():
    op = ""
    clear_screen()
    while(op != '1' and op != '2' and op != '3'):
        print("\n-----\Configuración")
        print("1> Modificar valores")
        print("2> visualizar valores")
        print("3> Volver ")
        op = input("Digite una opción del menú: ")

        if op != '1' and op != '2' and op != '3':
            wait_to_read("Error, digite una opción valida!")
    return int(op)

def set_up_menu():
    volver = False
    while not volver:
        op = ops_set_up_menu()

        if op == 1:
            info = read_data()
            print("\nValores actuales:")
            for key,value in info['paths'].items():
                print(key+" -> "+value)
            print()
            for key,value in info['paths'].items():
                if Y_N_question("¿Desea cambiar el valor de "+key+"?") == "S":
                    new_val = str(input("Digite el nuevo valor de "+key+": "))
                    update_data("paths",key,new_val)

                    if read_data()['paths'][key] == new_val:
                        wait_to_read("Cambio Realizado con exito!")
                    else:
                        wait_to_read("Algo salió mal, trate nuevamente")
        elif op == 2:
            clear_screen()
            print("\nValores actuales:")
            for key,value in read_data()['paths'].items():
                print(key+" -> "+value)
            wait_to_read("")
        elif op == 3:
            volver = True
            clear_screen()
        else:
            wait_to_read("Algo salió mal")

def main_menu(fitness):
    salir = False
    while not salir:
        op = ops_main_menu()
        if op == 1:
            ready = not init_model()
            if ready:
                main(fitness)
                wait_to_read("Fin de la ejecución")
            else:
                wait_to_read("El archivo del modelo no existe, verifique que su archivo .py este en la carpeta models o que el archivo .aedt exista en la carpeta .../Documents/Ansoft e intente ejecutar el código nuevamente")
        elif op == 2:
            only_fit(fitness)
            wait_to_read("Fin de la ejecución")
        elif op == 3:
            wait_to_read("Pendiente por desarrollar")
        elif op == 4:
            Tester.launch_tester(fitness)
        elif op == 5:
            set_up_menu()
        elif op == 6:
            print("\nGracias por usar nuestro software!")
            salir = True
        else:
            wait_to_read("Algo salió mal")
        