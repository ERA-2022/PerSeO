# PSO_for_hybrids_and_antennas
## **Geometry Optimization**

This package is intended to provide a tool that supports the optimization process of different components as hybrids or antennas, which electromagnetic performance is highly dependant on geometry. 

We apply optimization algorithms supported on HFSS simulations which provides a reliable tool to evaluate how every alternative geometry bahaves and to collect data derived from every optimization batch.

## **What's included**
1. ### **Version: v0.9**
-   Import and use
-   PSO optimization algorithm
-   Log file: Here you can find complete tracking of the optimization process
-   Data collection in CSV files
-   Passing configuration data through json files or from the code.
-   Simulation control by ID
-   Include two example for use the PSO in Hibryds and Antennas

2. ### **Requirements**
    _Things you need to set prior executing the script._
*   [Requirements file](requirements.txt) - Make sure to install all requirements from requirements.txt file
*   *Design_name.py* or *Design_name.aedt* - Add to the models folder located in the root folder a file contains the geometric model for HFSS (Python file), in case that the model will be a .aedt file, add this file to Ansoft folder located in Documents folder (default folder that create HFSS). The name of the .py file or .aedt file  must be equal of the project name.

*   __First step:__ You have to make sure to add the following imports to your main script.
    ```
    from PSO_core import commands
    from PSO_functions import Interfaz
    ```
*   __Second step:__ You have to define the following parameters for the optimizator, is recomended save this data in independents variables:
    * Path to executable of ANSYS
    * Path to default save of ANSYS
    * Category of structure (Antenna, Hybrid, Filter, among others)
    * Sub category of structure
    * Project name
    * Design name
    * Variable name or name of name the array where are the dimensions
    * Units (about of distance)
    * Maximum values that can vary the optimizator
    * Minimum values that can vary the optimizator
    * Nominals or default values of design
    * Number of iteratios
    * Number of particles
    <!-- * Number of branches  Posiblemente se elimine -->
    * Description about of simulation and relevant information
    * Reports what do you need for the fitness function
    
    This informatión will be use as parameters for initialize the optimizator with a method that later view.
    Follow the next example:
    ```
    exe = "C:/Program Files/AnsysEM/AnsysEM19.0/Win64/ansysedt.exe"
    save = "C:/Users/Astrolab/Documents/Ansoft/"
    category = "Antenna"
    sub_category = "Dipole blade"
    pname = "DIPOLE_BLADE_ANTENNA"
    dname = "DESIGN"
    vname = "variables"
    u = "mm"
    ma = [12650, 1300, 1600, 65, 20, 2.5, 1700]
    mi = [8200, 750, 950, 30, 20, 2.5, 750]
    nom = [8333.33, 813.33, 1043.33, 36.66, 20, 2.5, 866.66]
    i = 2
    p = 2
    b = 0
    desc = "100%BW with ideal BW to 80MHz, denominator (or cut-off frecuency) in 40MHz working in the frecuency band of 40MHz to 120MHz"

    reports = {
        "SMN":[(1,1)],
        "gain":[0,90],
        "vswr":[1],
        "zmn":[(1,1)],
        "aditional_data":{
            "fmin":40,
            "points":81,
            "units":"MHz"
        }
    }
    ```    

*   __Third step:__, you need define your fitness function, this must recive one parameter (the data of requiered reports as a dictionary) and must return the value of the fitness function as show to continue in the follow example.
    ```
    def fit (dataReports):
        for key in dataReports:
            print(str(key)+"--->"+str(len(dataReports[key])))

        areas_f = []
        areas_d = []
        new_area = True
        for data in dataReports['S11']:
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
                
            else:
                coeficiente = 20      
        
        print(f"Valor función de merito: {coeficiente}")
        print("---------------------------------------------------\n\n")
        return coeficiente
    ```

    In the same way that the before point, this function will use later.

*   __Fourth step:__ You must initialize the system with init_system(...), this method come on from commands of the first importation and you must add the arguments  definded in the second step.

    the order of arguments in the init_system method is:

    | Position |  argument name | data type |
    |:--------:|:--------------:|:---------:|
    |     1    |    ansys_exe   |    str    |
    |     2    | ansys_save_def |    str    |
    |     3    |  project_name  |    str    |
    |     4    |   design_name  |    str    |
    |     5    |  variable_name |    str    |
    |     6    |      units     |    str    |
    |     7    |       max      |    lst    |
    |     8    |       min      |    lst    |
    |     9    |     nomilas    |    lst    |
    |    10    |   iterations   |    int    |
    |    11    |    particles   |    int    |
    |    12    |    branches    |    int    |
    |    13    |     reports    |    dict   |
    |    14    |    category    |    str    |
    |    15    |  sub_category  |    str    |
    |    16    |   description  |    str    |

    As you see in the next example (using the data before defined):
    ```
    commands.init_system(exe, save, pname, dname,vname, u, ma, mi, nom, i, p, b, reports, category, sub_category, desc)
    ```

* __Fifth step:__ You must use the main_menu(...), this method come on from Interfaz of the second importation and you must add the fitness function as argumet of main_menu(...) as show in the next example:

    ```
    Interfaz.main_menu(fit)
    ```

## **How to use**

After verifying all requirements and save you main script, you can run that script in cmd as shown as below.

```
C:\Users\Astrolab\Documents\Jaime\Temporal>python3 Example_1.py
```
Other form to run your code is using some IDLE as VSCode, Spider, Conda, among others.

For interact with the interfaz of optimizer, you will be acces for the next options:

```
-------->PSO APP<---------
-----\Menú
1> Optimizate
2> Fitness function test
3> Graphics tools
4> Salir
Digite una opción del menú:
```

### Optimizate
Firstly, this option verify that the model exist using the ansys file or python file, in case of the software can't run the files, it will auto run trying to run successful repeatly, if this not result, the software will notify you of error and back to main menu.

once verified that the model exists, the software will ask if you want graphic the reports, for this write 's' or 'n' in the console and press intro, the optimization will start the process creating particles (new dimensions), followed of the simulation in ANSYS of this designs exporting the reports that you need and drawing the graphics (in ../ID/figures/) if is the case for later read and calculate again the fitness function value, dimensions and new particles.This process will repeat for all iterations and particles until end.

All data (for iteration) will save in the output.csv file in ../results/output.csv, here you will find the majority of informatión about the simulatión previously run as your ID, time to start and end, type, category, sub category, parameters of simulation, simulations result, best particles (globals and locals) beside the number of current iteration in this moment among others.
### Fitness function test
This option allows to execute a new simulation based on previous results, for this it is necessary to have the previous ID of one simulation, the diferents  reports  files (.csv) , and to have loaded the same parameters of the previous simulation. As the option 1 (Optimizate) you could choose if draw the graphics or not.

This optios is think to make fast test with diferents fitness functions since skip the simulation step wich use more time in all simulation process. but for this reason also you must understand that the optimizator show new dimensions it have not simulated.

All data (for iteration) will save in the output.csv file in ../results/output.csv, here you will find the majority of informatión about the simulatión previously run as your ID, time to start and end, type, category, sub category, parameters of simulation, simulations result, best particles (globals and locals) beside the number of current iteration in this moment among others.
### Graphics tools
This option has a menu that allows draw graphics of reports simulated as follow show
```
-----\Graphics tools
1> Graficar un reporte
2> Graficar una iteración completa
3> Graficar una ejecución completa
4> Graficar una comparación de reportes
5> Salir
Digite una opción del menú:
```
#### Graficar un reporte
Firstly, this option will request a previously simulated ID. Later the file name to draw (you could write the '.csv' extensión or not) . Next, you will need define the label of *x* axis, this is associate to magnitude in frequency (not apply to the gain phi graphics) and the process will finish with a message notify that the process end.
```
-----\Graphics tools
1> Graficar un reporte
2> Graficar una iteración completa
3> Graficar una ejecución completa
4> Graficar una comparación de reportes
5> Salir
Digite una opción del menú: 1
Digite el ID de la simulación previamente ejecutada: f86eb80d-3dd1-403d-a5ad-824081d8835b
Digite el nombre del archivo: datosVSWR(1)_0_0.csv
Digite las unidades (ej: Hz, MHz): MHz

El proceso ha terminado, verifique la grafica en la carpeta 'figures' en la carpeta con el ID digitado
Presione enter para continuar...
```
The graphics drawed will save in the figures folder between the ID folder previously request.
#### Graficar una iteración completa
As in the previously option, this will request a previously simulated ID followed by the number of iteration to draw and the label of *x* axis (not apply to the gain phi graphics).  Next, while the software  draw the graphics, in the screen will show the name of drawed files and the process will finish with a notification in the screen.

```
-----\Graphics tools
1> Graficar un reporte
2> Graficar una iteración completa     
3> Graficar una ejecución completa     
4> Graficar una comparación de reportes
5> Salir
Digite una opción del menú: 2
Digite el ID de la simulación previamente ejecutada: f86eb80d-3dd1-403d-a5ad-824081d8835b
Digite el número de iteración: 1
Digite las unidades de la frecuencia (ej: KHz, MHz, GHz): MHz
Graficando ---> datosGananciaPhi0_1_0.csv
Graficando ---> datosGananciaPhi0_1_1.csv
Graficando ---> datosGananciaPhi90_1_0.csv
Graficando ---> datosGananciaPhi90_1_1.csv
Graficando ---> datosS11_1_0.csv
Graficando ---> datosS11_1_1.csv
Graficando ---> datosVSWR(1)_1_0.csv
Graficando ---> datosVSWR(1)_1_1.csv
Graficando ---> datosZ11_1_0.csv
Graficando ---> datosZ11_1_1.csv

El proceso ha terminado, verifique las graficas en la carpeta figures en la carpeta con el ID digitado
Presione enter para continuar...
```
The graphics drawed will save in the figures folder between the ID folder previously request.
#### Graficar una ejecución completa
As in the previously option, this will request a previously simulated ID and the label of *x* axis (not apply to the gain phi graphics).  Next, while the software  draw the graphics, in the screen will show the name of drawed files and the process will finish with a count of files read and draw followed by a notification in the screen that it finished.
```
-----\Graphics tools
1> Graficar un reporte
2> Graficar una iteración completa
3> Graficar una ejecución completa
4> Graficar una comparación de reportes
5> Salir
Digite una opción del menú: 3
Digite el ID de la simulación previamente ejecutada: f86eb80d-3dd1-403d-a5ad-824081d8835b
Digite las unidades de la frecuencia (ej: KHz, MHz, GHz): MHz
Graficando ---> datosGananciaPhi0_0_0.csv
Graficando ---> datosGananciaPhi0_0_1.csv
Graficando ---> datosGananciaPhi0_1_0.csv
Graficando ---> datosGananciaPhi0_1_1.csv
Graficando ---> datosGananciaPhi90_0_0.csv
Graficando ---> datosGananciaPhi90_0_1.csv
Graficando ---> datosGananciaPhi90_1_0.csv
Graficando ---> datosGananciaPhi90_1_1.csv
Graficando ---> datosS11_0_0.csv
Graficando ---> datosS11_0_1.csv
Graficando ---> datosS11_1_0.csv
Graficando ---> datosS11_1_1.csv
Graficando ---> datosVSWR(1)_0_0.csv
Graficando ---> datosVSWR(1)_0_1.csv
Graficando ---> datosVSWR(1)_1_0.csv
Graficando ---> datosVSWR(1)_1_1.csv
Graficando ---> datosZ11_0_0.csv
Graficando ---> datosZ11_0_1.csv
Graficando ---> datosZ11_1_0.csv
Graficando ---> datosZ11_1_1.csv
Archivos leidos y graficados:10

El proceso ha terminado, verifique las graficas en la carpeta 'figures' en la carpeta con el ID digitado
Presione enter para continuar...
```
The graphics drawed will save in the figures folder between the ID folder previously request.
#### Graficar una comparación de reportes
For use this option is necessary that the two file have the same magnitude otherwise the graphic could see wrong.
Firstly, will be request the path (be suggest complete path not relative path) of first file. In the same way, will be request the path of second file. 
```
-----\Graphics tools
1> Graficar un reporte
2> Graficar una iteración completa     
3> Graficar una ejecución completa     
4> Graficar una comparación de reportes
5> Salir
Digite una opción del menú: 4
Digite la ruta del archivo 1: C:\Users\Astrolab\Documents\Jaime\Temporal\results\f86eb80d-3dd1-403d-a5ad-824081d8835b\files\datosS11_1_0.csv
Digite la ruta del archivo 2: C:\Users\Astrolab\Documents\Jaime\Temporal\results\ea33b78a-068e-4fa3-9149-c419164c3cfb\files\datosS11_0_1.csv
```
Next, will be request the save path, however, if you press Intro with this field empty, the save path will be ../results/comparison graphics/
* Example with specific save path
```
Nota, si presiona enter sin agregar ninguna ruta, esta será guardada en ../results/comparison graphics/
Digite la ruta donde será guardada la grafica resultante: C:\Users\Astrolab\Documents\Jaime\Comparaciones 
```
* Example with default save path
```
Nota, si presiona enter sin agregar ninguna ruta, esta será guardada en ../results/comparison graphics/
Digite la ruta donde será guardada la grafica resultante:
```
later, will be request the labels of *x* and *y* axis, the Title of the graphic,this will be the same of the save file name (this name cannot have dots) and the label  of each file tha will present in the graphic. when the process finish a message will notify it
```
Nota, si presiona enter sin agregar ninguna ruta, esta será guardada en ../results/comparison graphics/
Digite la ruta donde será guardada la grafica resultante: C:\Users\Astrolab\Documents\Jaime\Comparaciones                                       
Digite la leyenda del eje X: Frequency(MHz)
Digite la leyenda del eje y: dB 
Digite el titulo de la gráfica: S11 v1 vs v2
Digite la leyenda de los datos del archivo 1: v1 ID f86eb...
Digite la leyenda de los datos del archivo 2: v2 ID ea33b...

El proceso ha terminado, verifique la grafica en la carpeta 'Comparaciones'
Presione enter para continuar...
```
<!-- ### Set up -->
### Exit
This option is for end the script that is running

__*Developed by:*__ German Chaparro, Jorge Cardenas,Oscar Restrepo, Sergio Mora, Jhon Vera, and Jaime Angel

__*Year:*__ 2022
