# -*- coding: utf-8 -*-

from PSO_core.commands import get_graphic_name, read_data, get_instructions_to_reports
import logging
import subprocess
import os
import numpy as np
import matplotlib.pyplot as plt
# modulo que contiene strings de mensajes
import PSO_core.messages as msg
import shutil
#=============================================================================
# THIS customized FUNCTION CALLS 'funciones.py' FILE AND GENERATES THE DATA
# TO BE USED BY THE OPTIMIZER.

def create_sim_file(particle, i, j):
    requiered_reports = read_data()['values']['reports']
    particle = particle.round(4)  
    
    # if global_.A_dimension_index>6 and global_.A_dimension_index<12:

    #     L = 3.33
    # elif global_.A_dimension_index>12:
    #     L = 3.33
    # else:
    #     L = 3.33

    tag = "_"+str(i)+"_"+str(j)     #esta linea genera el string _i_j
    var = "[" + ", ".join([str(x) for x in particle]) + "]" #Generar string del array de datos de la particula
    #var_L = str(L)
    #os.chdir( os.path.normpath(read_data()['paths']['src']+""))
    
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

    unwritten_OV = True
    for report, value in requiered_reports.items():
        if unwritten_OV and (report.upper() == "AMPIMB" or report.upper() == "PHASEIMB"):
            unwritten_OV = False
            f.write('oModule = oDesign.GetModule("OutputVariable")\n')

        f.write(get_instructions_to_reports(tag, report, value))

    f.close()
    
## Launches HFSS simulation file
def run_simulation_hfss(ansys_path= read_data()['paths']['ansys_exe'], args= '-runscriptandexit',file_path= read_data()['paths']['src']+"simulacion.py"):
    # if ansys_path == "":
    #     ansys_path = read_data()['paths']['ansys_exe']
    subprocess.run([ansys_path, args, file_path])
    logging.info(msg.SIM_PARTICLE_FINISHED)

## read the simulation results
def read_simulation_results(i,j):
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
    for graphic, data in dataReports.items():
        specific_graphic_path = general_graphic_path + graphic +"_" + str(i)+"_"+str(j)
        
        if "GAIN" in graphic:
            x=np.arange(1,requiered_reports["aditional_data"]["points"],10)
            y=np.arange(1,6,1)
            colours=['b','g','b','k','y','r']
            figure=plt.figure(figsize=(8,6)) 
            for k in x:
                plt.plot(data[:,0],data[:,k],label = str(k+(requiered_reports["aditional_data"]["fmin"]-1)) +requiered_reports["aditional_data"]["units"])
                plt.legend(loc = 1,prop={'size': 12})
                plt.ylabel(r'Gain (lineal)',fontsize=18)
                plt.xlabel(r'$\theta$ (deg)',fontsize=18)
                plt.title(r'optimized (Plane $\phi$='+graphic.replace("GAINPhi","")+")",fontsize=18)
                plt.tick_params(axis='both', which='major', labelsize=18)
                plt.grid(True)
                plt.grid(color = '0.5', linestyle = '--', linewidth = 2)
            plt.savefig(specific_graphic_path)
            plt.close(figure)

        else:
            x_name = "Frequency (" + requiered_reports['aditional_data']['units']+")"
            y_name = ""
            if "S" in graphic:
                y_name = graphic + " (dB)"

            elif "V" in graphic:
                y_name = graphic + " (1)"
            
            elif graphic == "AMPIMB":
                y_name = "Amplitude Imbalance (dB)"
            
            if y_name != "":
                figure=plt.figure(figsize=(8,6))
                plt.plot(data[:,0],data[:,1])
                plt.ylabel(y_name,fontsize=18)
                plt.xlabel(x_name,fontsize=18)
                plt.tick_params(axis='both', which='major', labelsize=18)
                plt.grid(True)
                plt.grid(color = '0.5', linestyle = '--', linewidth = 2)
                plt.savefig(specific_graphic_path)
                plt.close(figure)

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