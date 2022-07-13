from PSO_core import commands
from PSO_functions import Interfaz,simulate
import numpy as np

exe = "C:/Program Files/AnsysEM/Ansys Student/v212/Win64/ansysedtsv.exe"
save = "C:/Users/ESTACION/Documents/Ansoft/"
pname = "DIPOLE_BLADE_ANTENNA"
dname = "DESIGN"
vname = "variables"
u = "mm"
ma = [12650, 1300, 1600, 65, 20, 2.5, 1700]
mi = [8200, 750, 950, 30, 20, 2.5, 750]
nom = [8333.33, 813.33, 1043.33, 36.66, 20, 2.5, 866.66]
i = 3
p = 3
desc = "100%BW con BW ideal a 80MHz, denominador (o frecuencia de corte)en 40MHz trabajando en la banda de frecuencia de 40MHz hasta 120MHz"

def fit (s11):
    areas_f = []
    areas_d = []
    new_area = True
    for data in s11:
        if data[1] < -9.8:
            if new_area:
                new_area = False
                areas_f.append([])
                areas_d.append([])
            areas_f[len(areas_f)-1].append(data[0])
            areas_d[len(areas_d)-1].append(data[1])
        else:
            new_area = True

    print(f"\nNumero de areas: {len(areas_f)} || Mat.freq y Mat.db con mismo tamaño: {len(areas_f) == len(areas_d)}\n")
    
    coeficiente = 0
    if len(areas_f)==0:
        coeficiente = 20
    else:
        bw = 0
        freq = 0
        for area in range(len(areas_f)):
            temp = areas_f[area][len(areas_f[area])-1] - areas_f[area][0]
            print(f">{temp}")
            if bw < temp:
                bw = temp
                freq = areas_f[area][areas_d[area].index(np.min(areas_d[area]))]
            
        if bw > 0:
            print("INFO PREVIEW")
            print(f"BW: {bw}Mhz")
            print(f"Freq: {freq}Mhz")
            coeficiente =  ((80-bw)/80)**2  
            print(f"Valor función de merito: {coeficiente}")
            print("---------------------------------------------------\n\n")
        else:
            coeficiente = 20      

    return coeficiente

# -> Futuro modulo de optimización
commands.init_system(exe,save,pname,dname,vname,u,ma,mi,nom,i,p,desc)
simulate.run_simulation_hfss(file_path="src/dibuja.py")
#simulate.run_simulation_hfss(args="-Runscript")
Interfaz.main_menu(fit)