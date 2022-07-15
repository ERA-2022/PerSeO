# PSO_for_hybrids_and_antennas
Desarrollo de módulos para aplicar el modelo de optimización PSO hacia híbridos y antenas.

Para su uso es necesario tener Ansys HFSS v19 o superior instalado, python y las librerías descritas en el archivo requirements.txt de este repositorio.

## Estructuras a tener en cuenta:
- Archivo de configuración (data.json):

~~~
data_structure = {
        "paths":
        {
            "main": os.getcwd().replace('\\','/')+'/',
            "results": os.getcwd().replace('\\','/')+'/'+"results/",
            "files": "",
            "figures": "",
            "models": os.getcwd().replace('\\','/')+'/'+"models/",
            "src": os.getcwd().replace('\\','/')+'/'+"src/",
            "ansys_exe": ansys_exe,
            "ansys_save_def": ansys_save_def
        },
        "values":
        {
            "project_name": project_name,
            "design_name": design_name,
            "variable_name": variable_name,
            "units": units,
            "max": max,
            "min": min,
            "def": nomilas,
            "n_var":len(nomilas),
            "iterations": iterations,
            "particles": particles,
            "reports": reports,
            "description": description
        },
        "info":
        {
            "OS": platform,
            "ID": "",
            "start_time": 0,
            "elapsed_time": 0
        }
    }
~~~

- Reportes a generar:

~~~
reportes = {
    "smn":[(m,n),...],
    "gain":[ang1,ang2,...],
    "ampimb":"",
    "phaseimb":"",
    "vswr":"",
    "bw":"",
    "datatable":"",
}
~~~