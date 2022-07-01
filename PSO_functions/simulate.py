# -*- coding: utf-8 -*-

from PSO_core.commands import read_data
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
    
    f.write("import PSO.ansys_functions as fn\n")

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
    f.write("fn.creaS11(oProject,'" + tag + "','"+ read_data()['info']['ID'] +"')\n")
    f.close()
    
## Launches HFSS simulation file
def run_simulation_hfss(args = ""):
    if args == "":
        subprocess.run([read_data()['paths']['ansys_exe'],'-runscriptandexit',read_data()['paths']['src']+"simulacion.py"])
    else:
        subprocess.run([read_data()['paths']['ansys_exe'],args,read_data()['paths']['src']+"simulacion.py"])

    logging.info(msg.SIM_PARTICLE_FINISHED)

## read the simulation results
def read_simulation_results(i,j):
    
    files_location = read_data()['paths']['files']

    #os.chdir(files_location)
    direccion_graficas_s11= read_data()['paths']['figures']+"S11"+"_" + str(i)+"_"+str(j)
    
    try:
        s11 = np.genfromtxt(files_location+"datosS11_"+str(i)+"_"+str(j)+
                     ".csv", skip_header = 1, delimiter = ',')
   
    except:
        filename="datosS11_"+str(i-1)+"_"+str(j)+".csv"
        new_filename="datosS11_"+str(i)+"_"+str(j)+".csv"
        copy_rename(filename,new_filename)
        
        s11 = np.genfromtxt(files_location+"datosS11_"+str(i)+"_"+str(j)+
                     ".csv", skip_header = 1, delimiter = ',')
    
    # try:

    
    #     s21 = np.genfromtxt("datosS21_"+str(i)+"_"+str(j)+
    #                  ".csv", skip_header = 1, delimiter = ',')
    
    #     direccion_graficas_s21= read_data()['paths']['results']+read_data()['info']['ID']+"/figures/S21"+"_" + str(i)+"_"+str(j)
    # except:

    #     filename="datosS21_"+str(i-1)+"_"+str(j)+".csv"
    #     new_filename="datosS21_"+str(i)+"_"+str(j)+".csv"
    #     copy_rename(filename,new_filename)

    #     s21 = np.genfromtxt("datosS21_"+str(i)+"_"+str(j)+
    #                  ".csv", skip_header = 1, delimiter = ',')
        
    #     direccion_graficas_s21= read_data()['paths']['results']+read_data()['info']['ID']+"/figures/S21"+"_" + str(i)+"_"+str(j)

    # try:

    
    #     s31 = np.genfromtxt("datosS31_"+str(i)+"_"+str(j)+
    #                  ".csv", skip_header = 1, delimiter = ',')
    
    #     direccion_graficas_s31= read_data()['paths']['results']+read_data()['info']['ID']+"/figures/S31"+"_" + str(i)+"_"+str(j)
    
    # except:
        
    #     filename="datosS31_"+str(i-1)+"_"+str(j)+".csv"
    #     new_filename="datosS31_"+str(i)+"_"+str(j)+".csv"
    #     copy_rename(filename,new_filename)

    #     s31 = np.genfromtxt("datosS31_"+str(i)+"_"+str(j)+
    #                  ".csv", skip_header = 1, delimiter = ',')
    #     direccion_graficas_s31= read_data()['paths']['results']+read_data()['info']['ID']+"/figures/S31"+"_" + str(i)+"_"+str(j)

    # try:
       

    #     s41 = np.genfromtxt("datosS41_"+str(i)+"_"+str(j)+
    #                  ".csv", skip_header = 1, delimiter = ',')
    # except:
    #     filename="datosS41_"+str(i-1)+"_"+str(j)+".csv"
    #     new_filename="datosS41_"+str(i)+"_"+str(j)+".csv"
    #     copy_rename(filename,new_filename)

    #     s41 = np.genfromtxt("datosS41_"+str(i)+"_"+str(j)+
    #                  ".csv", skip_header = 1, delimiter = ',')
    # #derivative_data = np.genfromtxt("Derivative_"+str(i)+"_"+str(j)+".csv", skip_header = 1, delimiter = ',')
    # #Plot S11 and S21

    # try:
    #     amp_imb = np.genfromtxt("amp_imb_"+str(i)+"_"+str(j)+
    #                  ".csv", skip_header = 1, delimiter = ',')
    
    #     direccion_graficas_amp= read_data()['paths']['results']+read_data()['info']['ID']+"\\figures\\amp_imb"+"_" + str(i)+"_"+str(j)
   
    # except:
    #     filename="amp_imb_"+str(i-1)+"_"+str(j)+".csv"
    #     new_filename="amp_imb_"+str(i)+"_"+str(j)+".csv"
    #     copy_rename(filename,new_filename)
        
    #     amp_imb = np.genfromtxt("amp_imb_"+str(i)+"_"+str(j)+
    #                  ".csv", skip_header = 1, delimiter = ',')
    #     direccion_graficas_amp= read_data()['paths']['results']+read_data()['info']['ID']+"\\figures\\amp_imb"+"_" + str(i)+"_"+str(j)

    # try:
    #     pha_imb = np.genfromtxt("pha_imb_"+str(i)+"_"+str(j)+
    #                  ".csv", skip_header = 1, delimiter = ',')
    
    #     direccion_graficas_pha= read_data()['paths']['results']+read_data()['info']['ID']+"\\figures\\pha_imb"+"_" + str(i)+"_"+str(j)
   
    # except:
    #     filename="pha_imb_"+str(i-1)+"_"+str(j)+".csv"
    #     new_filename="pha_imb_"+str(i)+"_"+str(j)+".csv"
    #     copy_rename(filename,new_filename)
        
    #     pha_imb = np.genfromtxt("pha_imb_"+str(i)+"_"+str(j)+
    #                  ".csv", skip_header = 1, delimiter = ',')
    #     direccion_graficas_pha= read_data()['paths']['results']+read_data()['info']['ID']+"\\figures\\pha_imb"+"_" + str(i)+"_"+str(j)


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


    #os.chdir(read_data()['paths']['results'])

    return s11#,s21,s31,s41, amp_imb

def get_simulation_params(self):
    params = {
        "simulation_type": "Antenna",
        "num_branches":str(0),
        "n_variables":read_data()['values']['n_var'],
        "iterations":read_data()['values']['iterations'],
        "n_particles":read_data()['values']['particles'],
        "nominal":read_data()['values']['def'],
        "var_min":read_data()['values']['min'],
        "var_max":read_data()['values']['max']
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