# -*- coding: utf-8 -*-
"""
Authors: German Chaparro, Jorge Cardenas,Oscar Restrepo, Sergio Mora, Jhon Vera, and Jaime Angel
Year: 2022
"""
import os
from sys import platform
from datetime import datetime
import time
import json
import uuid
from . import messages


def read_data():
    """Reads the data.json file located in ./src/ and returns its contents

    Returns:
        dict | None: if the file data.json exists, returns a dictionary with its information, otherwise returns None
    """
    try:
        path = os.getcwd().replace('\\', '/') + '/src'
        with open(path + '/data.json', 'r') as file:
            data = json.load(file)
            file.close()
        return data
    except:
        input(messages.READ_FILE_ERR)


def update_data(category="", key="", value=""):
    """Updates the data.json file, modifying the value of a specific key within a given category, such as routes or info.

    Args:
        category (str, optional): category or main key, among these are paths and info. Defaults to "".
        key (str, optional): sub-category or secondary key of a category. Defaults to "".
        value (str, optional): new value. Defaults to "".

    Returns:
        dict | None: returns a dictionary with the updated data from the file data.json
    """
    try:
        path = os.getcwd().replace('\\', '/') + '/src'
        with open(path + "/data.json", "r") as file:
            data = json.load(file)
            file.close()

        with open(path + "/data.json", "w") as file:
            data[category][key] = value
            json.dump(data, file, indent=2)
            file.close()
        return data
    except:
        input(messages.R_W_FILE_ERR)


def create_data_file(
    ansys_exe, ansys_save_def, project_name, design_name, variable_name, units,
    max, min, nominals, iterations, particles,
    branches, reports, category, sub_category, description
):
    """Take the arguments, and after organizing them in a dictionary, create the file data.json inside the folder './src'.

    Args:
        ansys_exe (str): containing the path to the Ansys HFSS executable, usually found in C:/program files/
        ansys_save_def (str): containing the path where the Ansys model file is located, it is recommended to leave the default path Ansys uses to save its files.
        project_name (str): containing the name of the project within the Ansys model
        design_name (str): containing the name of the design within the Ansys model
        variable_name (str): containing the name of the array name of the model dimensions
        units (str): containing the unit of measure of the model, e.g. mm (millimeters)
        max (list[float  |  int]): List of numbers with the maximum values that the PSO can take to modify the model's dimensions.
        min (list[float  |  int]): List of numbers with the minimum values the PSO can take to modify the model's dimensions.
        nominals (list[float  |  int]): List of numbers with the nominal or default values that the model has in its dimensions.
        iterations (int): number of iterations to be executed by the PSO
        particles (int): number of particles to be executed by the PSO
        branches (int): number of branches (only for hybrids with branches)
        reports (dict): Dictionary with the reports to be generated by ansys
        category (str): containing the category you want to give to the model or optimization
        sub_category (str): containing the sub-category you want to give to the model or optimization
        description (str): containing the description of the model, the setting function, additional information
    """
    data_structure = {
        "paths": {
            "main": os.getcwd().replace('\\', '/') + '/',
            "results": os.getcwd().replace('\\', '/') + '/' + "results/",
            "files": "",
            "figures": "",
            "models": os.getcwd().replace('\\', '/') + '/' + "models/",
            "src": os.getcwd().replace('\\', '/') + '/' + "src/",
            "ansys_exe": ansys_exe,
            "ansys_save_def": ansys_save_def
        },
        "values": {
            "project_name": project_name,
            "design_name": design_name,
            "variable_name": variable_name,
            "units": units,
            "max": max,
            "min": min,
            "def": nominals,
            "n_var": len(nominals),
            "iterations": iterations,
            "particles": particles,
            "branches": branches,
            "reports": reports,
        },
        "info": {
            "OS": platform,
            "ID": "",
            "category": category,
            "sub_category": sub_category,
            "description": description,
        }
    }

    try:
        with open(data_structure['paths']['src'] + "data.json", "w") as file:
            json.dump(data_structure, file, indent=2)
            file.close()
        print(messages.C_U_SETUP_FILE)
    except:
        input(messages.CREATE_SETUP_FILE_ERR)


def clear_screen():
    """Clean the console
    """
    os.system("cls")


def wait_to_read(msj="\nError!", clr=0):
    """Concatenates the string of a message with the constant INTRO_BTN_MSG to then pause the system. Depending on the value of the clr argument, passing the wait may or may not clear the console.

    Args:
        msj (str, optional): Custom message, default is "Error!".
        clr (int, optional): Value that if 0 will clear the console. default is 0.
    """
    msj += messages.INTRO_BTN_MSG
    input(msj)

    if clr == 0:
        clear_screen()


def make_directory(name, path):
    """Creates a directory if it does not exist with the name and path passed in the arguments.

    Args:
        name (str): directory name
        path (str): path where the new directory will be created
    """
    try:
        if not os.path.isdir(name):
            os.mkdir(path + name)
            print(name + messages.CREATE_DIR + path)
    except:
        print(messages.CREATE_DIR_ERR + name)


def Y_N_question(msj):
    """Asks the user a question that requires an affirmative or negative answer (yes or no).

    Args:
        msj (str): Contains the question you want to ask.

    Returns:
        str: Affirmative (Y) or negative (N) answer to the question asked.
    """
    op = ""
    while op.upper() != messages.YES and op.upper() != messages.NO:
        op = input(msj + messages.Y_N)
        if op.upper() != messages.YES and op.upper() != messages.NO:
            wait_to_read(messages.INVALID_IN_ERR, 1)

    return op.upper()


def start_timing():
    """Records the current time when the function is called.

    Returns:
        datetime: datetime object with the date when this function is called
    """
    return datetime.now()


def get_elapsed_time(start_time=""):
    """calculates the time elapsed from a given time to the current time.

    Args:
        start_time (str, optional): containing the start date, default is "" which throughout the function is taken as the current date.

    Returns:
        string containing the elapsed time in seconds
    """
    if start_time == "":
        start_time = read_data()['info']['start_time']
    diff = datetime.now() - start_time
    return str(diff.total_seconds())


def get_instructions_to_reports(tag, report, value):
    """generates a text string containing the necessary instructions to generate an Ansys HFSS report.

    Args:
        tag (str): tag that accompanies the name of the report after it is generated, generally associated with the particle and iteration from which it is generated e.g. S11_0_0.
        report (str): report name e.g. Smn, Zmn, Gain, AmpImb, PhaseImb, VSWR, BW or DataTable
        value (list | dict | str): value of the report to be generated

    Returns:
        string containing the instructions to generate the report(s) in Ansys HFSS
    """

    instructions = ""

    if report.upper() == "SMN":
        if len(value) > 0:
            for mn_val in value:
                instructions += "fn.createsSmn(oProject,'" + tag + "','" + read_data()['info']['ID'] + "','" + str(
                    mn_val[0]
                ) + "','" + str(mn_val[1]) + "')\n"

    elif report.upper() == "ZMN":
        if len(value) > 0:
            for mn_val in value:
                instructions += "fn.createsZmn(oProject,'" + tag + "','" + read_data()['info']['ID'] + "','" + str(
                    mn_val[0]
                ) + "','" + str(mn_val[1]) + "')\n"

    elif report.upper() == "GAIN":
        if len(value) > 0:
            for angle in value:
                instructions += "fn.createsGain(oProject,'" + tag + "','" + read_data(
                )['info']['ID'] + "','" + str(angle) + "')\n"

    elif report.upper() == "AMPIMB":
        instructions = 'oModule.CreateOutputVariable("AmpImbalance", "' + str(
            value
        ) + '", "Setup1 : Sweep", "Modal Solution Data", [])\n'
        instructions += "fn.createsAmpImb(oProject,'" + tag + "','" + read_data()['info']['ID'] + "')\n"

    elif report.upper() == "PHASEIMB":
        instructions = 'oModule.CreateOutputVariable("PhaseImb", "' + str(
            value
        ) + '", "Setup1 : Sweep", "Modal Solution Data", [])\n'
        instructions += "fn.createsPhaseImb(oProject,'" + tag + "','" + read_data()['info']['ID'] + "')\n"

    elif report.upper() == "VSWR":
        if len(value) > 0:
            for port in value:
                instructions += "fn.createsVSWR(oProject,'" + tag + "','" + read_data(
                )['info']['ID'] + "','" + str(port) + "')\n"

    elif report.upper() == "BW":
        instructions = "fn.createsBW(oProject,'" + tag + "','" + read_data()['info']['ID'] + "')\n"

    elif report.upper() == "DATATABLE":
        instructions = "fn.createsDataTable(oProject,'" + tag + "','" + read_data()['info']['ID'] + "')\n"

    return instructions


def get_graphic_name(report, value, i, j):
    """generates the name of a graph based on the report, the iteration number and the particle.

    Args:
        report (str): report name
        value (list | dict | str): value of the report
        i (int): iteration number
        j (int): particle number

    Returns:
        str: name of a graph
    """
    graphic_name = ""

    if report.upper() == "SMN":
        graphic_name += "datosS" + str(value[0]) + str(value[1])

    elif report.upper() == "ZMN":
        graphic_name += "datosZ" + str(value[0]) + str(value[1])

    elif report.upper() == "GAIN":
        graphic_name += "datosGananciaPhi" + str(value)

    elif report.upper() == "AMPIMB":
        graphic_name += "amp_imb"

    elif report.upper() == "PHASEIMB":
        graphic_name += "pha_imb"

    elif report.upper() == "VSWR":
        graphic_name += "datosVSWR(" + str(value) + ")"

    elif report.upper() == "BW":
        graphic_name += "datosBW"

    elif report.upper() == "DATATABLE":
        graphic_name += "datosTabla"

    graphic_name += "_" + str(i) + "_" + str(j)

    return graphic_name


def setSimID():
    """generates a universally unique identifier (UUID) as a text string

    Returns:
        str: text string that contain a UUID
    """
    return str(uuid.uuid4())


def init_system(
    ansys_exe, ansys_save_def, project_name, design_name, variable_name, units,
    max, min, nominals, iterations, particles,
    branches, reports, category, sub_category, description
):
    """Creates the necessary directories and files that will be used in the execution of an optimization.

    Args:
        ansys_exe (str): containing the path to the Ansys HFSS executable, usually found in C:/program files/
        ansys_save_def (str): containing the path where the Ansys model file is located, it is recommended to leave the default path Ansys uses to save its files.
        project_name (str): containing the name of the project within the Ansys model
        design_name (str): containing the name of the design within the Ansys model
        variable_name (str): containing the name of the array name of the model dimensions
        units (str): containing the unit of measure of the model, e.g. mm (millimeters)
        max (list[float  |  int]): List of numbers with the maximum values that the PSO can take to modify the model's dimensions.
        min (list[float  |  int]): List of numbers with the minimum values the PSO can take to modify the model's dimensions.
        nominals (list[float  |  int]): List of numbers with the nominal or default values that the model has in its dimensions.
        iterations (int): number of iterations to be executed by the PSO
        particles (int): number of particles to be executed by the PSO
        branches (int): number of branches (only for hybrids with branches)
        reports (dict): Dictionary with the reports to be generated by ansys
        category (str): containing the category you want to give to the model or optimization
        sub_category (str): containing the sub-category you want to give to the model or optimization
        description (str): containing the description of the model, the setting function, additional information
    """
    print(messages.START_SYS)
    main_path = os.getcwd().replace('\\', '/') + '/'

    make_directory('models', main_path)
    make_directory('results', main_path)
    make_directory(main_path + 'results/comparison graphics/', '')
    make_directory('src', main_path)

    create_data_file(
        ansys_exe, ansys_save_def, project_name, design_name, variable_name, units, max, min, nominals, iterations,
        particles, branches, reports, category, sub_category, description
    )

    if ansys_exe != "":
        print(messages.READY)
        time.sleep(3)
    clear_screen()
