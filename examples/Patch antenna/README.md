# Patch antenna example


## What's include
- An script with patch antenna design that works to 1.7*GHz*
- An script with an example of use to PSO with a fitness function to make work the antenna to 2.6*GHz* adapted minimum to -10dB

## How to use
1. You must copy the [main.py](main.py) and paste to the root of your proyect and run the initializate of system.
2. Later you must copy the [PATCH_ANTENNA.py](PATCH_ANTENNA.py) and paste to models folder located in the root of your proyect.
3. In *PATCH_ANTENNA.py* file you must change the path that appears in the project rename like show as follow:
`oProject.Rename("C:/Users/INVESTIGACIÓN/Documents/Ansoft/PATCH_ANTENNA.aedt", True)`
You only change the path not the name of project, change this to your Ansys default save path (it should be so similar to present in the example, except for the user name folder)
4. In the main file you must change the value of `ansys_path` and `save_path` variables with you respective values (for the first with the ansys execute file path an the second with the ansys default save path)
5. Now in the main file, you must uncomment the last line of code  and run the script, in the main menu select option one, continue selecting if you would draw the graphics, and wait for the PSO end the optimization