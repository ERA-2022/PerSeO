# -*- coding: utf-8 -*-
"""
Created on 30/07/2020

@author: Daniel Montofré and Oscar Restrepo

Modify on 15/06/2022

by: Jaime Angel
"""

from .commands import read_data

def agregaVariable(proj,nombre,valor):
        oDesign = proj.SetActiveDesign(read_data()['values']['design_name'])
        oDesign.ChangeProperty(
    	[
    		"NAME:AllTabs",
    		[
    			"NAME:LocalVariableTab",
    			[
    				"NAME:PropServers", 
    				"LocalVariables"
    			],
    			[
    				"NAME:NewProps",
    				[
    					"NAME:" + nombre,
    					"PropType:="		, "VariableProp",
    					"UserDef:="		, True,
    					"Value:="		, valor
    				]
    			]
    		]
    	])
    
def modificaVariable(proj,nombre,valor):
    oDesign = proj.SetActiveDesign(read_data()['values']['design_name'])
    oDesign.ChangeProperty(
    	[
    		"NAME:AllTabs",
    		[
    			"NAME:LocalVariableTab",
    			[
    				"NAME:PropServers", 
    				"LocalVariables"
    			],
    			[
    				"NAME:ChangedProps",
    				[
    					"NAME:"+ nombre ,
    					"Value:="		, valor
    				]
    			]
    		]
    	])
    
def agregaArreglo(proj,nombre,valor):
    oDesign = proj.SetActiveDesign(read_data()['values']['design_name'])
    oDesign.ChangeProperty(
    	[
    		"NAME:AllTabs",
    		[
    			"NAME:LocalVariableTab",
    			[
    				"NAME:PropServers", 
    				"LocalVariables"
    			],
    			[
    				"NAME:NewProps",
    				[
    					"NAME:" + nombre,
    					"PropType:="		, "VariableProp",
    					"UserDef:="		, True,
    					"Value:="		, valor
    				]
    			]
    		]
    	])

# modifica un arreglo del proyecto proj
# nombre y valor son strings
    
def modificaArreglo(proj,nombre,valor):
    oDesign = proj.SetActiveDesign(read_data()['values']['design_name'])
    oDesign.ChangeProperty(
    	[
    		"NAME:AllTabs",
    		[
    			"NAME:LocalVariableTab",
    			[
    				"NAME:PropServers", 
    				"LocalVariables"
    			],
    			[
    				"NAME:ChangedProps",
    				[
    					"NAME:"+ nombre,
    					"Value:="		, valor
    				]
    			]
    		]
    	])
    
#UNDERNEATH THE COMMANDS TO GENERATE THE S PARAMETERS ARE PRESENTED.
    
#Creating the S11 data
def creaS11(proj,nombre,simID):
    oDesign = proj.SetActiveDesign(read_data()['values']['design_name'])
    oModule = oDesign.GetModule("ReportSetup")
    oModule.CreateReport("S11", "Modal Solution Data", "Rectangular Plot", "Setup1 : Sweep", 
    	[
    		"Domain:="		, "Sweep"
    	], 
    	[
    		"Freq:="		, ["All"],
    	], 
    	[
    		"X Component:="		, "Freq",
    		"Y Component:="		, ["dB(S(1,1))"]
    	], [])

    oModule.ExportToFile("S11", read_data()['values']['results']+str(simID)+"/files/"+r"datosS11"+str(nombre)+".csv")

#Creating the S21 data
def creaS21(proj,nombre,simID):
    oDesign = proj.SetActiveDesign(read_data()['values']['design_name'])
    oModule = oDesign.GetModule("ReportSetup")
    oModule.CreateReport("S21", "Modal Solution Data", "Rectangular Plot", "Setup1 : Sweep", 
    	[
    		"Domain:="		, "Sweep"
    	], 
    	[
    		"Freq:="		, ["All"],
    	], 
    	[
    		"X Component:="		, "Freq",
    		"Y Component:="		, ["dB(S(2,1))"]
    	], [])
    oModule.ExportToFile("S21",read_data()['values']['results']+str(simID)+"/files/"+r"datosS21"+str(nombre)+".csv")

#Creating the S31 data
def creaS31(proj,nombre,simID):
    oDesign = proj.SetActiveDesign(read_data()['values']['design_name'])
    oModule = oDesign.GetModule("ReportSetup")
    oModule.CreateReport("S31", "Modal Solution Data", "Rectangular Plot", "Setup1 : Sweep", 
    	[
    		"Domain:="		, "Sweep"
    	], 
    	[
    		"Freq:="		, ["All"],
    	], 
    	[
    		"X Component:="		, "Freq",
    		"Y Component:="		, ["dB(S(3,1))"]
    	], [])
    oModule.ExportToFile("S31", read_data()['values']['results']+str(simID)+"/files/"+r"datosS31"+str(nombre)+".csv")

#Creating the S41 data
def creaS41(proj,nombre,simID):
    oDesign = proj.SetActiveDesign(read_data()['values']['design_name'])
    oModule = oDesign.GetModule("ReportSetup")
    oModule.CreateReport("S41", "Modal Solution Data", "Rectangular Plot", "Setup1 : Sweep", 
    	[
    		"Domain:="		, "Sweep"
    	], 
    	[
    		"Freq:="		, ["All"],
    	], 
    	[
    		"X Component:="		, "Freq",
    		"Y Component:="		, ["dB(S(4,1))"]
    	], [])
    oModule.ExportToFile("S41", read_data()['values']['results']+str(simID)+"/files/"+r"datosS41"+str(nombre)+".csv")

def creaAmpImb(proj,nombre,simID):
	
	oDesign = proj.SetActiveDesign(read_data()['values']['design_name'])
	oModule = oDesign.GetModule("ReportSetup")
	oModule.CreateReport("Amplitud Imbalance", "Modal Solution Data", "Rectangular Plot", "Setup1 : Sweep", 
	[
		"Domain:="		, "Sweep"
	], 
	[
		"Freq:="		, ["All"],
		"a:="			, ["Nominal"],
	], 
	[
		"X Component:="		, "Freq",
		"Y Component:="		, ["AmpImbalance"]
	], [])
	
	oModule.ExportToFile("Amplitud Imbalance", read_data()['values']['results']+str(simID)+"/files/"+r"amp_imb"+str(nombre)+".csv")

def creaPhaseImb(proj,nombre,simID):
	
	oDesign = proj.SetActiveDesign(read_data()['values']['design_name'])
	oModule = oDesign.GetModule("ReportSetup")
	oModule.CreateReport("Phase Imbalance", "Modal Solution Data", "Rectangular Plot", "Setup1 : Sweep", 
	[
		"Domain:="		, "Sweep"
	], 
	[
		"Freq:="		, ["All"],
	], 
	[
		"X Component:="		, "Freq",
		"Y Component:="		, ["PhaseImb"]
	], [])

	oModule.ExportToFile("Phase Imbalance", read_data()['values']['results']+str(simID)+"/files/"+r"pha_imb"+str(nombre)+".csv")

#UNDERNEATH THE COMMANDS TO GENERATE THE VSWR, GAIN, BW AND DATA TABLE PARAMETERS.
def creaVSWR(proj,nombre,simID):
    oDesign = proj.SetActiveDesign(read_data()['values']['design_name'])
    oModule = oDesign.GetModule("ReportSetup")

    oModule.CreateReport("VSWR", "Modal Solution Data", "Rectangular Plot", "Setup1 : Sweep", 
	    [  
    		"Domain:="		, "Sweep"
	    ], 
	    [
    		"Freq:="		, ["All"],
		    "frec:="		, ["Nominal"],
		    "t:="			, ["Nominal"]
	    ], 
	    [
		    "X Component:="		, "Freq",
		    "Y Component:="		, ["VSWR(1)"]
	    ], [])
    direccion = read_data()['values']['results']+str(simID)+"/files/"+r"datosVSWR"+str(nombre)+".csv"
    oModule.ExportToFile("VSWR",direccion)

def creaGain(proj, angulo, nombre,simID):
    oDesign = proj.SetActiveDesign(read_data()['values']['design_name'])
    oModule = oDesign.GetModule("ReportSetup")
    oModule.CreateReport("Gain Phi "+ str(angulo), 
                         "Far Fields", "Rectangular Plot", "Setup1 : Sweep", 
    	[
    		"Context:="		, "phi"+str(angulo)
    	], 
    	[
    		"Theta:="		, ["All"],
    		"Phi:="			, ["All"],
    		"Freq:="		, ["All"],
    		"frec:="		, ["Nominal"],
    		"t:="			, ["Nominal"]
    	], 
    	[
    		"X Component:="		, "Theta",
    		"Y Component:="		, ["GainTotal"]
    	], [])   
   
    direccion = read_data()['values']['results']+str(simID)+"/files/"+r"datosGanancia"+str(nombre)+".csv"
    oModule.ExportToFile("Gain Phi "+ str(angulo), direccion)

def creaBW(proj,nombre,simID):
    oDesign = proj.SetActiveDesign(read_data()['values']['design_name'])
    oModule = oDesign.GetModule("ReportSetup")
    oModule.AddTraceCharacteristics("S11", "XWidthAtYVal", ["-12"], ["Full"])
    oModule.AddTraceCharacteristics("S11", "XWidthAtYVal", ["-13"], ["Full"])
    direccion = read_data()['values']['results']+str(simID)+"/files/"+r"datosBW"+str(nombre)+".csv"
    oModule.ExportTableToFile("S11", direccion, "Legend")

def creaDataTable(proj,nombre,simID):
    oDesign = proj.SetActiveDesign(read_data()['values']['design_name'])
    oModule = oDesign.GetModule("ReportSetup")
    oModule.CreateReport("Variables Table 1", "Far Fields", "Data Table", "Setup1 : LastAdaptive", 
    	[
    		"Context:="		, "phi0"
    	], 
    	[
    		"Theta:="		, ["All"],
    		"Phi:="			, ["All"],
    
    	], 
    	[
    		"Y Component:="		, ["variables"]
    	], [])
    direccion = read_data()['values']['results']+str(simID)+"/files/"+r"datosTabla"+str(nombre)+".csv"
    oModule.ExportToFile("Variables Table 1", direccion)