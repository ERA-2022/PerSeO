from perseo_optimizer import commands, interface

ansys_path = r"C:\Program Files\AnsysEM\AnsysEM19.0\Win64\ansysedt.exe"  # Please change this path for your Ansys path
save_path = r'C:\Users\INVESTIGACIÓN\Documents\Ansoft/'  # Please change this path for your default Ansys save path
cat = "Planar antenna"
sub_cat = "Patch"
pro = "PATCH_ANTENNA"
des = "DESIGN"
var = "dim"
u = "mm"
val_max = [0.017, 1.57, 110, 15, 4.84, 24.05, 0.72, 50, 50, 15]
val_min = [0.017, 1.57, 110, 15, 4.84, 24.05, 0.72, 20, 50, 15]
val_nom = [0.017, 1.57, 110, 15, 4.84, 24.05, 0.72, 39, 50, 15]
i = 20
p = 10
b = 0
desc = "Patch antenna working in 2.6GHz adapted minimum to -10dB"
rep = {"SMN": [(1, 1)], "additional_data": {"fmin": 1.5, "points": 201, "units": "GHz"}}


def function_fitness(dataReports):
    # PRESENT THE REPORTS THAT HFSS  GENERATE
    for key in dataReports:
        print(str(key) + "--->" + str(len(dataReports[key])))

    # FIST FILTER TO GET ONLY DATA UNDER db <= -10
    freq = [
        dataReports['S11'][index][0] for index in range(len(dataReports["S11"])) if dataReports["S11"][index][1] <= -10
    ]
    dB = [
        dataReports['S11'][index][1] for index in range(len(dataReports["S11"])) if dataReports["S11"][index][1] <= -10
    ]

    if len(freq) == 0 or len(dB) == 0:
        # PENALTY THE FIT VALUE
        fit_value = 10

    else:
        # FIND THE WORK FREQUENCY AND POWER OF ANTENNA
        dB_min = min(dB)
        work_freq = freq[dB.index(dB_min)]

        # CALCULATE THE FIT VALUE
        fit_value = ((2.6 - work_freq) / 2.6)**2

    # RETURN CALCULATED VALUE
    return fit_value


commands.init_system(
    ansys_path, save_path, pro, des, var, u, val_max, val_min, val_nom, i, p, b, rep, cat, sub_cat, desc
)
# interface.main_menu(function_fitness)  # FIRST INITIALIZE THE SYSTEM AND LATER RUN THE MAIN MENU
