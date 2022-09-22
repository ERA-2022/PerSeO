# -*- coding: utf-8 -*-

from PSO_core.commands import get_graphic_name, read_data, get_instructions_to_reports, wait_to_read
from .graphicsManagement import draw_one_report
import logging
import subprocess
import os
import numpy as np
import matplotlib.pyplot as plt
import time
# modulo que contiene strings de mensajes
import PSO_core.messages as msg
import shutil
#=============================================================================
# THIS customized FUNCTION CALLS 'funciones.py' FILE AND GENERATES THE DATA
# TO BE USED BY THE OPTIMIZER.

def create_sim_file(particle, i, j):
    requiered_reports = read_data()['values']['reports']
    particle = particle.round(4)

    tag = "_"+str(i)+"_"+str(j)     #esta linea genera el string _i_j
    var = "[" + ", ".join([str(x) for x in particle]) + "]" #Generar string del array de datos de la particula
    
    f = open(read_data()['paths']['src']+"simulacion.py", "w")   #abre un archivo para escribir
    direccion_dibujo = '"'+read_data()["paths"]["ansys_save_def"]+read_data()["values"]["project_name"]+'.aedt"' 
    
    f.write("import PSO_core.ansys_functions as fn\n")

    f.write("\n")
    f.write("import ScriptEnv\n")
    f.write("oDesktop.RestoreWindow()\n")
    f.write("oDesktop.OpenProject("+direccion_dibujo+")\n")
    f.write("oProject = oDesktop.SetActiveProject(" + '"'+read_data()['values']['project_name']+'"' 
            + ")\n")

    f.write('fn.modificaArreglo(oProject,"' + read_data()['values']['variable_name'] + ' ","' + var 
            + read_data()['values']['units'] + '")\n')
    
    f.write('oDesign = oProject.SetActiveDesign("' +read_data()['values']['design_name'] + '")\n')
    f.write("oDesign.AnalyzeAll()")
    f.write("\n")

    first = True
    for report, value in requiered_reports.items():
        if first and (report.upper() == "AMPIMB" or report.upper() == "PHASEIMB"):
            first = False
            f.write('oModule = oDesign.GetModule("OutputVariable")\n')

        f.write(get_instructions_to_reports(tag, report, value))

    f.close()
    
## Launches HFSS simulation file
def run_simulation_hfss(ansys_path = "", args= '-runscriptandexit',file_path = ""):
    if ansys_path == "":
        ansys_path = read_data()['paths']['ansys_exe']
    
    if file_path == "":
        file_path = read_data()['paths']['src']+"simulacion.py"

    state = True
    Econt = 0
    while state and Econt < 22:
        state = bool(subprocess.run([ansys_path, args, file_path]).returncode)
        if state:
            logging.info(msg.SIM_PARTICLE_FINISHED+", had an error")
            print("Falló "+str(Econt+1)+" veces, intentando ejecutar de nuevo...")
            if Econt < 21:
                time.sleep(3+Econt)
            Econt += 1
        else:
            logging.info(msg.SIM_PARTICLE_FINISHED+" ,no errors")
    #print("Intentos: "+str(Econt))
    return state

## read the simulation results
def read_simulation_results(i,j,graph):
    dataReports = {}
    requiered_reports = read_data()['values']['reports']

    files_location = read_data()['paths']['files']
    general_graphic_path = read_data()['paths']['figures']

    for report, value in requiered_reports.items():
        if report.upper() == "SMN":
            if len(value) > 0:
                for mn_val in value:
                    graphic_name = get_graphic_name(report,mn_val,i,j)
                    try:
                        dataReports["S"+str(mn_val[0])+str(mn_val[1])] = np.genfromtxt(files_location+graphic_name+".csv", skip_header = 1, delimiter = ',')
                    except:
                        fileName = get_graphic_name(report,mn_val,(i-1),j)
                        newFileName = graphic_name
                        copy_rename(fileName,newFileName)
                        dataReports["S"+str(mn_val[0])+str(mn_val[1])] = np.genfromtxt(files_location+graphic_name+".csv", skip_header = 1, delimiter = ',')
        
        elif report.upper() == "ZMN":
            if len(value) > 0:
                for mn_val in value:
                    graphic_name = get_graphic_name(report,mn_val,i,j)
                    try:
                        dataReports["Z"+str(mn_val[0])+str(mn_val[1])] = np.genfromtxt(files_location+graphic_name+".csv", skip_header = 1, delimiter = ',')
                    except:
                        fileName = get_graphic_name(report,mn_val,(i-1),j)
                        newFileName = graphic_name
                        copy_rename(fileName,newFileName)
                        dataReports["Z"+str(mn_val[0])+str(mn_val[1])] = np.genfromtxt(files_location+graphic_name+".csv", skip_header = 1, delimiter = ',')

        elif report.upper() == "GAIN":
            if len(value) > 0:
                for angle in value:
                    graphic_name = get_graphic_name(report,angle,i,j)
                    try:
                        dataReports[report.upper()+"PHI"+str(angle)] = np.genfromtxt(files_location+graphic_name+".csv", skip_header = 1, delimiter = ',')                    
                    except:
                        fileName = get_graphic_name(report,mn_val,(i-1),j)
                        newFileName = graphic_name
                        copy_rename(fileName,newFileName)
                        dataReports[report.upper()+"PHI"+str(angle)] = np.genfromtxt(files_location+graphic_name+".csv", skip_header = 1, delimiter = ',')
        
        elif report.upper() == "VSWR":
            if len(value) > 0:
                for port in value:
                    graphic_name = get_graphic_name(report,port,i,j)
                    try:
                        dataReports[report.upper()+"("+str(port)+")"] = np.genfromtxt(files_location+graphic_name+".csv", skip_header = 1, delimiter = ',')                    
                    except:
                        fileName = get_graphic_name(report,mn_val,(i-1),j)
                        newFileName = graphic_name
                        copy_rename(fileName,newFileName)
                        dataReports[report.upper()+"PHI"+str(port)] = np.genfromtxt(files_location+graphic_name+".csv", skip_header = 1, delimiter = ',')
        
        else:
            if report.upper() != "ADITIONAL_DATA":
                graphic_name = get_graphic_name(report,value,i,j)
                try:
                    dataReports[report.upper()] = np.genfromtxt(files_location+graphic_name+".csv", skip_header = 1, delimiter = ',')                    
                except:
                    fileName = get_graphic_name(report,mn_val,(i-1),j)
                    newFileName = graphic_name
                    copy_rename(fileName,newFileName)
                    dataReports[report.upper()] = np.genfromtxt(files_location+graphic_name+".csv", skip_header = 1, delimiter = ',')

    # matplotlib.use("Agg")
    if graph:
        for graphic, data in dataReports.items():
            specific_graphic_path = general_graphic_path + graphic +"_" + str(i)+"_"+str(j)
            draw_one_report(specific_graphic_path, graphic, data)
            

    # #derivative_data = np.genfromtxt("Derivative_"+str(i)+"_"+str(j)+".csv", skip_header = 1, delimiter = ',')
    # #Plot S11 and S21

    # dydx1_31 = np.gradient(s31[:,1],s31[:,0])
    # dydx2_31 = np.gradient(dydx1_31,s31[:,0])

    # dydx1_21 = np.gradient(s21[:,1],s21[:,0])
    # dydx2_21 = np.gradient(dydx1_21,s31[:,0])
    #print("second derivative max"+str(rating))
    
    #data_to_plot=[dydx2_31, s31[:,0], dydx2_21, s31[:,0]]

    #create_plot(s11,s41,'Frequency (GHz)',r'S11,S41 (dB)',direccion_graficas_s11,[],-20)
   
    #Plot S31 and S41
    #create_plot(s31,s21,'Frequency (GHz)',r'S31,S21 (dB)',direccion_graficas_s31,data_to_plot,-3)

    #create_plot_imb(amp_imb,'Frequency (GHz)',r'Amplitude Imbalance (dB)',direccion_graficas_amp,1)
    #create_plot_imb(pha_imb,'Frequency (GHz)',r'Phase Imbalance (Grad)',direccion_graficas_pha,90)

    return dataReports

def get_simulation_params():
    info = read_data()
    
    if info['info']['category'].upper() == "ANTENNA":
        num_branches = "N/A"
    else:
        num_branches = info['values']['branches']
        
    params = {
        "num_branches":num_branches,
        "iterations":info['values']['iterations'],
        "n_particles":info['values']['particles'],
        "n_variables":info['values']['n_var'],
        "nominal":info['values']['def'],
        "var_min":info['values']['min'],
        "var_max":info['values']['max'],
        "description":info['info']['description']
    }
    return params

def create_plot(data_1, data_2,label_x, label_y, save_path,derivative_data,boundary):
     #Plot S11 and S21
    figure=plt.figure(figsize=(8,6))
    plt.plot(data_1[:,0],data_1[:,1])
    plt.plot(data_2[:,0],data_2[:,1])
    plt.axhline(y=boundary, color='r', linestyle='-')
    plt.axhline(y=boundary+0.5,color='r', alpha=0.7, linestyle='-')
    plt.axhline(y=boundary-0.5, color='r', alpha=0.7, linestyle='-')

    #if derivative_data!=[]:
       # plt.plot(derivative_data[1],derivative_data[0],alpha=0.5)
       # plt.plot(derivative_data[3],derivative_data[2],alpha=0.5)
    
    plt.plot()
    plt.ylabel(label_y,fontsize=15)
    plt.xlabel(label_x,fontsize=15)
    plt.tick_params(axis='both', which='major', labelsize=15)
    plt.grid(True)
    plt.grid(color = '0.5', linestyle = '--', linewidth = 1.5)
    plt.show
    plt.savefig(save_path)
    plt.close(figure)

def create_plot_imb(data_1,label_x, label_y, save_path,boundary):
     #Plot S11 and S21
    figure=plt.figure(figsize=(8,6))
    plt.plot(data_1[:,0],data_1[:,1])
    plt.axhline(y=boundary, color='r', linestyle='-')

    plt.plot()
    plt.ylabel(label_y,fontsize=15)
    plt.xlabel(label_x,fontsize=15)
    plt.tick_params(axis='both', which='major', labelsize=15)
    plt.grid(True)
    plt.grid(color = '0.5', linestyle = '--', linewidth = 1.5)
    plt.show
    plt.savefig(save_path)
    plt.close(figure)

def copy_rename(old_file_name, new_file_name):

        files_location = os.path.join( os.path.normpath(read_data()['paths']['results']),read_data()['info']['ID'],r"files")

        print(old_file_name)
        print(new_file_name)
        os.chdir(files_location)
        shutil.copy(old_file_name,new_file_name)

def init_model():
    error = False
    data = read_data()
    
    if not os.path.isfile(data['paths']['ansys_save_def']+data['values']['project_name']+".aedt"):
        state = run_simulation_hfss(file_path = data['paths']['models']+data['values']['project_name']+".py")
        if state or not os.path.isfile(data['paths']['ansys_save_def']+data['values']['project_name']+".aedt"):
            error = True
            wait_to_read("Error, no se encontró modelo, verifique que el script de su modelo se encuentra en la carpeta models o/y que su archivo .aedt se encuentre en la carpeta Ansoft")
    
    if not error:
        print("El modelo existe, iniciando proceso de optimización")
    
    return error