from os import path
from . import ansys_functions
from . import commands
from . import messages
from . import Tester

try:
    if not path.isfile("src/data.json"):
        commands.init_system("","","","","","",[],[],[],0,0,0,{},"","","")

except:
    print("Error al tratar de ejecutar el primer arranque")
