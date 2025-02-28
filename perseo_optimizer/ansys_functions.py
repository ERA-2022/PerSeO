# -*- coding: utf-8 -*-
"""
This module is designed to interact with Ansys HFSS software. Among its functions are the modification of arrays and variables in an Ansys HFSS design and the generation of different reports such as Smn, Zmn, VSWR among others.

Methods:
    addVariable(proj, name, value)
    
    changeVariable(proj, name, value)
    
    addArray(proj, name, value)
    
    changeArray(proj, name, value)
    
    createsSmn(proj, name, simID, m, n)
    
    createsZmn(proj, name, simID, m, n)
    
    createsAmpImb(proj, name, simID)
    
    createsPhaseImb(proj, name, simID)
    
    createsVSWR(proj, name, simID, port)
    
    createsGain(proj, name, simID, angle)
    
    createsBW(proj, name, simID)
    
    createsDataTable(proj, name, simID)
"""

from .commands import read_data


def addVariable(proj, name, value):
    """Adds a variable to the Ansys HFSS design, it is suggested that the value be accompanied by the units of measurement.

    Args:
        proj (Ansys project object ): object representing the Ansys HFSS project once opened
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


def changeVariable(proj, name, value):
    """Modify a variable to the Ansys HFSS design, it is suggested that the value be accompanied by the units of measurement.

    Args:
        proj (Ansys project object ): object representing the Ansys HFSS project once opened
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


def addArray(proj, name, value):
    """Adds a variable type array to the Ansys HFSS design, it is suggested that the value be accompanied by the units of measurement.

    Args:
        proj (Ansys project object ): object representing the Ansys HFSS project once opened
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


def changeArray(proj, name, value):
    """Modify a variable type array to the Ansys HFSS design, it is suggested that the value be accompanied by the units of measurement.

    Args:
        proj (Ansys project object ): object representing the Ansys HFSS project once opened
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


def createsSmn(proj, name, simID, m, n):
    """Creates, generates and exports Smn report in Ansys HFSS

    Args:
        proj (Ansys project object ): object representing the Ansys HFSS project once opened
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


def createsZmn(proj, name, simID, m, n):
    """Creates, generates and exports Zmn report in Ansys HFSS

    Args:
        proj (Ansys project object ): object representing the Ansys HFSS project once opened
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


def createsAmpImb(proj, name, simID):
    """Creates, generates and exports AmpImb report in Ansys HFSS

    Args:
        proj (Ansys project object ): object representing the Ansys HFSS project once opened
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


def createsPhaseImb(proj, name, simID):
    """Creates, generates and exports PhaseImb report in Ansys HFSS

    Args:
        proj (Ansys project object ): object representing the Ansys HFSS project once opened
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


def createsVSWR(proj, name, simID, port):
    """Creates, generates and exports VSWR report in Ansys HFSS

    Args:
        proj (Ansys project object ): object representing the Ansys HFSS project once opened
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
    save_path = read_data(
    )['paths']['results'] + str(simID) + "/files/" + r"datosVSWR(" + str(port) + ")" + str(name) + ".csv"
    oModule.ExportToFile("VSWR(" + str(port) + ")", save_path)


def createsGain(proj, name, simID, angle):
    """Creates, generates and exports gain report in Ansys HFSS

    Args:
        proj (Ansys project object ): object representing the Ansys HFSS project once opened
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

    save_path = read_data(
    )['paths']['results'] + str(simID) + "/files/" + r"datosGananciaPhi" + str(angle) + str(name) + ".csv"
    oModule.ExportToFile("Gain Phi " + str(angle), save_path)


def createsBW(proj, name, simID):
    """Creates, generates and exports BW report in Ansys HFSS

    Args:
        proj (Ansys project object ): object representing the Ansys HFSS project once opened
        name (str): complement of the file name, usually the iteration and particle. e.g _0_0
        simID (str): simulation id
    """
    oDesign = proj.SetActiveDesign(read_data()['values']['design_name'])
    oModule = oDesign.GetModule("ReportSetup")
    oModule.AddTraceCharacteristics("S11", "XWidthAtYVal", ["-12"], ["Full"])
    oModule.AddTraceCharacteristics("S11", "XWidthAtYVal", ["-13"], ["Full"])
    save_path = read_data()['paths']['results'] + str(simID) + "/files/" + r"datosBW" + str(name) + ".csv"
    oModule.ExportTableToFile("S11", save_path, "Legend")


def createsDataTable(proj, name, simID):
    """Creates, generates and exports a data table report in Ansys HFSS

    Args:
        proj (Ansys project object ): object representing the Ansys HFSS project once opened
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
    save_path = read_data()['paths']['results'] + str(simID) + "/files/" + r"datosTabla" + str(name) + ".csv"
    oModule.ExportToFile("Variables Table 1", save_path)
