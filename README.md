# PSO_for_hybrids_and_antennas
Desarrollo de módulos para aplicar el modelo de optimización PSO hacia híbridos y antenas.

Para su uso es necesario tener ANSYS HFSS v19 o superior instalado, Python y las librerías descritas en el archivo requirements.txt de este repositorio.

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
    "aditional_data":{
        "fmin":min freq,
        "points":poits to sweep (see Ansys analisis config),
        "units": units
    },
    "ampimb":"",
    "phaseimb":"",
    "vswr":"",
    "bw":"",
    "datatable":"",
}
~~~
Hay que tener en cuenta que la palabra clave "aditional_data", pues esta almacena en su interior palabras clave con la frecuencia mínima del análisis, cantidad de puntos del barrido y unidades de la frecuencia, asociadas a datos necesarios para generar los gráficos de la ganancia y otros reportes que necesiten este dato especifico.

Una vez el optimizador se haya ejecutado y comience a hacer uso de ANYSYS, al generar los reportes y devolvérselos al usuario en el parámetro de su función lo que se recibe como tal es un diccionario con las palabras clave en mayúsculas de los reportes solicitados, sin embargo, cabe resaltar que tanto la ganancia como los parámetros S los deberá llamar por el nombre especifico de ese reporte, por ejemplo, si mis parámetros solicitados fueron:

~~~
reportes = {
    "smn":[(1,1),(2,1),(3,1)],
    "gain":[0,90],
    "aditional_data":{
        "fmin":40,
        "points":81,
        "units": "MHz"
    },
    "ampimb":"",
    "vswr":"",
}
~~~

el parámetro que le llega a mi función fitness será una estructura como la siguiente:

~~~
datos = {
    "S11" = [...],
    "S21" = [...],
    "S31" = [...],
    "GAINPHI0" = [...],
    "GAINPHI90" = [...],
    "VSWR" = [...]
}
~~~
> **Note**
> En caso de acceder a los datos de ganancia, tener en cuenta que la palabra 'GAINPHI' va en mayúscula acompañada del ángulo.