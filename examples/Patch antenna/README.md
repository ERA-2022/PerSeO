# Patch antenna example


## What's include
- An script with patch antenna design that works to 1.7*GHz*
- An script with an example of use to PerSeO package with a fitness function to make work the antenna to 2.6*GHz* adapted minimum to -10dB

## How to use
1. You must have the perseo package installed, if not in your terminal use the command ```pip install perseo``` (it is recommended to have created a virtual environment),for more information, refer to the user manual or the [README.md](../../README.md) file in the PerSeO repository.
2. You must copy the [main.py](main.py) and paste to the root of your project and run the initialize of system.
3. Later you must copy the [PATCH_ANTENNA.py](PATCH_ANTENNA.py) and paste to models folder located in the root of your project.
4. In *PATCH_ANTENNA.py* file you must change the path that appears in the project rename like show as follow:
`oProject.Rename("C:/Users/INVESTIGACIÓN/Documents/Ansoft/PATCH_ANTENNA.aedt", True)`
You only change the path not the name of project, change this to your Ansys default save path (it should be so similar to present in the example, except for the user name folder)
5. In the main file you must change the value of `ansys_path` and `save_path` variables with you respective values (for the first with the ansys execute file path an the second with the ansys default save path)
6. Now in the main file, you must uncomment the last line of code  and run the script, in the main menu select option one, continue selecting if you would draw the graphics, and wait for end the optimization process