from PSO import commands, Interfaz
exe = "C:/Program Files/AnsysEM/Ansys Student/v212/Win64/ansysedtsv.exe"
save = "C:/Users/ESTACION/Documents/Ansoft/"
pname = "DIPOLE_BLADE_ANTENNA"
dname = "DESIGN"
vname = "variables"
u = "mm"
ma = [12050.0, 1000.0, 1500.0, 50.0, 20.0, 780.0]
mi = [11950.0, 300.0, 800.0, 5.0, 20.0, 730.0]
nom = [12000.0, 694.28571, 1180.0, 20.0, 20.0, 750.0]
i = 5
p = 3
desc = "100%BW con BW ideal a 80MHz, denominador (o frecuencia de corte)en 40MHz trabajando en la banda de frecuencia de 40MHz hasta 120MHz"

def fit (i, j):
    print("Prueba función fitness")
    print(f"valor i: {i} | valor de j: {j}")
    res = i*j
    print(f"valor: {res}")
# -> Futuro modulo de optimización
commands.init_system(exe,save,pname,dname,vname,u,ma,mi,nom,i,p,desc)
Interfaz.main_menu(fit)