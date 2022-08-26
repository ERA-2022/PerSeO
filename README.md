# PSO_for_hybrids_and_antennas
## **Geometry Optimization**

This package is intended to provide a tool that supports the optimization process of different components as cavities or antennas, which electromagnetic performance is highly dependant on geometry. 

We apply optimization algorithms supported on HDFS simulations which provides a reliable tool to evaluate how every alternative geometry bahaves and to collect data derived from every optimization batch.

## **What's included**
1. ### **Version: v0.1**
-   Import and use
-   PSO optimization algorithm
-   Log file: Here you can find complete tracking of the optimizatio process
-   Data collection in CSV files
-   Passing configuration data through json files or from the code.
-   Simulation control by ID
-   Include two example for use the PSO in Hibryds and Antennas

2. ### **Requirements**
    _Things you need to set prior executing the script._
*   [Requirements file](requirements.txt) - Make sure to install all requirements from requirements.txt file
*   [Design_name.py]() or [Design_name.aedt]() - Add to the models folder located in the root folder a file contains the geometric model for HFSS (Python file), in case that the model will be a .aedt file, add this file to Ansoft folder located in Documents folder (default folder that create HFSS). The name of the .py file or .aedt file  must be equal of the project name.

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
    * Units
    * Maximum values that can vary the optimizator
    * Minimum values that can vary the optimizator
    * Nominals or default values of design
    * Number of iteratios
    * Number of particles
    * Number of branches  --> Posiblemente se elimine
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

After verifying all requirements and save you main script, you can run that scrip and interact with the interfaz of optimizer, where you will be acces for the next options:

* __Optimaze__
* __Eval the fitness function__
* __run script__
* __Graphics tools__
* __Set up__