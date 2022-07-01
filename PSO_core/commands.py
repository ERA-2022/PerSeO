# -*- coding: utf-8 -*-
from datetime import datetime
import os
from sys import platform
import time
import json
import uuid

def read_data():
    try:
        path = os.getcwd().replace('\\','/')+'/src'
        with open(path+'/data.json', 'r') as file:
            data = json.load(file)
            file.close()
        return data
    except:
        input("Error al tratar de leer el archivo de configuración\nPresione enter para continuar...")

def update_data(category = "", key = "",value =""):
    try:
        path = os.getcwd().replace('\\','/')+'/src'
        with open(path+"/data.json", "r") as file:
            data = json.load(file)
            file.close()

        with open(path+"/data.json", "w") as file:
            data[category][key] = value
            json.dump(data,file,indent=2)
            file.close()
        return data
    except:
        input("Error al tratar de leer o escribir en el archivo de configuración\nPresione enter para continuar...")

def create_data_file(ansys_exe, ansys_save_def, project_name, design_name, variable_name, units, max, min, nomilas, iterations, particles, description):
    data_structure = {
        "paths":
        {
            "main": os.getcwd().replace('\\','/')+'/',
            "results": os.getcwd().replace('\\','/')+'/'+"results/",
            "files": "",
            "figures": "",
            "models": os.getcwd().replace('\\','/')+'/'+"models/",
            "src": os.getcwd().replace('\\','/')+'/'+"src/",
            "ansys_exe": ansys_exe,
            "ansys_save_def": ansys_save_def
        },
        "values":
        {
            "project_name": project_name,
            "design_name": design_name,
            "variable_name": variable_name,
            "units": units,
            "max": max,
            "min": min,
            "def": nomilas,
            "n_var":len(nomilas),
            "iterations": iterations,
            "particles": particles,
            "description": description
        },
        "info":
        {
            "OS": platform,
            "ID": "",
            "start_time": 0,
            "elapsed_time": 0
        }
    }
    
    try:
        with open(data_structure['paths']['src']+"data.json", "w") as file:
            json.dump(data_structure,file,indent=2)
            file.close()
        print("Archivo de configuración creado ó actualizado con éxito!!")
    except:
        input("\nAlgo salió mal, por favor pongase en contacto con el desarrollador\nPresione enter para continuar")
    
def clear_screen():
    os.system("cls")

def wait_to_read(msj = "\nError!",clr=0):
    msj += "\nPresione enter para continuar..."
    input(msj)
    
    if clr == 0:
        clear_screen()    

def make_directory(name, path):
    try:
        if not os.path.isdir(name):
            os.mkdir(path+name)
            print("directorio "+name+" creado con éxito en la ruta "+path)
    except:
        print("Error al tratar de crear el directorio "+name)

def Y_N_question(msj):
    op = ""
    while op.upper() != "S" and op.upper() != "N":
        op = input(msj+" (s/n): ")
        if op.upper() != "S" and op.upper() != "N":
            wait_to_read("Error, digite una opción valida", 1)
    
    return op.upper()

def start_timing():
    return datetime.now()

def get_elapsed_time():
    diff=datetime.now()- read_data()['info']['start_time']
    return str(diff.total_seconds())

def setSimID():
    return str(uuid.uuid4())

def init_system(ansys_exe, ansys_save_def, project_name, design_name, variable_name, units, max, min, nomilas, iterations, particles, description):
    print("Iniciando sistema...")
    main_path = os.getcwd().replace('\\','/')+'/'
    
    make_directory('models',main_path)
    make_directory('results', main_path)
    make_directory('src', main_path)

    create_data_file(ansys_exe, ansys_save_def, project_name, design_name, variable_name, units, max, min, nomilas, iterations, particles, description)
        
    print("listo!")
    time.sleep(3)
    clear_screen()