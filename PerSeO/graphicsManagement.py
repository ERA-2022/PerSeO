"""
Authors: German Chaparro, Jorge Cardenas,Oscar Restrepo, Sergio Mora, Jhon Vera, and Jaime Angel
Year: 2022
"""
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from . import messages as msg
from .commands import read_data, Y_N_question, wait_to_read, make_directory


def size_of_step(init_freq: int | float, final_freq: int | float, num_steps: int):
    """Calculates the amount of data that a report will generate based on the initial frequency, final frequency and number of points in the sweep, both frequency values must be in the same scientific notation.

    Args:
        init_freq (int | float): numerical value of the initial frequency of the model analysis in Ansys HFSS
        final_freq (int | float): numerical value of the final frequency of the model analysis in Ansys HFSS
        num_steps (int): number of steps or points used in the sweep analysis

    Returns:
        float: numerical value representing the amount of data that a report can deliver.
    """
    return ((final_freq - init_freq) / (num_steps - 1))


def draw_one_report(path="", report_n="", data=[], points=0, units=""):
    """Generates the graph of an AnsysHFSS report, such as the Smn, Zmn, AmpImb, PhaseImb, Gain and VSWR.

    Args:
        path (str, optional): path where the graphic will be saved.
        report_n (str, optional): Name of the report to be plotted.
        data (list, optional): data to be plotted.
        points (int, optional): number of points used in the sweep analysis (point on the x-axis). By default it take the points obtained in the ./src/data.json file
        units (str, optional): data units, e.g. KHz, MHz, GHz. By default it take the units obtained in the ./src/data.json file.
    """

    matplotlib.use("Agg")
    if points <= 0:
        points = read_data()['values']['reports']["additional_data"]["points"]
    if units == "":
        units = read_data()['values']['reports']["additional_data"]["units"]

    if "GAIN" in report_n.upper() or "GANANCIA" in report_n.upper():
        if points >= 100:
            steps = 10
        elif points < 100 and points >= 50:
            steps = 5
        elif points < 50 and points >= 20:
            steps = 2
        else:
            steps = 1

        x = np.arange(1, points, steps)
        figure = plt.figure(figsize=(8, 6))
        for k in x:
            plt.plot(data[:, 0], data[:, k])
            plt.ylabel(r'Gain (lineal)', fontsize=18)
            plt.xlabel(r'$\theta$ (deg)', fontsize=18)
            plt.title(r'optimized (Plane $\phi$=' + report_n.replace("GAINPhi", "") + ")", fontsize=18)
            plt.tick_params(axis='both', which='major', labelsize=18)
            plt.grid(True)
            plt.grid(color='0.5', linestyle='--', linewidth=2)
        plt.savefig(path)
        plt.close(figure)

    elif "Z" in report_n.upper():
        x_name = "Frequency (" + units + ")"
        figure = plt.figure(figsize=(8, 6))
        plt.plot(data[:, 0], data[:, 1], label="Re")
        plt.plot(data[:, 0], data[:, 2], label="Im")
        plt.ylabel("Y", fontsize=18)
        plt.xlabel(x_name, fontsize=18)
        plt.tick_params(axis='both', which='major', labelsize=18)
        plt.grid(True)
        plt.grid(color='0.5', linestyle='--', linewidth=2)
        plt.legend(loc=1, prop={'size': 12})
        plt.title(report_n)
        plt.savefig(path)
        plt.close(figure)
    else:
        x_name = "Frequency (" + units + ")"
        y_name = ""
        if "VS" in report_n.upper():
            y_name = report_n

        elif report_n == "PHASEIMB":
            y_name = "Phase Imbalance (dB)"

        elif "S" in report_n.upper():
            y_name = report_n + " (dB)"

        elif report_n == "AMPIMB":
            y_name = "Amplitude Imbalance (dB)"

        if y_name != "":
            figure = plt.figure(figsize=(8, 6))
            plt.plot(data[:, 0], data[:, 1])
            plt.ylabel(y_name, fontsize=18)
            plt.xlabel(x_name, fontsize=18)
            plt.tick_params(axis='both', which='major', labelsize=18)
            plt.grid(True)
            plt.grid(color='0.5', linestyle='--', linewidth=2)
            plt.savefig(path)
            plt.close(figure)


def get_data_for_one_report():
    """Prompts the user for a simulation ID and a report to plot, then reads the file and plots it.
    """
    temp_path = os.getcwd().replace('\\', '/') + '/results/'

    valid = False
    while not valid:
        id_for_read = input(msg.REQUEST_ID)
        if not os.path.isdir(temp_path + id_for_read):
            if Y_N_question(msg.INVALID_ID_ERR) == msg.NO:
                break
        else:
            valid = True

    if valid:
        valid = False
        while not valid:
            file_path = temp_path + id_for_read + '/'
            file_name = input(msg.REQUEST_FILE_NAME)
            if not ".csv" in file_name:
                file_name += ".csv"

            file_path += "files/" + file_name

            if not os.path.isfile(file_path):
                if Y_N_question(msg.INEXISTENT_FILE_ERR) == msg.NO:
                    break
            else:
                valid = True

    if valid:
        complement = file_name.replace("datos",
                                       "").replace(".csv",
                                                   "").replace("GananciaPhi",
                                                               "GAINPHI").replace("amp_imb", "AMPIMB"
                                                                                  ).replace("pha_imb",
                                                                                            "PHASEIMB").split("_")
        data = np.genfromtxt(file_path, skip_header=1, delimiter=',')
        fig_path = temp_path + id_for_read + "/figures/" + complement[0] + "_" + complement[1] + "_" + complement[2]
        points = len(data)

        if "GAINPHI" in complement[0]:
            points = len(data[0]) - 1
            units = ""
        else:
            units = input(msg.REQUEST_MAGNITUDE_FREQ)

        draw_one_report(fig_path, complement[0], data, points, units)
        wait_to_read(msg.END_GRAPHIC_PROCESS)


def draw_all_iteration():
    """Prompts the user for a simulation ID and a iteration to plot, then reads the files and plots it.
    """
    temp_path = os.getcwd().replace('\\', '/') + '/results/'
    valid = False
    while not valid:
        id_for_read = input(msg.REQUEST_ID)
        if not os.path.isdir(temp_path + id_for_read):
            if Y_N_question(msg.INVALID_ID_ERR) == msg.NO:
                break
        else:
            valid = True

    if valid:
        temp_path += id_for_read + "/"
        iteration = -1
        some_file_found = False
        while not some_file_found:

            while iteration < 0:
                try:
                    iteration = int(input(msg.REQUEST_ITERATION))

                    if iteration < 0:
                        wait_to_read(msg.VALUE_ERR)
                    else:
                        allFiles = os.listdir(temp_path + "files/")
                        specific_path = temp_path + "figures/"
                        units = input(msg.REQUEST_MAGNITUDE_FREQ)
                        for file in allFiles:
                            if f"_{iteration}_" in file:
                                if not some_file_found:
                                    some_file_found = True
                                complement = file.replace("datos", "").replace(".csv", "").replace(
                                    "GananciaPhi", "GAINPHI"
                                ).replace("amp_imb", "AMPIMB").replace("pha_imb", "PHASEIMB").split(f"_{iteration}_")
                                data = np.genfromtxt(temp_path + "files/" + file, skip_header=1, delimiter=',')
                                save_path = specific_path + complement[0] + "_" + str(iteration) + "_" + complement[1]
                                points = len(data)
                                if "GAINPHI" in complement[0]:
                                    points = len(data[0]) - 1
                                print(f"{msg.DRAWING_A_GRAPHIC} ---> {file}")
                                draw_one_report(save_path, complement[0], data, points, units)
                except:
                    print(msg.READ_ITERATION_DATA_ERR)

            if some_file_found:
                wait_to_read(msg.END_GRAPHIC_PROCESS)
            else:
                msj = f"\n{msg.FILE_ITERATION_P1_ERR} {iteration} {msg.FILE_ITERATION_P2_ERR}"
                iteration = -1
                if Y_N_question(msj) == msg.NO:
                    break


def draw_all_optimization():
    """It prompts the user for a simulation ID to plot, then reads all files in that simulation and plots them.
    """
    results_path = os.getcwd().replace('\\', '/') + '/results/'

    reports_exist = False
    while not reports_exist:
        id_for_read = input(msg.REQUEST_ID)
        if not os.path.isdir(results_path + id_for_read):
            if Y_N_question(msg.INVALID_ID_ERR) == msg.NO:
                break
        else:
            reports_exist = True

    if reports_exist:

        results_path += id_for_read + "/"

        allFiles = os.listdir(results_path + "files/")
        specific_path = results_path + "figures/"
        units = input(msg.REQUEST_MAGNITUDE_FREQ)
        cont = 0
        for file in allFiles:
            complement = file.replace("datos",
                                      "").replace(".csv",
                                                  "").replace("GananciaPhi",
                                                              "GAINPHI").replace("amp_imb", "AMPIMB"
                                                                                 ).replace("pha_imb",
                                                                                           "PHASEIMB").split("_")
            data = np.genfromtxt(results_path + "files/" + file, skip_header=1, delimiter=',')
            temp_path = specific_path + complement[0] + "_" + str(complement[1]) + "_" + complement[2]
            points = len(data)

            if "GAINPHI" in complement[0]:
                points = len(data[0]) - 1
            print(f"{msg.DRAWING_A_GRAPHIC} ---> {file}")
            cont += 1
            draw_one_report(temp_path, complement[0], data, points, units)

        print(f"{msg.FILES_R_D}:{cont}")
        wait_to_read(msg.END_GRAPHIC_PROCESS)


def draw_a_comparison():
    """It prompts the user for the path to two .csv files, a save path and additional information about the chart, such as title and axis name.
    """
    Valid = False
    while not Valid:
        filePath1 = input(msg.REQUEST_PATH_FILE_1)
        if os.path.isfile(filePath1):
            if ".csv" in filePath1:
                Valid = True
            else:
                if Y_N_question(msg.EXTENSION_FILE_ERR) == msg.NO:
                    break
        else:
            if Y_N_question(msg.INVALID_PATH_ERR) == msg.NO:
                break

    if Valid:
        Valid = False
        while not Valid:
            filePath2 = input(msg.REQUEST_PATH_FILE_2)
            if os.path.isfile(filePath2):
                if ".csv" in filePath2:
                    Valid = True
                else:
                    if Y_N_question(msg.EXTENSION_FILE_ERR) == msg.NO:
                        break
            else:
                if Y_N_question(msg.INVALID_PATH_ERR) == msg.NO:
                    break

    if Valid:
        Valid = False
        while not Valid:
            print(msg.ADD_NOTE_SAVE_PATH)
            savePath = input(msg.REQUEST_SAVE_PATH)

            if savePath == "":
                savePath = os.getcwd().replace('\\', '/') + '/'

                make_directory('results', savePath)
                savePath += "results/"

                make_directory(savePath + 'comparison graphics/', "")
                savePath += "comparison graphics/"

            else:
                if savePath[-1] != "/" and savePath[-1] != "\\":
                    savePath += "/"

            if os.path.isdir(savePath):
                Valid = True
            else:
                if Y_N_question(msg.INVALID_PATH_ERR) == msg.NO:
                    break

    if Valid:
        x_name = input(msg.REQUEST_X_LABEL)
        y_name = input(msg.REQUEST_Y_LABEL)
        graphicTitle = input(msg.REQUEST_TITLE)
        label1 = input(msg.REQUEST_FILE_1_LABEL)
        label2 = input(msg.REQUEST_FILE_2_LABEL)

        data1 = np.genfromtxt(filePath1, skip_header=1, delimiter=',')
        data2 = np.genfromtxt(filePath2, skip_header=1, delimiter=',')
        figure = plt.figure(figsize=(8, 6))
        plt.plot(data1[:, 0], data1[:, 1], label=label1)
        plt.plot(data2[:, 0], data2[:, 1], label=label2)
        plt.ylabel(y_name, fontsize=18)
        plt.xlabel(x_name, fontsize=18)
        plt.tick_params(axis='both', which='major', labelsize=18)
        plt.grid(True)
        plt.grid(color='0.5', linestyle='--', linewidth=2)
        plt.legend(loc=1, prop={'size': 12})
        plt.title(graphicTitle)
        plt.savefig(savePath + graphicTitle)
        plt.close(figure)
        wait_to_read(msg.END_GRAPHIC_COMPARISON_PROCESS)
