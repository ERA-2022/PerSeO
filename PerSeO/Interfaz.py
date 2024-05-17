# -*- coding: utf-8 -*-
"""
Authors: German Chaparro, Jorge Cardenas,Oscar Restrepo, Sergio Mora, Jhon Vera, and Jaime Angel
Year: 2022
"""
import time
from . import messages as msg
from . import graphicsManagement as graphics
from .commands import clear_screen, wait_to_read, read_data, Y_N_question, update_data
from .optimize import main, only_fit
from .simulate import init_model


def ops_main_menu():
    """It displays the main menu on the console and prompts the user to enter a menu option which is returned by this function.

    Returns:
        int: numerical value representing the option selected in the main menu by the user.
    """
    op = ""
    clear_screen()
    while (op != '1' and op != '2' and op != '3' and op != '4'):  # and op != '5' and op != '6'):
        print("\n-------->PSO APP<---------")
        print(f"-----\\{msg.MAIN_MENU}")
        print(f"1> {msg.OPTIMIZE}")
        print(f"2> {msg.FFT}")
        print(f"3> {msg.GRAPHICS_TOOLS}")
        # print("4> Run script")
        # print("5> Set up")
        print(f"4> {msg.EXIT}")
        op = input(msg.ENTER_AN_OPTION)

        if op != '1' and op != '2' and op != '3' and op != '4':  # and op != '5' and op != '6':
            wait_to_read(msg.INVALID_OPTION)
    return int(op)


def ops_set_up_menu():
    """It displays the set up menu on the console and prompts the user to enter a menu option which is returned by this function.

    Returns:
        int: numerical value representing the option selected in the set up main menu by the user.
    """
    op = ""
    clear_screen()
    while (op != '1' and op != '2' and op != '3'):
        print(f"\n-----\\{msg.SET_UP_MENU}")
        print(f"1> {msg.MOD_PATHS}")
        print(f"2> {msg.SHOW_VALUES}")
        print(f"3> {msg.BACK}")
        #print(f"2> {msg.MOD_VALUES}")
        op = input(msg.ENTER_AN_OPTION)

        if op != '1' and op != '2' and op != '3':
            wait_to_read(msg.INVALID_OPTION)
    return int(op)


def ops_graphics_tools():
    """It displays the graphic tools menu on the console and prompts the user to enter a menu option which is returned by this function.

    Returns:
        int: numerical value representing the option selected in the graphic tools menu by the user.
    """
    op = ""
    clear_screen()
    while (op != '1' and op != '2' and op != '3' and op != '4' and op != '5'):
        print(f"-----\\{msg.GRAPHICS_TOOLS}")
        print(f"1> {msg.DW_ONE_REPORT}")
        print(f"2> {msg.DW_ONE_COMPLETE_ITERATION}")
        print(f"3> {msg.DW_ONE_COMPLETE_EXECUTION}")
        print(f"4> {msg.DW_ONE_REPORTS_COMPARISONS}")
        print(f"5> {msg.BACK}")
        op = input(msg.ENTER_AN_OPTION)

        if op != '1' and op != '2' and op != '3' and op != '4' and op != '5':
            wait_to_read(msg.INVALID_OPTION)
    return int(op)


def graphic_tools_menu():
    """use the ops_graphics_tools function to show get an option from the graphic tools menu, then execute the action corresponding to the selected option
    """
    volver = False
    while not volver:
        op = ops_graphics_tools()

        if op == 1:
            graphics.get_data_for_one_report()
        elif op == 2:
            graphics.draw_all_iteration()
        elif op == 3:
            graphics.draw_all_optimization()
        elif op == 4:
            graphics.draw_a_comparison()
        elif op == 5:
            volver = True
            clear_screen()
        else:
            wait_to_read(msg.ANOMALY_ERR)


def set_up_menu():
    """use the ops_set_up_menu function to show get an option from the set up menu, then execute the action corresponding to the selected option
    """
    volver = False
    while not volver:
        op = ops_set_up_menu()

        if op == 1:
            info = read_data()
            print(f"\n{msg.CURRENT_VALUES}:")
            for key, value in info['paths'].items():
                print(key + " -> " + value)
            print()
            for key, value in info['paths'].items():
                if Y_N_question(msg.CHANGE_VALUE_1 + key + msg.CHANGE_VALUE_2) == msg.YES:
                    new_val = str(input(msg.REQUEST_NEW_VAL + key + ": "))
                    update_data("paths", key, new_val)

                    if read_data()['paths'][key] == new_val:
                        wait_to_read(msg.CHANGE_SUCCESSFUL)
                    else:
                        wait_to_read(msg.ANOMALY_ERR_2)
        elif op == 2:
            clear_screen()
            print(f"\n{msg.CURRENT_VALUES}:")
            for key, value in read_data()['paths'].items():
                print(key + " -> " + value)
            wait_to_read("")
        elif op == 3:
            volver = True
            clear_screen()
        else:
            wait_to_read(msg.ANOMALY_ERR)


def main_menu(fitness):
    """this function uses the ops_main_menu function to display and obtain an option from the main menu, then it executes the action corresponding to the selected option, it receives as parameter a function which will be used as an adjustment function in the process of optimizing option one or two of the menu, this adjustment function in turn must receive as parameter a dictionary where the access key will be the name of the report and the associated value will be the data obtained..
    Args:
        fitness (function(dataReports: dict)): The adjustment function to be used in the optimization process must receive as a parameter a dictionary with the names of the reports generated in Ansys HFSS, where the access key will be the name of the report and the associated value will be the data obtained.
    """
    salir = False
    while not salir:
        op = ops_main_menu()
        if op == 1:
            ready = not init_model()
            if ready:
                main(fitness)
                wait_to_read(msg.END_EXE)
            else:
                wait_to_read(msg.INEXISTENT_DESIGN)
        elif op == 2:
            only_fit(fitness)
            wait_to_read(msg.END_EXE)
        elif op == 3:
            graphic_tools_menu()
        elif op == 4:
            print(f"\n{msg.FINAL_MSG}")
            time.sleep(2)
            clear_screen()
            salir = True
        # elif op == 5:
        #     set_up_menu()
        # elif op == 6:
        #     print("\nGracias por usar nuestro software!")
        #     time.sleep(2)
        #     clear_screen()
        #     salir = True
        else:
            wait_to_read(msg.ANOMALY_ERR)
