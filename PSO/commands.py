import os
import time
import json

def read_data():
    try:
        with open(f"{os.getcwd().replace('\\','/')}/data.json", "r") as file:
            data = json.load(file)
            file.close()

        return data
    except:
        input("Error al tratar de leer el archivo de configuración\nPresione enter para continuar...")

def update_data(category = "", key = "",value =""):
    try:
        with open(f"{os.getcwd().replace('\\','/')}/data.json", "r") as file:
            data = json.load(file)
            file.close()

        with open(f"{os.getcwd().replace('\\','/')}/data.json", "w") as file:
            data[category][key] = value
            json.dump(data,file,indent=2)
            file.close()
        return data
    except:
        input("Error al tratar de leer o escribir en el archivo de configuración\nPresione enter para continuar...")

def back_up_data():
    data_structure = {
        "paths":
        {
            "main": os.getcwd().replace('\\','/')+'/',
            "results": "results/",
            "ansys_exe": "C:/Program Files/AnsysEM/Ansys Student/v212/Win64/ansysedtsv.exe",
            "ansys_save_def": "C:/Users/ESTACION/Documents/Ansoft/"
        },
        "values":
        {
            "project_name": "backup",
            "design_name": "backup",
            "variable_name": "variables",
            "units": "mm",
            "max": [0],
            "min": [0],
            "def": [0],
            "iterations": 0,
            "particles": 0,
            "merit_fun_info": "backup data"
        }
    }
    try:
        with open(f"{os.getcwd().replace('\\','/')}/data.json", "w") as file:
            json.dump(data_structure,file,indent=2)
            file.close()
        print("Archivo de configuración precargado!!, por favor verifique las rutas y valores en el menú->configuración->configuración de rutas ó valores")
    except:
        input("\nAlgo salió mal, por favor pongase en contacto con el desarrollador\nPresione enter para continuar")

def clear_screen():
    os.system("cls")

def wait_to_read(msj = "\nError!",clr=0):
    msj += "\nPresione enter para continuar..."
    input(msj)
    
    if clr == 0:
        clear_screen()    

def make_directory(name:str, path:str):
    try:
        if not os.path.isdir(name):
            os.mkdir(name)
            print(f"directorio '{name}' creado con éxito en la ruta '{path}'")
    except:
        print(f"Error al tratar de crear el directorio '{name}'")

def Y_N_question(msj:str):
    op = ""
    while op.upper() != "S" and op.upper() != "N":
        op = input(f"{msj} (s/n): ")
        if op.upper() != "S" and op.upper() != "N":
            wait_to_read("Error, digite una opción valida", 1)
    
    return op.upper()

def init_system():
    print("Iniciando sistema...")

    path = os.getcwd().replace('\\','/')+'/'
    if path != read_data()["paths"]['main']:
        update_data("paths","main",path)
        print("Path actualizado!")
    
    make_directory('models',path)
    make_directory('results', path)
    make_directory('src', path)
    
    print("listo!")
    time.sleep(3)
    clear_screen()
