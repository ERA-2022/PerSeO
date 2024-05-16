# -*- coding: utf-8 -*-
"""
Authors: German Chaparro, Jorge Cardenas,Oscar Restrepo, Sergio Mora, Jhon Vera, and Jaime Angel
Year: 2022
"""

from .commands import read_data


def agregaVariable(proj, name, value):
    """Adds a variable to the Ansys HFSS design, it is suggested that the value be accompanied by the units of measurement.

    Args:
        proj (Ansys project object ): objeto que representa el proyecto de Ansys HFSS una vez abierto
        name (str): name assigned to the variable
        value (str): value that the variable will take, e.g. 5mm
    """
    oDesign = proj.SetActiveDesign(read_data()['values']['design_name'])
    oDesign.ChangeProperty([
        "NAME:AllTabs",
        [
            "NAME:LocalVariableTab", ["NAME:PropServers", "LocalVariables"],
            ["NAME:NewProps", ["NAME:" + name, "PropType:=", "VariableProp", "UserDef:=", True, "Value:=", value]]
        ]
    ])


def modificaVariable(proj, name, value):
    """Modify a variable to the Ansys HFSS design, it is suggested that the value be accompanied by the units of measurement.

    Args:
        proj (Ansys project object ): objeto que representa el proyecto de Ansys HFSS una vez abierto
        name (str): name assigned to the variable
        value (str): value that the variable will take, e.g. 5mm
    """
    oDesign = proj.SetActiveDesign(read_data()['values']['design_name'])
    oDesign.ChangeProperty([
        "NAME:AllTabs",
        [
            "NAME:LocalVariableTab", ["NAME:PropServers", "LocalVariables"],
            ["NAME:ChangedProps", ["NAME:" + name, "Value:=", value]]
        ]
    ])


def agregaArreglo(proj, name, value):
    """Adds a variable type array to the Ansys HFSS design, it is suggested that the value be accompanied by the units of measurement.

    Args:
        proj (Ansys project object ): objeto que representa el proyecto de Ansys HFSS una vez abierto
        name (str): name assigned to the array
        value (str): value that the variable will take, e.g. [5, 2, 3, 1.8]mm
    """
    oDesign = proj.SetActiveDesign(read_data()['values']['design_name'])
    oDesign.ChangeProperty([
        "NAME:AllTabs",
        [
            "NAME:LocalVariableTab", ["NAME:PropServers", "LocalVariables"],
            ["NAME:NewProps", ["NAME:" + name, "PropType:=", "VariableProp", "UserDef:=", True, "Value:=", value]]
        ]
    ])


def modificaArreglo(proj, name, value):
    """Modify a variable type array to the Ansys HFSS design, it is suggested that the value be accompanied by the units of measurement.

    Args:
        proj (Ansys project object ): objeto que representa el proyecto de Ansys HFSS una vez abierto
        name (str): name assigned to the array
        value (str): value that the variable will take, e.g. [5, 2, 3, 1.8]mm
    """
    oDesign = proj.SetActiveDesign(read_data()['values']['design_name'])
    oDesign.ChangeProperty([
        "NAME:AllTabs",
        [
            "NAME:LocalVariableTab", ["NAME:PropServers", "LocalVariables"],
            ["NAME:ChangedProps", ["NAME:" + name, "Value:=", value]]
        ]
    ])


#UNDERNEATH THE COMMANDS TO GENERATE THE S PARAMETERS ARE PRESENTED.
def creaSmn(proj, name, simID, m, n):
    """Creates, generates and exports Smn report in Ansys HFSS

    Args:
        proj (Ansys project object ): objeto que representa el proyecto de Ansys HFSS una vez abierto
        name (str): complement of the file name, usually the iteration and particle. e.g _0_0
        simID (str): simulation id
        m (str | int): port m
        n (str | int): port n
    """
    oDesign = proj.SetActiveDesign(read_data()['values']['design_name'])
    oModule = oDesign.GetModule("ReportSetup")
    oModule.CreateReport(
        "S" + m + n, "Modal Solution Data", "Rectangular Plot", "Setup1 : Sweep", ["Domain:=", "Sweep"], [
            "Freq:=",
            ["All"],
        ], ["X Component:=", "Freq", "Y Component:=", ["dB(S(" + m + "," + n + "))"]], []
    )

    oModule.ExportToFile(
        "S" + m + n,
        read_data()['paths']['results'] + str(simID) + "/files/" + r"datosS" + str(m) + str(n) + str(name) + ".csv"
    )


def creaZmn(proj, name, simID, m, n):
    """Creates, generates and exports Zmn report in Ansys HFSS

    Args:
        proj (Ansys project object ): objeto que representa el proyecto de Ansys HFSS una vez abierto
        name (str): complement of the file name, usually the iteration and particle. e.g _0_0
        simID (str): simulation id
        m (str | int): port m
        n (str | int): port n
    """
    oDesign = proj.SetActiveDesign(read_data()['values']['design_name'])
    oModule = oDesign.GetModule("ReportSetup")
    oModule.CreateReport(
        "Z" + m + n, "Modal Solution Data", "Rectangular Plot", "Setup1 : Sweep", ["Domain:=", "Sweep"], [
            "Freq:=",
            ["All"],
        ], ["X Component:=", "Freq", "Y Component:=", ["re(Z(" + m + "," + n + "))", "im(Z(" + m + "," + n + "))"]], []
    )

    oModule.ExportToFile(
        "Z" + m + n,
        read_data()['paths']['results'] + str(simID) + "/files/" + r"datosZ" + str(m) + str(n) + str(name) + ".csv"
    )


def creaAmpImb(proj, name, simID):
    """Creates, generates and exports AmpImb report in Ansys HFSS

    Args:
        proj (Ansys project object ): objeto que representa el proyecto de Ansys HFSS una vez abierto
        name (str): complement of the file name, usually the iteration and particle. e.g _0_0
        simID (str): simulation id
    """
    oDesign = proj.SetActiveDesign(read_data()['values']['design_name'])
    oModule = oDesign.GetModule("ReportSetup")
    oModule.CreateReport(
        "Amplitud Imbalance", "Modal Solution Data", "Rectangular Plot", "Setup1 : Sweep", ["Domain:=", "Sweep"], [
            "Freq:=",
            ["All"],
            "a:=",
            ["Nominal"],
        ], ["X Component:=", "Freq", "Y Component:=", ["AmpImbalance"]], []
    )

    oModule.ExportToFile(
        "Amplitud Imbalance",
        read_data()['paths']['results'] + str(simID) + "/files/" + r"amp_imb" + str(name) + ".csv"
    )


def creaPhaseImb(proj, name, simID):
    """Creates, generates and exports PhaseImb report in Ansys HFSS

    Args:
        proj (Ansys project object ): objeto que representa el proyecto de Ansys HFSS una vez abierto
        name (str): complement of the file name, usually the iteration and particle. e.g _0_0
        simID (str): simulation id
    """
    oDesign = proj.SetActiveDesign(read_data()['values']['design_name'])
    oModule = oDesign.GetModule("ReportSetup")
    oModule.CreateReport(
        "Phase Imbalance", "Modal Solution Data", "Rectangular Plot", "Setup1 : Sweep", ["Domain:=", "Sweep"], [
            "Freq:=",
            ["All"],
        ], ["X Component:=", "Freq", "Y Component:=", ["PhaseImb"]], []
    )

    oModule.ExportToFile(
        "Phase Imbalance",
        read_data()['paths']['results'] + str(simID) + "/files/" + r"pha_imb" + str(name) + ".csv"
    )


#UNDERNEATH THE COMMANDS TO GENERATE THE VSWR, GAIN, BW AND DATA TABLE PARAMETERS.
def creaVSWR(proj, name, simID, port):
    """Creates, generates and exports VSWR report in Ansys HFSS

    Args:
        proj (Ansys project object ): objeto que representa el proyecto de Ansys HFSS una vez abierto
        name (str): complement of the file name, usually the iteration and particle. e.g _0_0
        simID (str): simulation id
        port (str | int): port to be analyzed
    """
    oDesign = proj.SetActiveDesign(read_data()['values']['design_name'])
    oModule = oDesign.GetModule("ReportSetup")

    oModule.CreateReport(
        "VSWR(" + port + ")", "Modal Solution Data", "Rectangular Plot", "Setup1 : Sweep", ["Domain:=", "Sweep"],
        ["Freq:=", ["All"], "frec:=", ["Nominal"], "t:=", ["Nominal"]],
        ["X Component:=", "Freq", "Y Component:=", ["VSWR(" + port + ")"]], []
    )
    direccion = read_data(
    )['paths']['results'] + str(simID) + "/files/" + r"datosVSWR(" + str(port) + ")" + str(name) + ".csv"
    oModule.ExportToFile("VSWR(" + str(port) + ")", direccion)


def creaGain(proj, name, simID, angle):
    """Creates, generates and exports gain report in Ansys HFSS

    Args:
        proj (Ansys project object ): objeto que representa el proyecto de Ansys HFSS una vez abierto
        name (str): complement of the file name, usually the iteration and particle. e.g _0_0
        simID (str): simulation id
        angle (str | int | float): angle to be analyzed
    """
    oDesign = proj.SetActiveDesign(read_data()['values']['design_name'])
    oModule = oDesign.GetModule("ReportSetup")
    oModule.CreateReport(
        "Gain Phi " + str(angle), "Far Fields", "Rectangular Plot", "Setup1 : Sweep", ["Context:=", "phi" + str(angle)],
        ["Theta:=", ["All"], "Phi:=", ["All"], "Freq:=", ["All"], "frec:=", ["Nominal"], "t:=", ["Nominal"]],
        ["X Component:=", "Theta", "Y Component:=", ["GainTotal"]], []
    )

    direccion = read_data(
    )['paths']['results'] + str(simID) + "/files/" + r"datosGananciaPhi" + str(angle) + str(name) + ".csv"
    oModule.ExportToFile("Gain Phi " + str(angle), direccion)


def creaBW(proj, name, simID):
    """Creates, generates and exports BW report in Ansys HFSS

    Args:
        proj (Ansys project object ): objeto que representa el proyecto de Ansys HFSS una vez abierto
        name (str): complement of the file name, usually the iteration and particle. e.g _0_0
        simID (str): simulation id
    """
    oDesign = proj.SetActiveDesign(read_data()['values']['design_name'])
    oModule = oDesign.GetModule("ReportSetup")
    oModule.AddTraceCharacteristics("S11", "XWidthAtYVal", ["-12"], ["Full"])
    oModule.AddTraceCharacteristics("S11", "XWidthAtYVal", ["-13"], ["Full"])
    direccion = read_data()['paths']['results'] + str(simID) + "/files/" + r"datosBW" + str(name) + ".csv"
    oModule.ExportTableToFile("S11", direccion, "Legend")


def creaDataTable(proj, name, simID):
    """Creates, generates and exports a data table report in Ansys HFSS

    Args:
        proj (Ansys project object ): objeto que representa el proyecto de Ansys HFSS una vez abierto
        name (str): complement of the file name, usually the iteration and particle. e.g _0_0
        simID (str): simulation id
    """
    oDesign = proj.SetActiveDesign(read_data()['values']['design_name'])
    oModule = oDesign.GetModule("ReportSetup")
    oModule.CreateReport(
        "Variables Table 1", "Far Fields", "Data Table", "Setup1 : LastAdaptive", ["Context:=", "phi0"], [
            "Theta:=",
            ["All"],
            "Phi:=",
            ["All"],
        ], ["Y Component:=", ["variables"]], []
    )
    direccion = read_data()['paths']['results'] + str(simID) + "/files/" + r"datosTabla" + str(name) + ".csv"
    oModule.ExportToFile("Variables Table 1", direccion)
