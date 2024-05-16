# -*- coding: utf-8 -*-
"""
Authors: German Chaparro, Jorge Cardenas,Oscar Restrepo, Sergio Mora, Jhon Vera, and Jaime Angel
Year: 2022
"""
from .commands import get_graphic_name, read_data, get_instructions_to_reports, wait_to_read
from .graphicsManagement import draw_one_report
import logging
import subprocess
import os
import numpy as np
import matplotlib.pyplot as plt
import time
# modulo que contiene strings de mensajes
from . import messages as msg
import shutil
#=============================================================================
# THIS customized FUNCTION CALLS 'funciones.py' FILE AND GENERATES THE DATA
# TO BE USED BY THE OPTIMIZER.


def create_sim_file(particle: np.ndarray, i: int, j: int):
    required_reports = read_data()['values']['reports']
    particle = particle.round(4)

    tag = "_" + str(i) + "_" + str(j)  # esta linea genera el string _i_j
    var = "[" + ", ".join([str(x) for x in particle]) + "]"  # Generar string del array de datos de la partícula

    f = open(read_data()['paths']['src'] + "simulacion.py", "w")  # abre un archivo para escribir
    direccion_dibujo = '"' + read_data()["paths"]["ansys_save_def"] + read_data()["values"]["project_name"] + '.aedt"'

    f.write("# -*- coding: utf-8 -*-\n")
    f.write("import PerSeo.ansys_functions as fn\n")

    f.write("\n")
    f.write("import ScriptEnv\n")
    f.write("oDesktop.RestoreWindow()\n")
    f.write("oDesktop.OpenProject(" + direccion_dibujo + ")\n")
    f.write("oProject = oDesktop.SetActiveProject(" + '"' + read_data()['values']['project_name'] + '"' + ")\n")

    f.write(
        'fn.modificaArreglo(oProject,"' + read_data()['values']['variable_name'] + ' ","' + var +
        read_data()['values']['units'] + '")\n'
    )

    f.write('oDesign = oProject.SetActiveDesign("' + read_data()['values']['design_name'] + '")\n')
    f.write("oDesign.AnalyzeAll()")
    f.write("\n")

    first = True
    for report, value in required_reports.items():
        if first and (report.upper() == "AMPIMB" or report.upper() == "PHASEIMB"):
            first = False
            f.write('oModule = oDesign.GetModule("OutputVariable")\n')

        f.write(get_instructions_to_reports(tag, report, value))

    f.close()


## Launches HFSS simulation file
def run_simulation_hfss(ansys_path="", args='-runscriptandexit', file_path=""):
    if ansys_path == "":
        ansys_path = read_data()['paths']['ansys_exe']

    if file_path == "":
        file_path = read_data()['paths']['src'] + "simulacion.py"

    state = True
    Econt = 0
    while state and Econt < 22:
        state = bool(subprocess.run([ansys_path, args, file_path]).returncode)
        if state:
            logging.info(msg.SIM_PARTICLE_FINISHED + msg.HAD_AN_ERR)
            print(msg.EXE_P1_ERR + str(Econt + 1) + msg.EXE_P2_ERR)
            if Econt < 21:
                time.sleep(3 + Econt)
            Econt += 1
        else:
            logging.info(msg.SIM_PARTICLE_FINISHED + msg.NO_ERR)
    #print("Intentos: "+str(Econt))
    return state


## read the simulation results
def read_simulation_results(i, j, graph):
    dataReports = {}
    required_reports = read_data()['values']['reports']

    files_location = read_data()['paths']['files']
    general_graphic_path = read_data()['paths']['figures']

    for report, value in required_reports.items():
        if report.upper() == "SMN":
            if len(value) > 0:
                for mn_val in value:
                    graphic_name = get_graphic_name(report, mn_val, i, j)
                    try:
                        dataReports["S" + str(mn_val[0]) + str(mn_val[1])] = np.genfromtxt(
                            files_location + graphic_name + ".csv", skip_header=1, delimiter=','
                        )
                    except:
                        fileName = get_graphic_name(report, mn_val, (i - 1), j)
                        newFileName = graphic_name
                        copy_rename(fileName, newFileName)
                        dataReports["S" + str(mn_val[0]) + str(mn_val[1])] = np.genfromtxt(
                            files_location + graphic_name + ".csv", skip_header=1, delimiter=','
                        )

        elif report.upper() == "ZMN":
            if len(value) > 0:
                for mn_val in value:
                    graphic_name = get_graphic_name(report, mn_val, i, j)
                    try:
                        dataReports["Z" + str(mn_val[0]) + str(mn_val[1])] = np.genfromtxt(
                            files_location + graphic_name + ".csv", skip_header=1, delimiter=','
                        )
                    except:
                        fileName = get_graphic_name(report, mn_val, (i - 1), j)
                        newFileName = graphic_name
                        copy_rename(fileName, newFileName)
                        dataReports["Z" + str(mn_val[0]) + str(mn_val[1])] = np.genfromtxt(
                            files_location + graphic_name + ".csv", skip_header=1, delimiter=','
                        )

        elif report.upper() == "GAIN":
            if len(value) > 0:
                for angle in value:
                    graphic_name = get_graphic_name(report, angle, i, j)
                    try:
                        dataReports[report.upper() + "PHI" + str(angle)] = np.genfromtxt(
                            files_location + graphic_name + ".csv", skip_header=1, delimiter=','
                        )
                    except:
                        fileName = get_graphic_name(report, mn_val, (i - 1), j)
                        newFileName = graphic_name
                        copy_rename(fileName, newFileName)
                        dataReports[report.upper() + "PHI" + str(angle)] = np.genfromtxt(
                            files_location + graphic_name + ".csv", skip_header=1, delimiter=','
                        )

        elif report.upper() == "VSWR":
            if len(value) > 0:
                for port in value:
                    graphic_name = get_graphic_name(report, port, i, j)
                    try:
                        dataReports[report.upper() + "(" + str(port) + ")"] = np.genfromtxt(
                            files_location + graphic_name + ".csv", skip_header=1, delimiter=','
                        )
                    except:
                        fileName = get_graphic_name(report, mn_val, (i - 1), j)
                        newFileName = graphic_name
                        copy_rename(fileName, newFileName)
                        dataReports[report.upper() + "PHI" + str(port)] = np.genfromtxt(
                            files_location + graphic_name + ".csv", skip_header=1, delimiter=','
                        )

        else:
            if report.upper() != "ADITIONAL_DATA":
                graphic_name = get_graphic_name(report, value, i, j)
                try:
                    dataReports[report.upper()] = np.genfromtxt(
                        files_location + graphic_name + ".csv", skip_header=1, delimiter=','
                    )
                except:
                    fileName = get_graphic_name(report, mn_val, (i - 1), j)
                    newFileName = graphic_name
                    copy_rename(fileName, newFileName)
                    dataReports[report.upper()] = np.genfromtxt(
                        files_location + graphic_name + ".csv", skip_header=1, delimiter=','
                    )

    # matplotlib.use("Agg")
    if graph:
        for graphic, data in dataReports.items():
            specific_graphic_path = general_graphic_path + graphic + "_" + str(i) + "_" + str(j)
            draw_one_report(specific_graphic_path, graphic, data)

    return dataReports


def get_simulation_params():
    info = read_data()

    if info['info']['category'].upper() == "ANTENNA":
        num_branches = "N/A"
    else:
        num_branches = info['values']['branches']

    params = {
        "num_branches": num_branches,
        "iterations": info['values']['iterations'],
        "n_particles": info['values']['particles'],
        "n_variables": info['values']['n_var'],
        "nominal": info['values']['def'],
        "var_min": info['values']['min'],
        "var_max": info['values']['max'],
        "description": info['info']['description']
    }
    return params


def create_plot(data_1, data_2, label_x, label_y, save_path, derivative_data, boundary):
    #Plot S11 and S21
    figure = plt.figure(figsize=(8, 6))
    plt.plot(data_1[:, 0], data_1[:, 1])
    plt.plot(data_2[:, 0], data_2[:, 1])
    plt.axhline(y=boundary, color='r', linestyle='-')
    plt.axhline(y=boundary + 0.5, color='r', alpha=0.7, linestyle='-')
    plt.axhline(y=boundary - 0.5, color='r', alpha=0.7, linestyle='-')

    plt.plot()
    plt.ylabel(label_y, fontsize=15)
    plt.xlabel(label_x, fontsize=15)
    plt.tick_params(axis='both', which='major', labelsize=15)
    plt.grid(True)
    plt.grid(color='0.5', linestyle='--', linewidth=1.5)
    plt.show
    plt.savefig(save_path)
    plt.close(figure)


def create_plot_imb(data_1, label_x, label_y, save_path, boundary):
    #Plot S11 and S21
    figure = plt.figure(figsize=(8, 6))
    plt.plot(data_1[:, 0], data_1[:, 1])
    plt.axhline(y=boundary, color='r', linestyle='-')

    plt.plot()
    plt.ylabel(label_y, fontsize=15)
    plt.xlabel(label_x, fontsize=15)
    plt.tick_params(axis='both', which='major', labelsize=15)
    plt.grid(True)
    plt.grid(color='0.5', linestyle='--', linewidth=1.5)
    plt.show
    plt.savefig(save_path)
    plt.close(figure)


def copy_rename(old_file_name, new_file_name):

    files_location = os.path.join(
        os.path.normpath(read_data()['paths']['results']),
        read_data()['info']['ID'], r"files"
    )

    print(old_file_name)
    print(new_file_name)
    os.chdir(files_location)
    shutil.copy(old_file_name, new_file_name)


def init_model():
    error = False
    data = read_data()

    if not os.path.isfile(data['paths']['ansys_save_def'] + data['values']['project_name'] + ".aedt"):
        state = run_simulation_hfss(file_path=data['paths']['models'] + data['values']['project_name'] + ".py")
        if state or not os.path.isfile(data['paths']['ansys_save_def'] + data['values']['project_name'] + ".aedt"):
            error = True
            wait_to_read(msg.INEXISTENT_DESIGN)

    if not error:
        print(msg.FIND_DESIGN)

    return error
