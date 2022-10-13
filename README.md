# PSO_for_hybrids_and_antennas
## **Geometry Optimization**

This package is intended to provide a tool that supports the optimization process of different components as hybrids or antennas, which electromagnetic performance is highly dependant on geometry. 

We apply optimization algorithms supported on HFSS simulations which provides a reliable tool to evaluate how every alternative geometry bahaves and to collect data derived from every optimization batch.

## **What's included**
1. ### **Version: v0.91**
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
-----\MENU
1> Optimizate
2> Fitness function test
3> Graphics tools
4> Exit
Enter an option:
```

### Optimizate
Firstly, this option verify that the model exist using the ansys file or python file, in case of the software can't run the files, it will auto run trying to run successful repeatly, if this not result, the software will notify you of error and back to main menu.

once verified that the model exists, the software will ask if you want graphic the reports, for this write 'Y' or 'N' in the console and press intro, the optimization will start the process creating particles (new dimensions), followed of the simulation in ANSYS of this designs exporting the reports that you need and drawing the graphics (in ../ID/figures/) if is the case for later read and calculate again the fitness function value, dimensions and new particles.This process will repeat for all iterations and particles until end.

All data (for iteration) will save in the output.csv file in ../results/output.csv, here you will find the majority of informatión about the simulatión previously run as your ID, time to start and end, type, category, sub category, parameters of simulation, simulations result, best particles (globals and locals) beside the number of current iteration in this moment among others.
### Fitness function test
This option allows to execute a new simulation based on previous results, for this it is necessary to have the previous ID of one simulation, the diferents  reports  files (.csv) , and to have loaded the same parameters of the previous simulation. As the option 1 (Optimizate) you could choose if draw the graphics or not.

This optios is think to make fast test with diferents fitness functions since skip the simulation step wich use more time in all simulation process. but for this reason also you must understand that the optimizator show new dimensions it have not simulated.

All data (for iteration) will save in the output.csv file in ../results/output.csv, here you will find the majority of informatión about the simulatión previously run as your ID, time to start and end, type, category, sub category, parameters of simulation, simulations result, best particles (globals and locals) beside the number of current iteration in this moment among others.
### Graphics tools
This option has a menu that allows draw graphics of reports simulated as follow show
```
-----\Graphics tools
1> Draw one report
2> Draw one complete iterations
3> Draw one complete ejecution
4> Draw one reports comparitions
5> Back
Enter an option:
```
#### Draw one report
Firstly, this option will request a previously simulated ID. Later the file name to draw (you could write the '.csv' extensión or not) . Next, you will need define the label of *x* axis, this is associate to magnitude in frequency (not apply to the gain phi graphics) and the process will finish with a message notify that the process end.
```
-----\Graphics tools
1> Draw one report
2> Draw one complete iterations
3> Draw one complete ejecution
4> Draw one reports comparitions
5> Back
Enter an option: 1
Enter a previously simulate ID: 8b041a42-8bae-4df9-9f44-b909f84038c9
Enter the file name: amp_imb_0_0
Enter the magnitude of frequency (for example Hz, KHz, MHz, GHz, among others): GHz

The process has ended,  verify that the draw graphic is in 'figures' folder in the entered ID folder
Press intro to continue...
```
The graphics drawed will save in the figures folder between the ID folder previously request.
#### Draw one complete iterations
As in the previously option, this will request a previously simulated ID followed by the number of iteration to draw and the label of *x* axis (not apply to the gain phi graphics).  Next, while the software  draw the graphics, in the screen will show the name of drawed files and the process will finish with a notification in the screen.

```
-----\Graphics tools
1> Draw one report
2> Draw one complete iterations 
3> Draw one complete ejecution  
4> Draw one reports comparitions
5> Back
Enter an option: 2
Enter a previously simulate ID: 8b041a42-8bae-4df9-9f44-b909f84038c9
Enter the iteration number: 3
Enter the magnitude of frequency (for example Hz, KHz, MHz, GHz, among others): GHz
Drawing a graphic ---> amp_imb_3_0.csv
Drawing a graphic ---> amp_imb_3_1.csv
Drawing a graphic ---> amp_imb_3_2.csv
Drawing a graphic ---> amp_imb_3_3.csv
Drawing a graphic ---> amp_imb_3_4.csv
Drawing a graphic ---> datosS11_3_0.csv
Drawing a graphic ---> datosS11_3_1.csv
Drawing a graphic ---> datosS11_3_2.csv
Drawing a graphic ---> datosS11_3_3.csv
Drawing a graphic ---> datosS11_3_4.csv
Drawing a graphic ---> datosS21_3_0.csv
Drawing a graphic ---> datosS21_3_1.csv
Drawing a graphic ---> datosS21_3_2.csv
Drawing a graphic ---> datosS21_3_3.csv
Drawing a graphic ---> datosS21_3_4.csv
Drawing a graphic ---> datosS31_3_0.csv
Drawing a graphic ---> datosS31_3_1.csv
Drawing a graphic ---> datosS31_3_2.csv
Drawing a graphic ---> datosS31_3_3.csv
Drawing a graphic ---> datosS31_3_4.csv
Drawing a graphic ---> datosS41_3_0.csv
Drawing a graphic ---> datosS41_3_1.csv
Drawing a graphic ---> datosS41_3_2.csv
Drawing a graphic ---> datosS41_3_3.csv
Drawing a graphic ---> datosS41_3_4.csv
Drawing a graphic ---> datosS42_3_0.csv
Drawing a graphic ---> datosS42_3_1.csv
Drawing a graphic ---> datosS42_3_2.csv
Drawing a graphic ---> datosS42_3_3.csv
Drawing a graphic ---> datosS42_3_4.csv
Drawing a graphic ---> datosVSWR(1)_3_0.csv
Drawing a graphic ---> datosVSWR(1)_3_1.csv
Drawing a graphic ---> datosVSWR(1)_3_2.csv
Drawing a graphic ---> datosVSWR(1)_3_3.csv
Drawing a graphic ---> datosVSWR(1)_3_4.csv
Drawing a graphic ---> datosVSWR(2)_3_0.csv
Drawing a graphic ---> datosVSWR(2)_3_1.csv
Drawing a graphic ---> datosVSWR(2)_3_2.csv
Drawing a graphic ---> datosVSWR(2)_3_3.csv
Drawing a graphic ---> datosVSWR(2)_3_4.csv
Drawing a graphic ---> datosVSWR(3)_3_0.csv
Drawing a graphic ---> datosVSWR(3)_3_1.csv
Drawing a graphic ---> datosVSWR(3)_3_2.csv
Drawing a graphic ---> datosVSWR(3)_3_3.csv
Drawing a graphic ---> datosVSWR(3)_3_4.csv
Drawing a graphic ---> datosVSWR(4)_3_0.csv
Drawing a graphic ---> datosVSWR(4)_3_1.csv
Drawing a graphic ---> datosVSWR(4)_3_2.csv
Drawing a graphic ---> datosVSWR(4)_3_3.csv
Drawing a graphic ---> datosVSWR(4)_3_4.csv
Drawing a graphic ---> datosZ11_3_0.csv
Drawing a graphic ---> datosZ11_3_1.csv
Drawing a graphic ---> datosZ11_3_2.csv
Drawing a graphic ---> datosZ11_3_3.csv
Drawing a graphic ---> datosZ11_3_4.csv
Drawing a graphic ---> datosZ21_3_0.csv
Drawing a graphic ---> datosZ21_3_1.csv
Drawing a graphic ---> datosZ21_3_2.csv
Drawing a graphic ---> datosZ21_3_3.csv
Drawing a graphic ---> datosZ21_3_4.csv
Drawing a graphic ---> datosZ31_3_0.csv
Drawing a graphic ---> datosZ31_3_1.csv
Drawing a graphic ---> datosZ31_3_2.csv
Drawing a graphic ---> datosZ31_3_3.csv
Drawing a graphic ---> datosZ31_3_4.csv
Drawing a graphic ---> datosZ41_3_0.csv
Drawing a graphic ---> datosZ41_3_1.csv
Drawing a graphic ---> datosZ41_3_2.csv
Drawing a graphic ---> datosZ41_3_3.csv
Drawing a graphic ---> datosZ41_3_4.csv
Drawing a graphic ---> datosZ42_3_0.csv
Drawing a graphic ---> datosZ42_3_1.csv
Drawing a graphic ---> datosZ42_3_2.csv
Drawing a graphic ---> datosZ42_3_3.csv
Drawing a graphic ---> datosZ42_3_4.csv
Drawing a graphic ---> pha_imb_3_0.csv
Drawing a graphic ---> pha_imb_3_1.csv
Drawing a graphic ---> pha_imb_3_2.csv
Drawing a graphic ---> pha_imb_3_3.csv
Drawing a graphic ---> pha_imb_3_4.csv

The process has ended,  verify that the draw graphic is in 'figures' folder in the entered ID folder
Press intro to continue...
```
The graphics drawed will save in the figures folder between the ID folder previously request.
#### Draw one complete ejecution
As in the previously option, this will request a previously simulated ID and the label of *x* axis (not apply to the gain phi graphics).  Next, while the software  draw the graphics, in the screen will show the name of drawed files and the process will finish with a count of files read and draw followed by a notification in the screen that it finished.
```
-----\Graphics tools
1> Draw one report
2> Draw one complete iterations
3> Draw one complete ejecution
4> Draw one reports comparitions
5> Back
Enter an option: 3
Enter a previously simulate ID: 8b041a42-8bae-4df9-9f44-b909f84038c9
Enter the magnitude of frequency (for example Hz, KHz, MHz, GHz, among others): GHz
Drawing a graphic ---> amp_imb_0_0.csv
Drawing a graphic ---> amp_imb_0_1.csv
Drawing a graphic ---> amp_imb_0_2.csv
Drawing a graphic ---> amp_imb_0_3.csv
Drawing a graphic ---> amp_imb_0_4.csv
Drawing a graphic ---> amp_imb_1_0.csv
Drawing a graphic ---> amp_imb_1_1.csv
Drawing a graphic ---> amp_imb_1_2.csv
Drawing a graphic ---> amp_imb_1_3.csv
Drawing a graphic ---> amp_imb_1_4.csv
Drawing a graphic ---> amp_imb_2_0.csv
Drawing a graphic ---> amp_imb_2_1.csv
Drawing a graphic ---> amp_imb_2_2.csv
Drawing a graphic ---> amp_imb_2_3.csv
Drawing a graphic ---> amp_imb_2_4.csv
Drawing a graphic ---> amp_imb_3_0.csv
Drawing a graphic ---> amp_imb_3_1.csv
Drawing a graphic ---> amp_imb_3_2.csv
Drawing a graphic ---> amp_imb_3_3.csv
Drawing a graphic ---> amp_imb_3_4.csv
Drawing a graphic ---> amp_imb_4_0.csv
Drawing a graphic ---> amp_imb_4_1.csv
Drawing a graphic ---> amp_imb_4_2.csv
Drawing a graphic ---> amp_imb_4_3.csv
Drawing a graphic ---> amp_imb_4_4.csv
Drawing a graphic ---> amp_imb_5_0.csv
Drawing a graphic ---> amp_imb_5_1.csv
Drawing a graphic ---> amp_imb_5_2.csv
Drawing a graphic ---> amp_imb_5_3.csv
Drawing a graphic ---> amp_imb_5_4.csv
Drawing a graphic ---> datosS11_0_0.csv
Drawing a graphic ---> datosS11_0_1.csv
Drawing a graphic ---> datosS11_0_2.csv
Drawing a graphic ---> datosS11_0_3.csv
Drawing a graphic ---> datosS11_0_4.csv
Drawing a graphic ---> datosS11_1_0.csv
Drawing a graphic ---> datosS11_1_1.csv
Drawing a graphic ---> datosS11_1_2.csv
Drawing a graphic ---> datosS11_1_3.csv
Drawing a graphic ---> datosS11_1_4.csv
Drawing a graphic ---> datosS11_2_0.csv
Drawing a graphic ---> datosS11_2_1.csv
Drawing a graphic ---> datosS11_2_2.csv
Drawing a graphic ---> datosS11_2_3.csv
Drawing a graphic ---> datosS11_2_4.csv
Drawing a graphic ---> datosS11_3_0.csv
Drawing a graphic ---> datosS11_3_1.csv
Drawing a graphic ---> datosS11_3_2.csv
Drawing a graphic ---> datosS11_3_3.csv
Drawing a graphic ---> datosS11_3_4.csv
Drawing a graphic ---> datosS11_4_0.csv
Drawing a graphic ---> datosS11_4_1.csv
Drawing a graphic ---> datosS11_4_2.csv
Drawing a graphic ---> datosS11_4_3.csv
Drawing a graphic ---> datosS11_4_4.csv
Drawing a graphic ---> datosS11_5_0.csv
Drawing a graphic ---> datosS11_5_1.csv
Drawing a graphic ---> datosS11_5_2.csv
Drawing a graphic ---> datosS11_5_3.csv
Drawing a graphic ---> datosS11_5_4.csv
Drawing a graphic ---> datosS21_0_0.csv
Drawing a graphic ---> datosS21_0_1.csv
Drawing a graphic ---> datosS21_0_2.csv
Drawing a graphic ---> datosS21_0_3.csv
Drawing a graphic ---> datosS21_0_4.csv
Drawing a graphic ---> datosS21_1_0.csv
Drawing a graphic ---> datosS21_1_1.csv
Drawing a graphic ---> datosS21_1_2.csv
Drawing a graphic ---> datosS21_1_3.csv
Drawing a graphic ---> datosS21_1_4.csv
Drawing a graphic ---> datosS21_2_0.csv
Drawing a graphic ---> datosS21_2_1.csv
Drawing a graphic ---> datosS21_2_2.csv
Drawing a graphic ---> datosS21_2_3.csv
Drawing a graphic ---> datosS21_2_4.csv
Drawing a graphic ---> datosS21_3_0.csv
Drawing a graphic ---> datosS21_3_1.csv
Drawing a graphic ---> datosS21_3_2.csv
Drawing a graphic ---> datosS21_3_3.csv
Drawing a graphic ---> datosS21_3_4.csv
Drawing a graphic ---> datosS21_4_0.csv
Drawing a graphic ---> datosS21_4_1.csv
Drawing a graphic ---> datosS21_4_2.csv
Drawing a graphic ---> datosS21_4_3.csv
Drawing a graphic ---> datosS21_4_4.csv
Drawing a graphic ---> datosS21_5_0.csv
Drawing a graphic ---> datosS21_5_1.csv
Drawing a graphic ---> datosS21_5_2.csv
Drawing a graphic ---> datosS21_5_3.csv
Drawing a graphic ---> datosS21_5_4.csv
Drawing a graphic ---> datosS31_0_0.csv
Drawing a graphic ---> datosS31_0_1.csv
Drawing a graphic ---> datosS31_0_2.csv
Drawing a graphic ---> datosS31_0_3.csv
Drawing a graphic ---> datosS31_0_4.csv
Drawing a graphic ---> datosS31_1_0.csv
Drawing a graphic ---> datosS31_1_1.csv
Drawing a graphic ---> datosS31_1_2.csv
Drawing a graphic ---> datosS31_1_3.csv
Drawing a graphic ---> datosS31_1_4.csv
Drawing a graphic ---> datosS31_2_0.csv
Drawing a graphic ---> datosS31_2_1.csv
Drawing a graphic ---> datosS31_2_2.csv
Drawing a graphic ---> datosS31_2_3.csv
Drawing a graphic ---> datosS31_2_4.csv
Drawing a graphic ---> datosS31_3_0.csv
Drawing a graphic ---> datosS31_3_1.csv
Drawing a graphic ---> datosS31_3_2.csv
Drawing a graphic ---> datosS31_3_3.csv
Drawing a graphic ---> datosS31_3_4.csv
Drawing a graphic ---> datosS31_4_0.csv
Drawing a graphic ---> datosS31_4_1.csv
Drawing a graphic ---> datosS31_4_2.csv
Drawing a graphic ---> datosS31_4_3.csv
Drawing a graphic ---> datosS31_4_4.csv
Drawing a graphic ---> datosS31_5_0.csv
Drawing a graphic ---> datosS31_5_1.csv
Drawing a graphic ---> datosS31_5_2.csv
Drawing a graphic ---> datosS31_5_3.csv
Drawing a graphic ---> datosS31_5_4.csv
Drawing a graphic ---> datosS41_0_0.csv
Drawing a graphic ---> datosS41_0_1.csv
Drawing a graphic ---> datosS41_0_2.csv
Drawing a graphic ---> datosS41_0_3.csv
Drawing a graphic ---> datosS41_0_4.csv
Drawing a graphic ---> datosS41_1_0.csv
Drawing a graphic ---> datosS41_1_1.csv
Drawing a graphic ---> datosS41_1_2.csv
Drawing a graphic ---> datosS41_1_3.csv
Drawing a graphic ---> datosS41_1_4.csv
Drawing a graphic ---> datosS41_2_0.csv
Drawing a graphic ---> datosS41_2_1.csv
Drawing a graphic ---> datosS41_2_2.csv
Drawing a graphic ---> datosS41_2_3.csv
Drawing a graphic ---> datosS41_2_4.csv
Drawing a graphic ---> datosS41_3_0.csv
Drawing a graphic ---> datosS41_3_1.csv
Drawing a graphic ---> datosS41_3_2.csv
Drawing a graphic ---> datosS41_3_3.csv
Drawing a graphic ---> datosS41_3_4.csv
Drawing a graphic ---> datosS41_4_0.csv
Drawing a graphic ---> datosS41_4_1.csv
Drawing a graphic ---> datosS41_4_2.csv
Drawing a graphic ---> datosS41_4_3.csv
Drawing a graphic ---> datosS41_4_4.csv
Drawing a graphic ---> datosS41_5_0.csv
Drawing a graphic ---> datosS41_5_1.csv
Drawing a graphic ---> datosS41_5_2.csv
Drawing a graphic ---> datosS41_5_3.csv
Drawing a graphic ---> datosS41_5_4.csv
Drawing a graphic ---> datosS42_0_0.csv
Drawing a graphic ---> datosS42_0_1.csv
Drawing a graphic ---> datosS42_0_2.csv
Drawing a graphic ---> datosS42_0_3.csv
Drawing a graphic ---> datosS42_0_4.csv
Drawing a graphic ---> datosS42_1_0.csv
Drawing a graphic ---> datosS42_1_1.csv
Drawing a graphic ---> datosS42_1_2.csv
Drawing a graphic ---> datosS42_1_3.csv
Drawing a graphic ---> datosS42_1_4.csv
Drawing a graphic ---> datosS42_2_0.csv
Drawing a graphic ---> datosS42_2_1.csv
Drawing a graphic ---> datosS42_2_2.csv
Drawing a graphic ---> datosS42_2_3.csv
Drawing a graphic ---> datosS42_2_4.csv
Drawing a graphic ---> datosS42_3_0.csv
Drawing a graphic ---> datosS42_3_1.csv
Drawing a graphic ---> datosS42_3_2.csv
Drawing a graphic ---> datosS42_3_3.csv
Drawing a graphic ---> datosS42_3_4.csv
Drawing a graphic ---> datosS42_4_0.csv
Drawing a graphic ---> datosS42_4_1.csv
Drawing a graphic ---> datosS42_4_2.csv
Drawing a graphic ---> datosS42_4_3.csv
Drawing a graphic ---> datosS42_4_4.csv
Drawing a graphic ---> datosS42_5_0.csv
Drawing a graphic ---> datosS42_5_1.csv
Drawing a graphic ---> datosS42_5_2.csv
Drawing a graphic ---> datosS42_5_3.csv
Drawing a graphic ---> datosS42_5_4.csv
Drawing a graphic ---> datosVSWR(1)_0_0.csv
Drawing a graphic ---> datosVSWR(1)_0_1.csv
Drawing a graphic ---> datosVSWR(1)_0_2.csv
Drawing a graphic ---> datosVSWR(1)_0_3.csv
Drawing a graphic ---> datosVSWR(1)_0_4.csv
Drawing a graphic ---> datosVSWR(1)_1_0.csv
Drawing a graphic ---> datosVSWR(1)_1_1.csv
Drawing a graphic ---> datosVSWR(1)_1_2.csv
Drawing a graphic ---> datosVSWR(1)_1_3.csv
Drawing a graphic ---> datosVSWR(1)_1_4.csv
Drawing a graphic ---> datosVSWR(1)_2_0.csv
Drawing a graphic ---> datosVSWR(1)_2_1.csv
Drawing a graphic ---> datosVSWR(1)_2_2.csv
Drawing a graphic ---> datosVSWR(1)_2_3.csv
Drawing a graphic ---> datosVSWR(1)_2_4.csv
Drawing a graphic ---> datosVSWR(1)_3_0.csv
Drawing a graphic ---> datosVSWR(1)_3_1.csv
Drawing a graphic ---> datosVSWR(1)_3_2.csv
Drawing a graphic ---> datosVSWR(1)_3_3.csv
Drawing a graphic ---> datosVSWR(1)_3_4.csv
Drawing a graphic ---> datosVSWR(1)_4_0.csv
Drawing a graphic ---> datosVSWR(1)_4_1.csv
Drawing a graphic ---> datosVSWR(1)_4_2.csv
Drawing a graphic ---> datosVSWR(1)_4_3.csv
Drawing a graphic ---> datosVSWR(1)_4_4.csv
Drawing a graphic ---> datosVSWR(1)_5_0.csv
Drawing a graphic ---> datosVSWR(1)_5_1.csv
Drawing a graphic ---> datosVSWR(1)_5_2.csv
Drawing a graphic ---> datosVSWR(1)_5_3.csv
Drawing a graphic ---> datosVSWR(1)_5_4.csv
Drawing a graphic ---> datosVSWR(2)_0_0.csv
Drawing a graphic ---> datosVSWR(2)_0_1.csv
Drawing a graphic ---> datosVSWR(2)_0_2.csv
Drawing a graphic ---> datosVSWR(2)_0_3.csv
Drawing a graphic ---> datosVSWR(2)_0_4.csv
Drawing a graphic ---> datosVSWR(2)_1_0.csv
Drawing a graphic ---> datosVSWR(2)_1_1.csv
Drawing a graphic ---> datosVSWR(2)_1_2.csv
Drawing a graphic ---> datosVSWR(2)_1_3.csv
Drawing a graphic ---> datosVSWR(2)_1_4.csv
Drawing a graphic ---> datosVSWR(2)_2_0.csv
Drawing a graphic ---> datosVSWR(2)_2_1.csv
Drawing a graphic ---> datosVSWR(2)_2_2.csv
Drawing a graphic ---> datosVSWR(2)_2_3.csv
Drawing a graphic ---> datosVSWR(2)_2_4.csv
Drawing a graphic ---> datosVSWR(2)_3_0.csv
Drawing a graphic ---> datosVSWR(2)_3_1.csv
Drawing a graphic ---> datosVSWR(2)_3_2.csv
Drawing a graphic ---> datosVSWR(2)_3_3.csv
Drawing a graphic ---> datosVSWR(2)_3_4.csv
Drawing a graphic ---> datosVSWR(2)_4_0.csv
Drawing a graphic ---> datosVSWR(2)_4_1.csv
Drawing a graphic ---> datosVSWR(2)_4_2.csv
Drawing a graphic ---> datosVSWR(2)_4_3.csv
Drawing a graphic ---> datosVSWR(2)_4_4.csv
Drawing a graphic ---> datosVSWR(2)_5_0.csv
Drawing a graphic ---> datosVSWR(2)_5_1.csv
Drawing a graphic ---> datosVSWR(2)_5_2.csv
Drawing a graphic ---> datosVSWR(2)_5_3.csv
Drawing a graphic ---> datosVSWR(2)_5_4.csv
Drawing a graphic ---> datosVSWR(3)_0_0.csv
Drawing a graphic ---> datosVSWR(3)_0_1.csv
Drawing a graphic ---> datosVSWR(3)_0_2.csv
Drawing a graphic ---> datosVSWR(3)_0_3.csv
Drawing a graphic ---> datosVSWR(3)_0_4.csv
Drawing a graphic ---> datosVSWR(3)_1_0.csv
Drawing a graphic ---> datosVSWR(3)_1_1.csv
Drawing a graphic ---> datosVSWR(3)_1_2.csv
Drawing a graphic ---> datosVSWR(3)_1_3.csv
Drawing a graphic ---> datosVSWR(3)_1_4.csv
Drawing a graphic ---> datosVSWR(3)_2_0.csv
Drawing a graphic ---> datosVSWR(3)_2_1.csv
Drawing a graphic ---> datosVSWR(3)_2_2.csv
Drawing a graphic ---> datosVSWR(3)_2_3.csv
Drawing a graphic ---> datosVSWR(3)_2_4.csv
Drawing a graphic ---> datosVSWR(3)_3_0.csv
Drawing a graphic ---> datosVSWR(3)_3_1.csv
Drawing a graphic ---> datosVSWR(3)_3_2.csv
Drawing a graphic ---> datosVSWR(3)_3_3.csv
Drawing a graphic ---> datosVSWR(3)_3_4.csv
Drawing a graphic ---> datosVSWR(3)_4_0.csv
Drawing a graphic ---> datosVSWR(3)_4_1.csv
Drawing a graphic ---> datosVSWR(3)_4_2.csv
Drawing a graphic ---> datosVSWR(3)_4_3.csv
Drawing a graphic ---> datosVSWR(3)_4_4.csv
Drawing a graphic ---> datosVSWR(3)_5_0.csv
Drawing a graphic ---> datosVSWR(3)_5_1.csv
Drawing a graphic ---> datosVSWR(3)_5_2.csv
Drawing a graphic ---> datosVSWR(3)_5_3.csv
Drawing a graphic ---> datosVSWR(3)_5_4.csv
Drawing a graphic ---> datosVSWR(4)_0_0.csv
Drawing a graphic ---> datosVSWR(4)_0_1.csv
Drawing a graphic ---> datosVSWR(4)_0_2.csv
Drawing a graphic ---> datosVSWR(4)_0_3.csv
Drawing a graphic ---> datosVSWR(4)_0_4.csv
Drawing a graphic ---> datosVSWR(4)_1_0.csv
Drawing a graphic ---> datosVSWR(4)_1_1.csv
Drawing a graphic ---> datosVSWR(4)_1_2.csv
Drawing a graphic ---> datosVSWR(4)_1_3.csv
Drawing a graphic ---> datosVSWR(4)_1_4.csv
Drawing a graphic ---> datosVSWR(4)_2_0.csv
Drawing a graphic ---> datosVSWR(4)_2_1.csv
Drawing a graphic ---> datosVSWR(4)_2_2.csv
Drawing a graphic ---> datosVSWR(4)_2_3.csv
Drawing a graphic ---> datosVSWR(4)_2_4.csv
Drawing a graphic ---> datosVSWR(4)_3_0.csv
Drawing a graphic ---> datosVSWR(4)_3_1.csv
Drawing a graphic ---> datosVSWR(4)_3_2.csv
Drawing a graphic ---> datosVSWR(4)_3_3.csv
Drawing a graphic ---> datosVSWR(4)_3_4.csv
Drawing a graphic ---> datosVSWR(4)_4_0.csv
Drawing a graphic ---> datosVSWR(4)_4_1.csv
Drawing a graphic ---> datosVSWR(4)_4_2.csv
Drawing a graphic ---> datosVSWR(4)_4_3.csv
Drawing a graphic ---> datosVSWR(4)_4_4.csv
Drawing a graphic ---> datosVSWR(4)_5_0.csv
Drawing a graphic ---> datosVSWR(4)_5_1.csv
Drawing a graphic ---> datosVSWR(4)_5_2.csv
Drawing a graphic ---> datosVSWR(4)_5_3.csv
Drawing a graphic ---> datosVSWR(4)_5_4.csv
Drawing a graphic ---> datosZ11_0_0.csv
Drawing a graphic ---> datosZ11_0_1.csv
Drawing a graphic ---> datosZ11_0_2.csv
Drawing a graphic ---> datosZ11_0_3.csv
Drawing a graphic ---> datosZ11_0_4.csv
Drawing a graphic ---> datosZ11_1_0.csv
Drawing a graphic ---> datosZ11_1_1.csv
Drawing a graphic ---> datosZ11_1_2.csv
Drawing a graphic ---> datosZ11_1_3.csv
Drawing a graphic ---> datosZ11_1_4.csv
Drawing a graphic ---> datosZ11_2_0.csv
Drawing a graphic ---> datosZ11_2_1.csv
Drawing a graphic ---> datosZ11_2_2.csv
Drawing a graphic ---> datosZ11_2_3.csv
Drawing a graphic ---> datosZ11_2_4.csv
Drawing a graphic ---> datosZ11_3_0.csv
Drawing a graphic ---> datosZ11_3_1.csv
Drawing a graphic ---> datosZ11_3_2.csv
Drawing a graphic ---> datosZ11_3_3.csv
Drawing a graphic ---> datosZ11_3_4.csv
Drawing a graphic ---> datosZ11_4_0.csv
Drawing a graphic ---> datosZ11_4_1.csv
Drawing a graphic ---> datosZ11_4_2.csv
Drawing a graphic ---> datosZ11_4_3.csv
Drawing a graphic ---> datosZ11_4_4.csv
Drawing a graphic ---> datosZ11_5_0.csv
Drawing a graphic ---> datosZ11_5_1.csv
Drawing a graphic ---> datosZ11_5_2.csv
Drawing a graphic ---> datosZ11_5_3.csv
Drawing a graphic ---> datosZ11_5_4.csv
Drawing a graphic ---> datosZ21_0_0.csv
Drawing a graphic ---> datosZ21_0_1.csv
Drawing a graphic ---> datosZ21_0_2.csv
Drawing a graphic ---> datosZ21_0_3.csv
Drawing a graphic ---> datosZ21_0_4.csv
Drawing a graphic ---> datosZ21_1_0.csv
Drawing a graphic ---> datosZ21_1_1.csv
Drawing a graphic ---> datosZ21_1_2.csv
Drawing a graphic ---> datosZ21_1_3.csv
Drawing a graphic ---> datosZ21_1_4.csv
Drawing a graphic ---> datosZ21_2_0.csv
Drawing a graphic ---> datosZ21_2_1.csv
Drawing a graphic ---> datosZ21_2_2.csv
Drawing a graphic ---> datosZ21_2_3.csv
Drawing a graphic ---> datosZ21_2_4.csv
Drawing a graphic ---> datosZ21_3_0.csv
Drawing a graphic ---> datosZ21_3_1.csv
Drawing a graphic ---> datosZ21_3_2.csv
Drawing a graphic ---> datosZ21_3_3.csv
Drawing a graphic ---> datosZ21_3_4.csv
Drawing a graphic ---> datosZ21_4_0.csv
Drawing a graphic ---> datosZ21_4_1.csv
Drawing a graphic ---> datosZ21_4_2.csv
Drawing a graphic ---> datosZ21_4_3.csv
Drawing a graphic ---> datosZ21_4_4.csv
Drawing a graphic ---> datosZ21_5_0.csv
Drawing a graphic ---> datosZ21_5_1.csv
Drawing a graphic ---> datosZ21_5_2.csv
Drawing a graphic ---> datosZ21_5_3.csv
Drawing a graphic ---> datosZ21_5_4.csv
Drawing a graphic ---> datosZ31_0_0.csv
Drawing a graphic ---> datosZ31_0_1.csv
Drawing a graphic ---> datosZ31_0_2.csv
Drawing a graphic ---> datosZ31_0_3.csv
Drawing a graphic ---> datosZ31_0_4.csv
Drawing a graphic ---> datosZ31_1_0.csv
Drawing a graphic ---> datosZ31_1_1.csv
Drawing a graphic ---> datosZ31_1_2.csv
Drawing a graphic ---> datosZ31_1_3.csv
Drawing a graphic ---> datosZ31_1_4.csv
Drawing a graphic ---> datosZ31_2_0.csv
Drawing a graphic ---> datosZ31_2_1.csv
Drawing a graphic ---> datosZ31_2_2.csv
Drawing a graphic ---> datosZ31_2_3.csv
Drawing a graphic ---> datosZ31_2_4.csv
Drawing a graphic ---> datosZ31_3_0.csv
Drawing a graphic ---> datosZ31_3_1.csv
Drawing a graphic ---> datosZ31_3_2.csv
Drawing a graphic ---> datosZ31_3_3.csv
Drawing a graphic ---> datosZ31_3_4.csv
Drawing a graphic ---> datosZ31_4_0.csv
Drawing a graphic ---> datosZ31_4_1.csv
Drawing a graphic ---> datosZ31_4_2.csv
Drawing a graphic ---> datosZ31_4_3.csv
Drawing a graphic ---> datosZ31_4_4.csv
Drawing a graphic ---> datosZ31_5_0.csv
Drawing a graphic ---> datosZ31_5_1.csv
Drawing a graphic ---> datosZ31_5_2.csv
Drawing a graphic ---> datosZ31_5_3.csv
Drawing a graphic ---> datosZ31_5_4.csv
Drawing a graphic ---> datosZ41_0_0.csv
Drawing a graphic ---> datosZ41_0_1.csv
Drawing a graphic ---> datosZ41_0_2.csv
Drawing a graphic ---> datosZ41_0_3.csv
Drawing a graphic ---> datosZ41_0_4.csv
Drawing a graphic ---> datosZ41_1_0.csv
Drawing a graphic ---> datosZ41_1_1.csv
Drawing a graphic ---> datosZ41_1_2.csv
Drawing a graphic ---> datosZ41_1_3.csv
Drawing a graphic ---> datosZ41_1_4.csv
Drawing a graphic ---> datosZ41_2_0.csv
Drawing a graphic ---> datosZ41_2_1.csv
Drawing a graphic ---> datosZ41_2_2.csv
Drawing a graphic ---> datosZ41_2_3.csv
Drawing a graphic ---> datosZ41_2_4.csv
Drawing a graphic ---> datosZ41_3_0.csv
Drawing a graphic ---> datosZ41_3_1.csv
Drawing a graphic ---> datosZ41_3_2.csv
Drawing a graphic ---> datosZ41_3_3.csv
Drawing a graphic ---> datosZ41_3_4.csv
Drawing a graphic ---> datosZ41_4_0.csv
Drawing a graphic ---> datosZ41_4_1.csv
Drawing a graphic ---> datosZ41_4_2.csv
Drawing a graphic ---> datosZ41_4_3.csv
Drawing a graphic ---> datosZ41_4_4.csv
Drawing a graphic ---> datosZ41_5_0.csv
Drawing a graphic ---> datosZ41_5_1.csv
Drawing a graphic ---> datosZ41_5_2.csv
Drawing a graphic ---> datosZ41_5_3.csv
Drawing a graphic ---> datosZ41_5_4.csv
Drawing a graphic ---> datosZ42_0_0.csv
Drawing a graphic ---> datosZ42_0_1.csv
Drawing a graphic ---> datosZ42_0_2.csv
Drawing a graphic ---> datosZ42_0_3.csv
Drawing a graphic ---> datosZ42_0_4.csv
Drawing a graphic ---> datosZ42_1_0.csv
Drawing a graphic ---> datosZ42_1_1.csv
Drawing a graphic ---> datosZ42_1_2.csv
Drawing a graphic ---> datosZ42_1_3.csv
Drawing a graphic ---> datosZ42_1_4.csv
Drawing a graphic ---> datosZ42_2_0.csv
Drawing a graphic ---> datosZ42_2_1.csv
Drawing a graphic ---> datosZ42_2_2.csv
Drawing a graphic ---> datosZ42_2_3.csv
Drawing a graphic ---> datosZ42_2_4.csv
Drawing a graphic ---> datosZ42_3_0.csv
Drawing a graphic ---> datosZ42_3_1.csv
Drawing a graphic ---> datosZ42_3_2.csv
Drawing a graphic ---> datosZ42_3_3.csv
Drawing a graphic ---> datosZ42_3_4.csv
Drawing a graphic ---> datosZ42_4_0.csv
Drawing a graphic ---> datosZ42_4_1.csv
Drawing a graphic ---> datosZ42_4_2.csv
Drawing a graphic ---> datosZ42_4_3.csv
Drawing a graphic ---> datosZ42_4_4.csv
Drawing a graphic ---> datosZ42_5_0.csv
Drawing a graphic ---> datosZ42_5_1.csv
Drawing a graphic ---> datosZ42_5_2.csv
Drawing a graphic ---> datosZ42_5_3.csv
Drawing a graphic ---> datosZ42_5_4.csv
Drawing a graphic ---> pha_imb_0_0.csv
Drawing a graphic ---> pha_imb_0_1.csv
Drawing a graphic ---> pha_imb_0_2.csv
Drawing a graphic ---> pha_imb_0_3.csv
Drawing a graphic ---> pha_imb_0_4.csv
Drawing a graphic ---> pha_imb_1_0.csv
Drawing a graphic ---> pha_imb_1_1.csv
Drawing a graphic ---> pha_imb_1_2.csv
Drawing a graphic ---> pha_imb_1_3.csv
Drawing a graphic ---> pha_imb_1_4.csv
Drawing a graphic ---> pha_imb_2_0.csv
Drawing a graphic ---> pha_imb_2_1.csv
Drawing a graphic ---> pha_imb_2_2.csv
Drawing a graphic ---> pha_imb_2_3.csv
Drawing a graphic ---> pha_imb_2_4.csv
Drawing a graphic ---> pha_imb_3_0.csv
Drawing a graphic ---> pha_imb_3_1.csv
Drawing a graphic ---> pha_imb_3_2.csv
Drawing a graphic ---> pha_imb_3_3.csv
Drawing a graphic ---> pha_imb_3_4.csv
Drawing a graphic ---> pha_imb_4_0.csv
Drawing a graphic ---> pha_imb_4_1.csv
Drawing a graphic ---> pha_imb_4_2.csv
Drawing a graphic ---> pha_imb_4_3.csv
Drawing a graphic ---> pha_imb_4_4.csv
Drawing a graphic ---> pha_imb_5_0.csv
Drawing a graphic ---> pha_imb_5_1.csv
Drawing a graphic ---> pha_imb_5_2.csv
Drawing a graphic ---> pha_imb_5_3.csv
Drawing a graphic ---> pha_imb_5_4.csv
Files read and drawn:480

The process has ended,  verify that the draw graphic is in 'figures' folder in the entered ID folder
Press intro to continue...
```
The graphics drawed will save in the figures folder between the ID folder previously request.
#### Draw one reports comparitions
For use this option is necessary that the two file have the same magnitude otherwise the graphic could see wrong.
Firstly, will be request the path (be suggest complete path not relative path) of first file. In the same way, will be request the path of second file. 
```
-----\Graphics tools
1> Draw one report
2> Draw one complete iterations
3> Draw one complete ejecution
4> Draw one reports comparitions
5> Back
Enter an option: 4
Enter the path file 1: C:\Users\ESTACION\Documents\GitHub\PSO_for_hybrids_and_antennas\results\8b041a42-8bae-4df9-9f44-b909f84038c9\files\amp_imb_0_0.csv
Enter the path file 2: C:\Users\ESTACION\Documents\GitHub\PSO_for_hybrids_and_antennas\results\8b041a42-8bae-4df9-9f44-b909f84038c9\files\amp_imb_5_4.csv
```
Next, will be request the save path, however, if you press Intro with this field empty, the save path will be ../results/comparison graphics/
* Example with specific save path
```
Note: if you press intro without add nothign path, this will save in ../results/comparison graphics/ by default
Enter the save path: C:\Users\Astrolab\Documents\Jaime\Comparaciones 
```
* Example with default save path
```
Note: if you press intro without add nothign path, this will save in ../results/comparison graphics/ by default
Enter the save path:
```
later, will be request the labels of *x* and *y* axis, the Title of the graphic,this will be the same of the save file name (this name cannot have dots) and the label  of each file tha will present in the graphic. when the process finish a message will notify it
```
Note: if you press intro without add nothign path, this will save in ../results/comparison graphics/ by default
Enter the save path:
Enter the axis x label: Frequency (GHz)
Enter the axis y label: dB
Enter the graphic title: Amplitud imbalace before to optimization vs after optimization
Enter the label of the  data to file 1: Initial particle
Enter the label of the  data to file 2: Optimizate particle

The process has ended,  verify that the draw graphic is in the entered path or the default path
Press intro to continue...
```
<!-- ### Set up -->
### Exit
This option is for end the script that is running

__*Developed by:*__ German Chaparro, Jorge Cardenas,Oscar Restrepo, Sergio Mora, Jhon Vera, and Jaime Angel

__*Year:*__ 2022
