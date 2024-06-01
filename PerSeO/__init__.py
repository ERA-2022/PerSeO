"""
Authors: German Chaparro, Jorge Cardenas,Oscar Restrepo, Sergio Mora, Jhon Vera, and Jaime Angel
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
