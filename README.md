# PSO_for_hybrids_and_antennas
## **Geometry Optimization**

This package is intended to provide a tool that supports the optimization process of different components, such as hybrids or antennas, in which electromagnetic performance is highly dependent on geometry.

We apply optimization algorithms supported by HFSS simulations, which provide a reliable tool to evaluate how every alternative geometry behaves and to collect data derived from every optimization batch.

## **What's included**
1. ### **Version: v0.91**
-   Import and use
-   PSO optimization algorithm
-   Log file: Here you can find complete tracking of the optimization process
-   Data collection in CSV files
-   Passing configuration data through JSON files or from the code.
-   Simulation control by ID
-   Include two examples for using the PSO in Hibryds and Antennas

2. ### **Requirements**
    _Things you need to set up before executing the script._
*   [Requirements file](requirements.txt) - Make sure to install all requirements from the requirements.txt file.
    > **Note**
    > use _pip install -r requirements.txt_ in your cmd for install all requirements
*   *Design_name.py* or *Design_name.aedt* - Add a file containing the geometric model for HFSS (Python file) to the model's folder located in the root folder. If the model is a .aedt file, add this file to the Ansoft folder located in the Documents folder (the default folder that creates HFSS). in both cases (.py or .aedt files), the name of the file must be equal to the project name.

    The following example exposes a part of a python file with a dipole blade antenna geometry. Verify that the name of your file (.py or .aedt) is the same as the line responsible to define the project's name
```
# ----------------------------------------------
# Script Recorded by Ansys Electronics Desktop Student Version 2021.2.0
# 15:07:57  may. 26, 2022
# ----------------------------------------------
import PSO_core.ansys_functions as fn

import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.NewProject()
oProject.Rename("C:/Users/Astrolab/Documents/Ansoft/DIPOLE_BLADE_ANTENNA.aedt", True) #This line is responsible for the path and renaming the project
oProject.InsertDesign("HFSS", "HFSSDesign1", "HFSS Modal Network", "")
oDesign = oProject.SetActiveDesign("HFSSDesign1")
oDesign.RenameDesignInstance("HFSSDesign1", "DESIGN")
...
```

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
    * Variable name or name of the array where are the dimensions
    * Units (about of distance)
    * Maximum values that can vary the optimization
    * Minimum values that can vary the optimization
    * Nominals or default values of design
    * Number of iterations
    * Number of particles
    * Number of branches  <!-- Posiblemente se elimine -->
    * Description of simulation and relevant information
    * Reports what you need for the fitness function
    
    This information will be used as parameters for initializing the optimization with a later view method. Follow the next example:
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

*   __Third step:__ you need define your fitness function, this must recive one parameter (the data of requiered reports as a dictionary) and must return the value of the fitness function as show to continue in the follow example.
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

*   __Fourth step:__ You must initialize the system with init_system(...), this method comes from commands of the first importation, and you must add the arguments defined in the second step.

    The order of arguments in the init_system method is:

    | Position |  argument name | data type | description |
    |:--------:|:--------------:|:---------:| :---------:|
    |     1    |    ansys_exe   |    str    | A string that saves the executable path of Ansys |
    |     2    | ansys_save_def |    str    | A string that saves the default save path of Ansys |
    |     3    |  project_name  |    str    | A string that saves the project's name  |
    |     4    |   design_name  |    str    | A string that saves the designs's name |
    |     5    |  variable_name |    str    | Variable name or name of the array where are the dimensions |
    |     6    |      units     |    str    | A string that contains the units of dimensions (in distance) of the design |
    |     7    |       max      |    lst    | A list with maximun values that can take the PSO for the particles, this values must be numbers |
    |     8    |       min      |    lst    | A list with minimum values that can take the PSO for the particles, these values must be numbers |
    |     9    |     nomilas    |    lst    | A list with default values that can take the PSO for the particles, these values must be numbers |
    |    10    |   iterations   |    int    | An integer that defines how many iterations will execute the code |
    |    11    |    particles   |    int    | An integer that defines how many particles will be created |
    |    12    |    branches    |    int    | An integer that defines how many branches have the hybrid |
    |    13    |     reports    |    dict   | A dictionary containing the required reports will be used in the fitness function. Among these reports are: parameter  Smn, parameter Zmn, Gain phi x angle, Amplitude imbalance, phase imbalance, and VSWR(x port) |
    |    14    |    category    |    str    | A string that contains the category of design, for example, “Antenna”, “Hybrid”, “Filter”, among others |
    |    15    |  sub_category  |    str    | A string that contains the category of design, for example, "Dipole blade", "Low pass", "8 branches", among others |
    |    16    |   description  |    str    | A string with add/relevant information on design |

    As you see in the following example (using the data before defined):
    ```
    commands.init_system(exe, save, pname, dname,vname, u, ma, mi, nom, i, p, b, reports, category, sub_category, desc)
    ```

* __Fifth step:__ You must use the main_menu(...), this method comes on from Interfaz of the second importation, and you must add the fitness function as an argument of main_menu(...) as shown in the following example:

    ```
    Interfaz.main_menu(fit)
    ```

## **How to use**

After verifying all requirements and saving your main script, you can run that script in cmd, as shown below.

```
C:\Users\Astrolab\Documents\Jaime\Temporal>python3 Example_1.py
```
Another form to run your code is using some IDLE such as VSCode, Spider, and Conda, among others.

To interact with the interface of the optimizer, you will be accessed the following options:

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
Firstly, this option verifies that the model exists using the Ansys or python files. In case of the software cannot run the files, it will autorun trying to run successfully repeatedly; if this does not result, the software will notify you of the error and go back to the main menu.

Once the model is verified, the software will ask if you want to graphic the reports. Write 'Y' or 'N' in the console and press the Intro. The optimization will start the process of creating the particles (new random dimensions), followed by the simulation of this design in ANSYS, exporting the reports previously request, and according to requirement drawing the graphics (saves it in ../ID/figures/).later, with the data reports the software will evaluate the fitness function and new particles dimensions. This process will repeat for all iterations and particles until the end.

When the optimization process finishes, all results obtained will save in the _ output.csv file located in the results folder (.../results/output.csv). In this file, you will find the ID, time to start and end, type, category, sub-category, simulation parameters, results, and best particles. All this ordinate for rows as summaries to each iteration.
### Fitness function test
This option allows to execution of a new simulation based on previous results. For this, it is necessary to have the previous ID of one simulation and the different reports files (.csv) and to have loaded the exact parameters of the previous simulation. As option 1 (Optimization), you could choose if you draw the graphics or not.

This option makes a fast test with different fitness functions since skipping the simulation step uses more time in all simulation processes. However, for this reason, also you must understand that the optimization shows new dimensions it has not simulated.

In the same way that the previous option, all data obtained will save in the _output.csv_ file in ../results/output.csv.
### Graphics tools
This option has a menu that allows drawing graphics of reports simulated as it's shown in the following.
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
Firstly, this option will request a previously simulated ID. Later the file name to draw (you could write the '.csv' extensión or not). Next, you will need to define the label of the x-axis, which is associated with magnitude in frequency (not applied to the gain phi graphics), and the process will finish with a message that the process ends.
```
-----\Graphics tools
1> Draw one report
2> Draw one complete iterations
3> Draw one complete ejecution
4> Draw one reports comparitions
5> Back
Enter an option: 1
Enter a previously simulate ID: b2466c28-8fe8-4b71-af6c-fd435b6e5418
Enter the file name: datosS11_1_0.csv
Enter the magnitude of frequency (for example Hz, KHz, MHz, GHz, among others): MHz

The process has ended,  verify that the draw graphic is in 'figures' folder in the entered ID folder
Press intro to continue...
```
The graphics drawn will be saved in the figures folder between the previously requested ID folder.
#### Draw one complete iteration
As in the previous option, this will request a previously simulated ID followed by the number of iterations to draw and the label of the x-axis (not applicable to the gain phi graphics). Next, while the software draws the graphics, the screen will show the drawn files' names, and the process will finish with a notification on the screen.

```
-----\Graphics tools
1> Draw one report
2> Draw one complete iterations
3> Draw one complete ejecution
4> Draw one reports comparitions
5> Back
Enter an option: 2
Enter a previously simulate ID: b2466c28-8fe8-4b71-af6c-fd435b6e5418
Enter the iteration number: 2
Enter the magnitude of frequency (for example Hz, KHz, MHz, GHz, among others): MHz
Drawing a graphic ---> datosGananciaPhi0_2_0.csv
Drawing a graphic ---> datosGananciaPhi0_2_1.csv
Drawing a graphic ---> datosGananciaPhi90_2_0.csv
Drawing a graphic ---> datosGananciaPhi90_2_1.csv
Drawing a graphic ---> datosS11_2_0.csv
Drawing a graphic ---> datosS11_2_1.csv
Drawing a graphic ---> datosVSWR(1)_2_0.csv
Drawing a graphic ---> datosVSWR(1)_2_1.csv
Drawing a graphic ---> datosZ11_2_0.csv
Drawing a graphic ---> datosZ11_2_1.csv

The process has ended,  verify that the draw graphic is in 'figures' folder in the entered ID folder
Press intro to continue...
```
The graphics drawn will be saved in the figures folder between the previously requested ID folder.
#### Draw one complete execution
As in the previous option, this will request a previously simulated ID and the x-axis label (not applicable to the gain phi graphics). Next, while the software draws the graphics, the screen will show the name of the drawn files, and the process will finish with a count of files read and drawn, followed by a notification on the screen that it finished.
```
-----\Graphics tools
1> Draw one report
2> Draw one complete iterations 
3> Draw one complete ejecution  
4> Draw one reports comparitions
5> Back
Enter an option: 3
Enter a previously simulate ID: b2466c28-8fe8-4b71-af6c-fd435b6e5418
Enter the magnitude of frequency (for example Hz, KHz, MHz, GHz, among others): MHz
Drawing a graphic ---> datosGananciaPhi0_0_0.csv
Drawing a graphic ---> datosGananciaPhi0_0_1.csv
Drawing a graphic ---> datosGananciaPhi0_1_0.csv
Drawing a graphic ---> datosGananciaPhi0_1_1.csv
Drawing a graphic ---> datosGananciaPhi0_2_0.csv
Drawing a graphic ---> datosGananciaPhi0_2_1.csv
Drawing a graphic ---> datosGananciaPhi90_0_0.csv
Drawing a graphic ---> datosGananciaPhi90_0_1.csv
Drawing a graphic ---> datosGananciaPhi90_1_0.csv
Drawing a graphic ---> datosGananciaPhi90_1_1.csv
Drawing a graphic ---> datosGananciaPhi90_2_0.csv
Drawing a graphic ---> datosGananciaPhi90_2_1.csv
Drawing a graphic ---> datosS11_0_0.csv
Drawing a graphic ---> datosS11_0_1.csv
Drawing a graphic ---> datosS11_1_0.csv
Drawing a graphic ---> datosS11_1_1.csv
Drawing a graphic ---> datosS11_2_0.csv
Drawing a graphic ---> datosS11_2_1.csv
Drawing a graphic ---> datosVSWR(1)_0_0.csv
Drawing a graphic ---> datosVSWR(1)_0_1.csv
Drawing a graphic ---> datosVSWR(1)_1_0.csv
Drawing a graphic ---> datosVSWR(1)_1_1.csv
Drawing a graphic ---> datosVSWR(1)_2_0.csv
Drawing a graphic ---> datosVSWR(1)_2_1.csv
Drawing a graphic ---> datosZ11_0_0.csv
Drawing a graphic ---> datosZ11_0_1.csv
Drawing a graphic ---> datosZ11_1_0.csv
Drawing a graphic ---> datosZ11_1_1.csv
Drawing a graphic ---> datosZ11_2_0.csv
Drawing a graphic ---> datosZ11_2_1.csv
Files read and drawn:30

The process has ended,  verify that the draw graphic is in 'figures' folder in the entered ID folder
Press intro to continue...
```
The graphics drawn will be saved in the figures folder between the previously requested ID folder.
#### Draw one reports comparison
For use, this option is necessary that the two files have the same magnitude; otherwise, the graphic could see wrong.

Firstly, it will request the path (suggest a complete path, not a relative path) of the first file. In the same way, it will request the path of the second file. 
```
-----\Graphics tools
1> Draw one report
2> Draw one complete iterations
3> Draw one complete ejecution
4> Draw one reports comparitions
5> Back
Enter an option: 4
Enter the path file 1: C:\Users\ESTACION\Documents\GitHub\PSO_for_hybrids_and_antennas\results\b2466c28-8fe8-4b71-af6c-fd435b6e5418\files\datosS11_0_1.csv
Enter the path file 2: C:\Users\ESTACION\Documents\GitHub\PSO_for_hybrids_and_antennas\results\b2466c28-8fe8-4b71-af6c-fd435b6e5418\files\datosS11_2_1.csv
```
Next, it will request the save path; however, if you press Intro with this field empty, the save path will be ../results/comparison graphics/
* Example with specific save path
```
Note: if you press intro without add nothign path, this will save in ../results/comparison graphics/ by default
Enter the save path: C:\Users\ESTACION\Documents\Jaime\Comparaciones 
```
* Example with default save path
```
Note: if you press intro without add nothign path, this will save in ../results/comparison graphics/ by default
Enter the save path:
```
Later, it will request the labels of the x and y-axis, the Title of the graphic, which will be the same as the save file name (this name cannot have dots), and the label of each file that will present in the graphic. When the process finishes, a message will notify it.
```
Note: if you press intro without add nothign path, this will save in ../results/comparison graphics/ by default
Enter the save path: C:\Users\Astrolab\Documents\Jaime\Comparaciones
Enter the axis x label: Frequency (MHz)
Enter the axis y label: dB
Enter the graphic title: S11 initial particle vs final particle
Enter the label of the  data to file 1: Initial particle
Enter the label of the  data to file 2: Final particle 

The process has ended,  verify that the draw graphic is in the entered path or the default path
Press intro to continue...
```
<!-- ### Set up -->
### Exit
This option is to end the script that is running.

__*Developed by:*__ German Chaparro, Jorge Cardenas,Oscar Restrepo, Sergio Mora, Jhon Vera, and Jaime Angel

__*Year:*__ 2022
