# -*- coding: utf-8 -*-
"""
Authors: German Chaparro, Jorge Cardenas,Oscar Restrepo, Sergio Mora, Jhon Vera, and Jaime Angel
Year: 2022
"""
import os
import subprocess
import logging
import time
import shutil
import numpy as np
import matplotlib.pyplot as plt
from . import messages as msg
from .commands import get_graphic_name, read_data, get_instructions_to_reports, wait_to_read
from .graphicsManagement import draw_one_report


def create_sim_file(particle: np.ndarray, i: int, j: int):
    """Create a Python script that can be executed from Ansys HFSS with the necessary instructions to open the model, modify the array in the model dimensions, generate the required reports and close the program.

    Args:
        particle (np.ndarray): numpy ndarray type, contains the dimensions to be placed in the Ansys model
        i (int): Number of iteration
        j (int): Number of particle
    """
    required_reports = read_data()['values']['reports']
    particle = particle.round(4)

    tag = "_" + str(i) + "_" + str(j)
    var = "[" + ", ".join([str(x) for x in particle]) + "]"

    f = open(read_data()['paths']['src'] + "simulacion.py", "w")
    pathProject = '"' + read_data()["paths"]["ansys_save_def"] + read_data()["values"]["project_name"] + '.aedt"'

    f.write("# -*- coding: utf-8 -*-\n")
    f.write("import PerSeO.ansys_functions as fn\n")

    f.write("\n")
    f.write("import ScriptEnv\n")
    f.write("oDesktop.RestoreWindow()\n")
    f.write("oDesktop.OpenProject(" + pathProject + ")\n")
    f.write("oProject = oDesktop.SetActiveProject(" + '"' + read_data()['values']['project_name'] + '"' + ")\n")

    f.write(
        'fn.changeArray(oProject,"' + read_data()['values']['variable_name'] + ' ","' + var +
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


def run_simulation_hfss(ansys_path="", args='-runscriptandexit', file_path=""):
    """Open Ansys HFSS and from that program run the script 'simulacion.py', if the simulation runs correctly it returns true, otherwise false.

    Args:
        ansys_path (str, optional): path where the Ansys HFSS executable is located. Defaults read ./src/data.json and take ansys_exe value.
        args (str, optional): arguments to be run by the subprocess to open ansys. Defaults to '-runscriptandexit'.
        file_path (str, optional): path where the simulation script is located. Defaults read ./src/data.json and take src value + simulacion.py.

    Returns:
        bool: returns true or false depending on whether it was possible to open Ansys and run the script 'simulacion.py' correctly.
    """
    if ansys_path == "":
        ansys_path = read_data()['paths']['ansys_exe']

    if file_path == "":
        file_path = read_data()['paths']['src'] + "simulacion.py"

    state = True
    counterError = 0
    while state and counterError < 22:
        state = bool(subprocess.run([ansys_path, args, file_path]).returncode)
        if state:
            logging.info(msg.SIM_PARTICLE_FINISHED + msg.HAD_AN_ERR)
            print(msg.EXE_P1_ERR + str(counterError + 1) + msg.EXE_P2_ERR)
            if counterError < 21:
                time.sleep(3 + counterError)
            counterError += 1
        else:
            logging.info(msg.SIM_PARTICLE_FINISHED + msg.NO_ERR)
    #print("Attempts: "+str(counterError))
    return state


def read_simulation_results(i: int, j: int, graph: bool):
    """Reads the reports of a particle in one iteration, and returns them in a dictionary, optionally graphs them.

    Args:
        i (int): Number of iteration
        j (int): Number of particle
        graph (bool): boolean value representing whether it is necessary to plot the read data

    Returns:
        dict: Returns a dictionary with the data read, where each key is the name of the report read, example S11, VSWR
    """
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
            if report.upper() != "ADDITIONAL_DATA":
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
    """reads data from the ./src/data.json file and returns a dictionary with branches, iterations, particles, dimension array size, nominal value array, minimum maxima and description.

    Returns:
        dict: dictionary with branches, iterations, particles, dimension array size, nominal value array, minimum maxima and description.
    """
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


def copy_rename(old_file_name: str, new_file_name: str):
    """Takes an existing file from the /results/ folder of the optimization id found in data.json and creates a copy with a new name in the same path

    Args:
        old_file_name (str): Existing file name
        new_file_name (str): Name of the new file
    """
    files_location = os.path.join(
        os.path.normpath(read_data()['paths']['results']),
        read_data()['info']['ID'], r"files"
    )

    print(old_file_name)
    print(new_file_name)
    os.chdir(files_location)
    shutil.copy(old_file_name, new_file_name)


def init_model():
    """Verify that the model (.aedt file) exists, otherwise it will try to run a script with the model name in the ./models/ folder. At the end it returns true or false if the model is found.

    Returns:
        bool: returns true if the model exists
    """
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
