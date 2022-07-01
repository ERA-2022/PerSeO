from PSO_core import commands
from PSO_functions import Interfaz, optimizate,simulate
import numpy as np

exe = "C:/Program Files/AnsysEM/Ansys Student/v212/Win64/ansysedtsv.exe"
save = "C:/Users/ESTACION/Documents/Ansoft/"
pname = "DIPOLE_BLADE_ANTENNA"
dname = "DESIGN"
vname = "variables"
u = "mm"
ma = [12050.0, 1000.0, 1500.0, 50.0, 20.0, 780.0]
mi = [11950.0, 300.0, 800.0, 5.0, 20.0, 730.0]
nom = [12000.0, 694.28571, 1180.0, 20.0, 20.0, 750.0]
i = 3
p = 3
desc = "100%BW con BW ideal a 80MHz, denominador (o frecuencia de corte)en 40MHz trabajando en la banda de frecuencia de 40MHz hasta 120MHz"

def fit (s11):
    adaptabilidad = s11[s11[:,1] < -9.8] #->db primer filtro de datos que estén por debajo del valor que acompaña la condición
    temp = []
    temp_2 = []
    #freq_min = 0
    adp_min = 0        
    coeficiente = 0
    if len(adaptabilidad)==0:
        coeficiente = 20
    else:
        for dupla in adaptabilidad:
            temp.append(dupla[0])
            temp_2.append(dupla[1])
        #print(f"Lista de frecuencias calculada:\n{temp}\n")

        #freq_min = np.min(temp)
        adp_min = np.min(temp_2)
        print(f"Adaptabilidad {adp_min}\n")
        bw = temp[len(adaptabilidad)-1]-temp[0]
        print(f"BW valor de: {bw}Mz\n")
        freq_min = temp[temp_2.index(adp_min)]
        print(f"Valor frecuencia mejor adaptada: (f) {freq_min}  || (db) {adp_min}\n")
        
        coeficiente = (((80-bw)/40)**2)
        
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
    bw = 0
    for area in areas_f:
        temp = area[len(area)-1] - area[0]
        print(f">{temp}")
        if bw <= temp:
            bw = temp
    print(f"el ancho de banda es {bw}")    

    return coeficiente


# -> Futuro modulo de optimización
commands.init_system(exe,save,pname,dname,vname,u,ma,mi,nom,i,p,desc)
simulate.run_simulation_hfss(args="-runscript")