"""
	Authors: German Chaparro, Jorge Cardenas,Oscar Restrepo, Sergio Mora, Jhon Vera, and Jaime Angel
	Year: 2022
"""
from os import path
from . import messages
from . import ansys_functions
from . import commands

try:
    if not path.isfile("src/data.json"):
        commands.init_system("", "", "", "", "", "", [], [], [], 0, 0, 0, {}, "", "", "")

except:
    print(messages.FIRST_RUN_ERR)
