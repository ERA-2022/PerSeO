# -*- coding: utf-8 -*-
"""
	Authors: German Chaparro, Jorge Cardenas,Oscar Restrepo, Sergio Mora, Jhon Vera, and Jaime Angel
	Year: 2022
"""
from datetime import datetime
import os
from sys import platform
import time
import json
import uuid
import PSO_core.messages as messages

def read_data():
    try:
        path = os.getcwd().replace('\\','/')+'/src'
        with open(path+'/data.json', 'r') as file:
            data = json.load(file)
            file.close()
        return data
    except:
        input(messages.READ_FILE_ERR)

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
        input(messages.R_W_FILE_ERR)

def create_data_file(ansys_exe, ansys_save_def, project_name, design_name, variable_name, units, max, min, nomilas, iterations, particles, branches,reports,category, sub_category,description):
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
            "branches": branches,
            "reports": reports,
        },
        "info":
        {
            "OS": platform,
            "ID": "",
            "category": category,
            "sub_category": sub_category,
            "description": description,
        }
    }
    
    try:
        with open(data_structure['paths']['src']+"data.json", "w") as file:
            json.dump(data_structure,file,indent=2)
            file.close()
        print(messages.C_U_SETUP_FILE)
    except:
        input(messages.CREATE_SETUP_FILE_ERR)
    
def clear_screen():
    os.system("cls")

def wait_to_read(msj = "\nError!",clr=0):
    msj += messages.INTRO_BTN_MSG
    input(msj)
    
    if clr == 0:
        clear_screen()    

def make_directory(name, path):
    try:
        if not os.path.isdir(name):
            os.mkdir(path+name)
            print(name + messages.CREATE_DIR + path)
    except:
        print(messages.CREATE_DIR_ERR+name)

def Y_N_question(msj):
    op = ""
    while op.upper() != messages.YES and op.upper() != messages.NO:
        op = input(msj+messages.Y_N)
        if op.upper() != messages.YES and op.upper() != messages.NO:
            wait_to_read(messages.INVALID_IN_ERR, 1)
    
    return op.upper()

def start_timing():
    return datetime.now()

def get_elapsed_time(start_time = ""):
    if start_time == "":
        start_time = read_data()['info']['start_time']
    diff= datetime.now()- start_time
    return str(diff.total_seconds())

def get_instructions_to_reports(tag, report, value):
    instructions = ""
    
    if report.upper() == "SMN":
        if len(value) > 0:
            for mn_val in value:
                instructions += "fn.creaSmn(oProject,'" + tag + "','"+ read_data()['info']['ID']+ "','"+ str(mn_val[0]) + "','"+ str(mn_val[1]) +"')\n"

    elif report.upper() == "ZMN":
        if len(value) > 0:
            for mn_val in value:
                instructions += "fn.creaZmn(oProject,'" + tag + "','"+ read_data()['info']['ID']+ "','"+ str(mn_val[0]) + "','"+ str(mn_val[1]) +"')\n"

    elif report.upper() == "GAIN":
        if len(value) > 0:
            for angle in value:
                instructions += "fn.creaGain(oProject,'" + tag + "','"+ read_data()['info']['ID']+ "','"+ str(angle)+"')\n"
    
    elif report.upper() == "AMPIMB":
        instructions = 'oModule.CreateOutputVariable("AmpImbalance", "'+str(value)+'", "Setup1 : Sweep", "Modal Solution Data", [])\n'
        instructions += "fn.creaAmpImb(oProject,'" + tag + "','"+ read_data()['info']['ID']+"')\n"

    elif report.upper() == "PHASEIMB":
        instructions = 'oModule.CreateOutputVariable("PhaseImb", "'+str(value)+'", "Setup1 : Sweep", "Modal Solution Data", [])\n'
        instructions += "fn.creaPhaseImb(oProject,'" + tag + "','"+ read_data()['info']['ID']+"')\n"
    
    elif report.upper() == "VSWR":
        if len(value) > 0:
            for port in value:
                instructions += "fn.creaVSWR(oProject,'" + tag + "','"+ read_data()['info']['ID']+"','"+str(port)+"')\n"

    elif report.upper() == "BW":
        instructions = "fn.creaBW(oProject,'" + tag + "','"+ read_data()['info']['ID']+"')\n"
    
    elif report.upper() == "DATATABLE":
        instructions = "fn.creaDataTable(oProject,'" + tag + "','"+ read_data()['info']['ID']+"')\n"

    return instructions

def get_graphic_name(report, value, i, j):
    graphic_name = ""

    if report.upper() == "SMN":
        graphic_name += "datosS"+str(value[0])+str(value[1])
    
    elif report.upper() == "ZMN":
        graphic_name += "datosZ"+str(value[0])+str(value[1])
    
    elif report.upper() == "GAIN":
        graphic_name +="datosGananciaPhi"+str(value)
    
    elif report.upper() == "AMPIMB":
        graphic_name += "amp_imb"

    elif report.upper() == "PHASEIMB":
        graphic_name += "pha_imb"
    
    elif report.upper() == "VSWR":
        graphic_name += "datosVSWR("+str(value)+")"

    elif report.upper() == "BW":
        graphic_name += "datosBW"
    
    elif report.upper() == "DATATABLE":
        graphic_name += "datosTabla"
    
    graphic_name += "_" + str(i)+"_"+str(j)
    
    return graphic_name

def setSimID():
    return str(uuid.uuid4())

def init_system(ansys_exe, ansys_save_def, project_name, design_name, variable_name, units, max, min, nomilas, iterations, particles, branches, reports, category, sub_category,description):
    print(messages.START_SYS)
    main_path = os.getcwd().replace('\\','/')+'/'
    
    make_directory('models',main_path)
    make_directory('results', main_path)
    make_directory(main_path+'results/comparison graphics/','')
    make_directory('src', main_path)

    create_data_file(ansys_exe, ansys_save_def, project_name, design_name, variable_name, units, max, min, nomilas, iterations, particles, branches, reports, category, sub_category,description)

    if ansys_exe != "":    
        print(messages.READY)
        time.sleep(3)
    clear_screen()