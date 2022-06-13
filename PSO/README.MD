# Información de los módulos desarrollados
En esta carpeta se presenta los módulos desarrollados para el uso del PSO

## BACK UP data.json

Este archivo contempla la estructura y las rutas a tener en cuenta para que los modulos puedan funcionar correctamente

Estructura:

~~~
{
  "paths": {
    "main": "C:/Users/ESTACION/Documents/GitHub/BASIC_PSO/",
    "results": "results/",
    "src": "src/",
    "ansys_exe": "C:/Program Files/AnsysEM/Ansys Student/v212/Win64/ansysedtsv.exe",
    "ansys_save_def": "C:/Users/ESTACION/Documents/Ansoft/"
  },
  "values": {
    "model": "Dipolo_blade.aedt",
    "project_name": "DIPOLE_BLADE_ANTENNA",
    "design_name": "DESIGN",
    "variable_name": "variables",
    "units": "mm",
    "max": [
      12050.0,
      1000.0,
      1500.0,
      50.0,
      20.0,
      780.0
    ],
    "min": [
      11950.0,
      300.0,
      800.0,
      5.0,
      20.0,
      730.0
    ],
    "def": [
      12000.0,
      694.28571,
      1180.0,
      20.0,
      20.0,
      750.0
    ],
    "iterations": 5,
    "particles": 3,
    "merit_fun_info": "100%BW con BW ideal a 80MHz, denominador (o frecuencia de corte)en 40MHz trabajando en la banda de frecuencia de 40MHz hasta 120MHz"
  }
}
~~~