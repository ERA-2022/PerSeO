import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os

from PSO_core.commands import read_data,Y_N_question, wait_to_read, update_data, make_directory,clear_screen

def size_of_step(init_freq, final_freq, num_steps):
    return ((final_freq-init_freq)/(num_steps-1))

def get_data_for_one_report():
    temp_path = os.getcwd().replace('\\','/')+'/results/'

    valid = False
    while not valid:    # Verificación de ID
        id_for_read = input("Digite el ID de la simulación previamente ejecutada: ")
        if not os.path.isdir(temp_path+id_for_read):
            msj = "Error, ID no valido o existente!!\n¿Desea digitar otro ID?"
            if Y_N_question(msj) == "N":
                break
        else:
            valid = True
    
    if valid:   # Verificación de archivo
        valid = False
        while not valid:
            file_path = temp_path + id_for_read +'/'
            file_name = input("Digite el nombre del archivo: ")
            if not ".csv" in file_name:
                file_name += ".csv"

            file_path += "files/" + file_name
            print(file_path)
            if not os.path.isfile(file_path):
                msj = "Error, el archivo no existe!!\n¿Desea intentarlo de nuevo?"
                if Y_N_question(msj) == "N":
                    break
            else:
                valid = True
    
    if valid:
        complement = file_name.replace("datos","").replace(".csv","").replace("GananciaPhi","GAINPHI").replace("amp_imb","AMPIMB").replace("pha_imb","PHASEIMB").split("_")
        data = np.genfromtxt(file_path, skip_header = 1, delimiter = ',')
        fig_path = temp_path+ id_for_read+"/figures/" + complement[0] +"_"+ complement[1] +"_"+ complement[2]
        points = len(data)
        units = input("Digite las unidades (ej: Hz, MHz): ")
        if "GAINPHI" in complement[0]:
            points = len(data[0])-1
        print(fig_path)
        # print(f"report: {complement[0]} iteration: {complement[1]} particle: {complement[2]} points:{points}")
        draw_one_report(fig_path, complement[0], data, points, units)

def draw_one_report(path="", report_n = "", data = [], points = 0, units = ""):
    matplotlib.use("Agg")
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

        allFiles = os.listdir(read_data()['paths']['files'])
        specific_path =  read_data()['paths']['figures']
        units = input("Digite las unidades de la frecuencia (ej: KHz, MHz, GHz): ")
        cont = 0
        for file in allFiles:
            complement = file.replace("datos","").replace(".csv","").replace("GananciaPhi","GAINPHI").replace("amp_imb","AMPIMB").replace("pha_imb","PHASEIMB").split("_")
            data = np.genfromtxt(read_data()['paths']['files']+file,skip_header = 1, delimiter = ',')
            temp_path = specific_path + complement[0] +"_"+ str(complement[1]) +"_"+ complement[2]
            points = len(data)
            
            if "GAINPHI" in complement[0]:
                points = len(data[0])-1
            print(f"report: {complement[0]} points:{points} file:{file} data[0]:{data[0]}")
            cont+=1
            draw_one_report(temp_path, complement[0], data, points, units)

        print(f"Archivos leidos:{cont}")

def draw_a_comparison():
    Valid = False   # Verificación del archivo 1
    while not Valid:
        filePath1 = input("Digite la ruta del archivo 1: ")
        if os.path.isfile(filePath1):
            if ".csv" in filePath1:
                Valid = True
            else:
                msj = "Error, formato de archivo no válido! Asegurese que el tipo de archivo que intenta acceder tiene la extensión '.csv'\n¿Desea intentarlo de nuevo?"
                if Y_N_question(msj) == "N":
                    break
        else:
            msj = "Error, ruta invalida o inexistente!!\n¿Desea digitar otra?"
            if Y_N_question(msj) == "N":
                break
        
    if Valid:   # Verificación del archivo 2
        Valid = False
        while not Valid:
            filePath2 = input("Digite la ruta del archivo 2: ")
            if os.path.isfile(filePath2):
                if ".csv" in filePath2:
                    Valid = True
                else:
                    msj = "Error, formato de archivo no válido! Asegurese que el tipo de archivo que intenta acceder tiene la extensión '.csv'\n¿Desea intentarlo de nuevo?"
                    if Y_N_question(msj) == "N":
                        break
            else:
                msj = "Error, ruta invalida o inexistente!!\n¿Desea digitar otra?"
                if Y_N_question(msj) == "N":
                    break
    
    if Valid:   # Selección y verificación de la ruta de guardado
        Valid = False
        while not Valid:
            print("Nota, si presiona enter sin agregar ninguna ruta, esta será guardada en ../results/comparison graphics/")
            savePath = input("Digite la ruta donde será guardada la grafica resultante: ")
            
            if savePath == "":
                savePath = os.getcwd().replace('\\','/')+'/'
                make_directory('results', savePath)
                savePath += "results/"
                make_directory(savePath+'comparison graphics', "/")
                savePath += "comparison graphics/"

            if os.path.isdir(savePath):
                Valid = True
            else:
                msj = "Error, ruta invalida o inexistente!!\n¿Desea digitar otra?"
                if Y_N_question(msj) == "N":
                    break
        
    if Valid:   # Graficación
        x_name = input("Digite la leyenda del eje X: ")
        y_name = input("Digite la leyenda del eje y: ")
        graphicTitle = input("Digite el titulo de la gráfica: ")
        label1 = input("Digite la leyenda de los datos del archivo 1: ")
        label2 = input("Digite la leyenda de los datos del archivo 2: ")

        data1 = np.genfromtxt(filePath1,skip_header = 1, delimiter = ',')
        data2 = np.genfromtxt(filePath2,skip_header = 1, delimiter = ',')
        figure=plt.figure(figsize=(8,6))
        plt.plot(data1[:,0],data1[:,1], label = label1)
        plt.plot(data2[:,0],data2[:,1], label = label2)
        plt.ylabel(y_name,fontsize=18)
        plt.xlabel(x_name,fontsize=18)
        plt.tick_params(axis='both', which='major', labelsize=18)
        plt.grid(True)
        plt.grid(color = '0.5', linestyle = '--', linewidth = 2)
        plt.legend(loc = 1,prop={'size': 12})
        plt.title(graphicTitle)
        plt.savefig(savePath+graphicTitle)
        plt.close(figure)
    