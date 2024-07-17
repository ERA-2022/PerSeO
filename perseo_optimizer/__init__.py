#  -*- coding: utf-8 -*-
"""
The overall vision of PerSeO is to help people optimize RF designs modeled in Ansys HFSS and get better performance before construction without requiring very advanced Python knowledge. It offers freedom over the tuning function, applies the PSO optimization algorithm for this purpose and generates logs about the executed optimizations and generated reports to be used at any time.

Modules:
    messages

    commands

    ansys_functions

    dataManagement

    graphicsManagement

    interface

    optimize

    pso
    
    simulate

Authors: German Chaparro, Jorge Cardenas,Oscar Restrepo, Sergio Mora, Jhon Vera and Jaime Angel
Contributors: Daniela Paez Díaz
Year: 2022
"""
from os import path
from . import messages
from . import commands
from . import ansys_functions


try:
    if not path.isfile("src/data.json"):
        commands.init_system("", "", "", "", "", "", [], [], [], 0, 0, 0, {}, "", "", "")

except:
    print(messages.FIRST_RUN_ERR)

try:
    from . import dataManagement
    from . import graphicsManagement
    from . import interface
    from . import optimize
    from . import pso
    from . import simulate
except:
    pass
