import numpy as np
import matplotlib.pyplot as plt
import os

from PSO_core.commands import read_data,Y_N_question, wait_to_read, update_data



def size_of_step(init_freq, final_freq, num_steps):
    return ((final_freq-init_freq)/(num_steps-1))

def draw_one_report(path="", report_n = "", data = [], points = 0, units = ""):
    if points <= 0: 
        points = read_data()['values']['reports']["aditional_data"]["points"]
    if units == "":
        units = read_data()['values']['reports']["aditional_data"]["units"]
    
    # requiered_reports = read_data()['values']['reports']

    if "GAIN" in report_n.upper() or "GANANCIA" in report_n.upper():
        if points >= 100:
            steps = 10
        elif points < 100 and points >= 50:
            steps = 5
        elif points < 50 and points >= 20:
            steps = 2
        else:
            steps = 1

        x=np.arange(1,points,steps)
        #y=np.arange(1,6,1)
        #colours=['b','g','b','k','y','r']
        figure=plt.figure(figsize=(8,6))
        for k in x:
            plt.plot(data[:,0],data[:,k]) #,label = str(k+(requiered_reports["aditional_data"]["fmin"]-1)) +requiered_reports["aditional_data"]["units"]
            # plt.legend(loc = 1,prop={'size': 12}) # Configuración del texto si se ponen labels
            plt.ylabel(r'Gain (lineal)',fontsize=18)
            plt.xlabel(r'$\theta$ (deg)',fontsize=18)
            plt.title(r'optimized (Plane $\phi$='+report_n.replace("GAINPhi","")+")",fontsize=18)
            plt.tick_params(axis='both', which='major', labelsize=18)
            plt.grid(True)
            plt.grid(color = '0.5', linestyle = '--', linewidth = 2)
        plt.savefig(path)
        plt.close(figure)

    elif "Z" in report_n.upper():
        x_name = "Frequency (" + units+")"
        figure=plt.figure(figsize=(8,6))
        plt.plot(data[:,0],data[:,1], label = "Re")
        plt.plot(data[:,0],data[:,2], label = "Im")
        plt.ylabel("Y",fontsize=18)
        plt.xlabel(x_name,fontsize=18)
        plt.tick_params(axis='both', which='major', labelsize=18)
        plt.grid(True)
        plt.grid(color = '0.5', linestyle = '--', linewidth = 2)
        plt.legend(loc = 1,prop={'size': 12})
        plt.title(report_n)
        plt.savefig(path)
        plt.close(figure)
    else:
        x_name = "Frequency (" + units+")"
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
            figure=plt.figure(figsize=(8,6))
            plt.plot(data[:,0],data[:,1])
            plt.ylabel(y_name,fontsize=18)
            plt.xlabel(x_name,fontsize=18)
            plt.tick_params(axis='both', which='major', labelsize=18)
            plt.grid(True)
            plt.grid(color = '0.5', linestyle = '--', linewidth = 2)
            plt.savefig(path)
            plt.close(figure)

def draw_all_iteration():
    reports_exist = False
    while not reports_exist:
        id_for_read = input("Digite el ID de la simulación previamente ejecutada: ")
        if not os.path.isdir(read_data()['paths']['results']+id_for_read):
            msj = "Error, ID no valido o existente!!\n¿Desea digitar otro ID?"
            if Y_N_question(msj) == "N":
                break
        else:
            reports_exist = True

    if reports_exist:
        update_data("info","ID", id_for_read)
        update_data("paths","files",read_data()['paths']['results']+id_for_read+"/files/")
        update_data("paths","figures", read_data()['paths']['results']+id_for_read+"/figures/")

        iteration = -1
        while iteration < 0 or iteration > read_data()["values"]["iterations"]:
            try:
                iteration = int(input("Digite el número de iteración: "))

                if iteration < 0:
                    wait_to_read("Valor no válido, el número debe ser un valor entero positivo")
                elif iteration > read_data()["values"]["iterations"]:
                    wait_to_read("Valor no válido, el número debe ser menor o igual a la cantidad de iteraciones declaradas en el archivo de configuración")
                else:
                    allFiles = os.listdir(read_data()['paths']['files'])
                    specific_path =  read_data()['paths']['figures']
                    units = input("Digite las unidades de la frecuencia (ej: KHz, MHz, GHz): ")
                    for file in allFiles:
                        if f"_{iteration}_" in file:
                            complement = file.replace("datos","").replace(".csv","").replace("GananciaPhi","GAINPHI").replace("amp_imb","AMPIMB").replace("pha_imb","PHASEIMB").split(f"_{iteration}_")
                            data = np.genfromtxt(read_data()['paths']['files']+file,skip_header = 1, delimiter = ',')
                            temp_path = specific_path + complement[0] +"_"+ str(iteration) +"_"+ complement[1]
                            points = len(data)
                            if "GAINPHI" in complement[0]:
                                points = len(data[0])-1
                            # print(f"report: {complement[0]} points:{points}")
                            draw_one_report(temp_path, complement[0], data, points, units)
            except:
                print("Algo salió mal, verifique que el dato ingresado es un número entero")

def draw_all_optimization():
    pass
def draw_a_comparison():
    pass