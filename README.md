# PerSeO: PSO Applied to RF Device Design
## **Geometry Optimization**
This package is crafted to provide a tool that aids the optimization process for various components, such as hybrids or antennas, where the electromagnetic performance is significantly dependent on their geometric structure.

Our optimization algorithms are corroborated by HFSS simulations, thereby offering a dependable tool to assess the performance of each proposed geometry and to extract data from each optimization batch.

## **What's included**
1. ### **Version: v1.0.0**
-   Import and usage functionality
-   Implementation of the PSO optimization algorithm
-   A log file providing comprehensive tracking of the optimization process
-   Data collection in CSV format
-   Configurations passable via JSON files or directly from the code
-   Simulation control via unique IDs
-   Includes one examples demonstrating PSO usage in Antennas
-   Documentation of all methods and classes of the package
-   Package installation using [PyPI](https://pypi.org/project/perseo-optimizer/)

2. ### **Prerequisites**
    _These are configuration procedures required before using the package or the files found in this repository._
* [Python version 3.10.4](https://www.python.org/downloads/release/python-3104/) must be installed. Compatibility with other Python versions cannot be guaranteed.
*   Package installation - you must install the perseo_optimizer package, which contains all the files and data for its use. to install the package, use the command ```pip install perseo-optimizer``` in your terminal.
    > **Note**
    > if you are going to use the files found directly in this repository, you must not install the package, instead, you must install all the dependencies found in the [requirements.txt](requirements.txt) file. To do this use the _pip install -r requirements.txt_ command in your terminal

*   Package installation in IronPython (**required only if you installed the package in the last step**) - Ansys HFSS uses IronPython to use the scripting option, for this reason, it is also necessary to add the perseo_optimizer package to the IronPython packages. The folder containing the packages is located where Ansys was installed, inside the ./common/IronPython/lib/ folder. Locate this group of folders inside the path where Ansys was installed and then use the command ```pip install perseo-optimizer -t "YOUR_PATH_TO_ANSYS_IRONPYTHON_PACKAGES/"``` in your terminal.

*   *Design_name.py* or *Design_name.aedt* - Add a file containing the geometric model for HFSS (Python file) to the model's folder located in the root folder. If the model is a .aedt file, add this file to the Ansoft folder located in the Documents folder (the default folder that creates HFSS) in both cases (.py or .aedt files), the file's name  must be equal to the project name.

    The following example shows part of a Python file containing the geometry of a blade dipole antenna. The file name (.py or .aedt) should correspond to the line that defines the project name.
```
# -*- coding: utf-8 -*-
# ----------------------------------------------
# Script Recorded by Ansys Electronics Desktop Student Version 2021.2.0
# 15:07:57  may. 26, 2022
# ----------------------------------------------
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

*   __First step:__ Add the following imports to your main script:
    ```
    from perseo_optimizer import commands, interface
    ```
*   __Second step:__ Define the following parameters for the optimization process. It is recommended to save these parameters as individual variables:
    * Path to executable of ANSYS
    * Path to default save of ANSYS
    * Category of structure (Antenna, Hybrid, Filter, among others)
    * Subcategory of structure
    * Project name
    * Design name
    * Variable name or name of the array where are the dimensions
    * Units (about of distance)
    * Maximum values that can vary the optimization
    * Minimum values that can vary the optimization
    * Nominals or default values of design
    * Number of iterations
    * Number of particles
    * Number of branches  <!-- Possibly removed -->
    * Description of simulation and relevant information
    * Reports what you need for the fitness function
    
    These parameters will be used in the optimization initialization method as shown below:
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
    desc = "100%BW with ideal BW to 80MHz, denominator (or cut-off frequency) in 40MHz working in the frequency band of 40MHz to 120MHz"

    reports = {
        "SMN":[(1,1)],
        "gain":[0,90],
        "vswr":[1],
        "zmn":[(1,1)],
        "additional_data":{
            "fmin":40,
            "points":81,
            "units":"MHz"
        }
    }
    ```    

*   __Third step:__ Define your fitness function; it must take in one parameter (a dictionary of required reports) and return the value of the fitness function. Refer to the example below:
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

        print(f"\nNumber of areas: {len(areas_f)} || Mat.freq and Mat.db with same size: {len(areas_f) == len(areas_d)}\n")
        
        coefficient = 0
        if len(areas_f)==0:
            coefficient = 20
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
                coefficient =  ((80-bw)/80)**2  
                
            else:
                coefficient = 20      
        return coefficient
    ```

    Similar to the previous point, this function will be used later on.

*   __Fourth step:__ Initialize the system using the init_system(...) method from the commands module. This method takes in the parameters defined in the second step.

The order of arguments in the init_system method is as follows:

    

    | Position |  argument name | data type | description |
    |:--------:|:--------------:|:---------:| :---------:|
    |     1    |    ansys_exe   |    str    | A string that saves the executable path of Ansys |
    |     2    | ansys_save_def |    str    | A string that saves the default save path of Ansys |
    |     3    |  project_name  |    str    | A string that saves the project's name  |
    |     4    |   design_name  |    str    | A string that saves the designs's name |
    |     5    |  variable_name |    str    | Variable name or name of the array where are the dimensions |
    |     6    |      units     |    str    | A string that contains the units of dimensions (in the distance) of the design |
    |     7    |       max      |    lst    | A list with maximum values that can take the PSO for the particles. These values must be numbers |
    |     8    |       min      |    lst    | A list with minimum values that can take the PSO for the particles. These values must be numbers |
    |     9    |     nominals    |    lst    | A list with default values that can take the PSO for the particles. These values must be numbers |
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

* __Fifth step:__ You must use the main_menu(...), this method comes on from interface of the second importation, and you must add the fitness function as an argument of main_menu(...) as shown in the following example:      

    ```
    interface.main_menu(fit)
    ```

## **How to use**

Once you have verified all requirements and saved your primary script, you may run this script in your command line as depicted below:

```
C:\Users\Astrolab\Documents\Jaime\Temporal>python3 Example_1.py
```
An alternative way to execute your code involves using an Integrated Development Environment (IDE) such as VSCode, Spyder, or Anaconda, among others.

Upon interacting with the PSO optimizer's user interface, you will be presented with the following options:

```
-------->PSO APP<---------
-----\MENU
1> Optimize
2> Fitness function test
3> Graphics tools
4> Exit
Enter an option:
```

### Optimize
The first operation checks for the existence of a model utilizing Ansys or Python files. In the event the software cannot execute these files, it will continuously attempt to do so. If this attempt is not successful, the software will alert you to the error and revert to the main menu.

After the model's verification, the software will inquire if you wish to graphically represent the reports. To respond, enter 'Y' for yes or 'N' for no in the console and press Enter. The optimization process will commence by generating particles (new random dimensions) and simulating these designs in ANSYS. Subsequently, the previously requested reports will be exported, and graphics will be produced if necessary (stored in ../ID/figures/). The software will then evaluate the fitness function and generate new particle dimensions using the data reports. This process will iterate for all particles until completion.

Upon finishing the optimization process, all obtained results will be stored in the _output.csv file located in the results folder (.../results/output.csv). This file will include the ID, start and end times, type, category, sub-category, simulation parameters, results, and optimal particles. All this information will be systematically organized in rows, each summarizing an iteration.

### Fitness function test
This option allows the execution of a new simulation based on previous results. It requires the ID from a previous simulation, different report files (.csv), and the exact parameters from the previous simulation. Like option 1 (Optimization), you can choose to graphically represent the results.

This option provides a rapid test with different fitness functions by omitting the time-consuming simulation step. However, keep in mind that the optimization may show new dimensions that have not been simulated.

As with the previous option, all data obtained will be stored in the output.csv file at ../results/output.csv.

### Graphics tools
This option provides a menu that allows the creation of graphs from simulated reports. The structure is as follows:
```
-----\Graphics tools
1> Draw one report
2> Draw one complete iteration
3> Draw one complete execution
4> Draw one report comparisons
5> Back
Enter an option:
```
#### Draw one report
This feature will prompt the user for an ID associated with a prior simulation. Following this, the name of the file to be plotted is requested (the '.csv' extension can be optionally included). The user will also need to define the label for the x-axis, which corresponds to frequency magnitude (this does not apply to the gain phi graphs). The operation concludes with a confirmation message indicating that the process has completed.
```
-----\Graphics tools
1> Draw one report
2> Draw one complete iteration
3> Draw one complete execution
4> Draw one report comparisons
5> Back
Enter option: 1
Enter a previously simulate ID: b2466c28-8fe8-4b71-af6c-fd435b6e5418
Enter the file name: datosS11_1_0.csv
Enter the magnitude of frequency (for example Hz, KHz, MHz, GHz, among others): MHz

The process has ended,  verify that the draw graphic is in 'figures' folder in the entered ID folder
Press intro to continue...
```
The resulting graphics are stored in the 'figures' folder within the specified ID folder.

#### Draw a complete iteration
Similar to the previous option, this feature will ask for an ID from a previous simulation, then the iteration number to be plotted, and the label for the x-axis (not applicable to the gain phi graphs). As the software generates the graphics, the names of the files being plotted will be displayed on the screen. The process concludes with a notification on screen.

```
-----\Graphics tools
1> Draw one report
2> Draw one complete iteration
3> Draw one complete execution
4> Draw one report comparisons
5> Back
Enter option: 2
Enter a previously simulate ID: b2466c28-8fe8-4b71-af6c-fd435b6e5418
Enter the iteration number: 2
Enter the magnitude of frequency (for example, Hz, kHz, MHz, GHz, among others): MHz
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

The process has ended. Verify that the drawn graphic is in the 'figures' folder in the entered ID folder
Press intro to continue...
```
The resulting graphics are stored in the 'figures' folder within the specified ID folder.

#### Draw a Complete Execution
Similar to the previous options, this feature will ask for an ID from a previous simulation, then the unit of frequency (not applicable to the gain phi graphs). As the software generates the graphics, the names of the files being plotted will be displayed on the screen. The process concludes with a count of the files that were read and plotted, followed by a completion notification on the screen.
```
-----\Graphics tools
1> Draw one report
2> Draw one complete iteration
3> Draw one complete execution  
4> Draw one report comparisons
5> Back
Enter option: 3
Enter a previously simulate ID: b2466c28-8fe8-4b71-af6c-fd435b6e5418
Enter the magnitude of frequency (for example, Hz, kHz, MHz, GHz, among others): MHz
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

The process has ended. Verify that the drawn graphic is in the 'figures' folder in the entered ID folder.
Press intro to continue...
```
The resulting graphics are stored in the 'figures' folder within the specified ID folder.


#### Draw a Report Comparison
In order to utilize this function, it is crucial to ensure that the two files being compared share the same units of magnitude. If not, the resulting graphic may display inaccurately.

To initiate the process, the system will prompt you to input the absolute path of the first file. The same will be requested for the second file.
```
-----\Graphics tools
1> Draw one report
2> Draw one complete iteration
3> Draw one complete execution
4> Draw one report comparisons
5> Back
Enter option: 4
Enter the path file 1: C:\Users\ESTACION\Documents\GitHub\PSO_for_hybrids_and_antennas\results\b2466c28-8fe8-4b71-af6c-fd435b6e5418\files\datosS11_0_1.csv
Enter the path file 2: C:\Users\ESTACION\Documents\GitHub\PSO_for_hybrids_and_antennas\results\b2466c28-8fe8-4b71-af6c-fd435b6e5418\files\datosS11_2_1.csv
```
Next, you'll be asked to define the saving path. By default, if you press 'Enter' without providing a path, the graphic will be saved in the default path: ../results/comparison graphics/

* Example with a specific save path
```
Note: if you press Intro without adding nothing path, this will save in ../results/comparison graphics/ by default
Enter the save path: C:\Users\ESTACION\Documents\Jaime\Comparaciones 
```
* Example with default save path
```
Note: if you press Intro without adding nothing path, this will save in ../results/comparison graphics/ by default
Enter the save path:
```
Following this, the system will request labels for the x and y-axes, the graphic's title (which will also serve as the saved file name - this cannot include periods), and the data label for each file to be displayed on the graphic. When the process concludes, you will be notified with a message.
```
Note: if you press intro without add nothing path, this will save in ../results/comparison graphics/ by default
Enter the save path: C:\Users\Astrolab\Documents\Jaime\Comparaciones
Enter the axis x label: Frequency (MHz)
Enter the axis y label: dB
Enter the graphic title: S11 initial particle vs final particle
Enter the label of the  data to file 1: Initial particle
Enter the label of the  data to file 2: Final particle 

The process has ended. Verify that the drawn graphic is in the entered path or the default path.
Press intro to continue...
```

### Exit
This function is designed to terminate the currently running script.

----
__*Developed by:*__ German Chaparro, Jorge Cardenas,Oscar Restrepo, Sergio Mora, Jhon Vera, and Jaime Angel

__*Contributors:*__ Daniela Paez Díaz

__*Year:*__ 2022
