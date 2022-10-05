# -*- coding: utf-8 -*-
"""
	Authors: German Chaparro, Jorge Cardenas,Oscar Restrepo, Sergio Mora, Jhon Vera, and Jaime Angel
	Year: 2022
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
def creaSmn(proj,nombre,simID,m,n):
	oDesign = proj.SetActiveDesign(read_data()['values']['design_name'])
	oModule = oDesign.GetModule("ReportSetup")
	oModule.CreateReport("S"+m+n, "Modal Solution Data", "Rectangular Plot", "Setup1 : Sweep", 
    	[
    		"Domain:="		, "Sweep"
    	], 
    	[
    		"Freq:="		, ["All"],
    	], 
    	[
    		"X Component:="		, "Freq",
    		"Y Component:="		, ["dB(S("+m+","+n+"))"]
    	], [])

	oModule.ExportToFile("S"+m+n, read_data()['paths']['results']+str(simID)+"/files/"+r"datosS"+str(m)+str(n)+str(nombre)+".csv")

def creaZmn(proj,nombre,simID,m,n):
	oDesign = proj.SetActiveDesign(read_data()['values']['design_name'])
	oModule = oDesign.GetModule("ReportSetup")
	oModule.CreateReport("Z"+m+n, "Modal Solution Data", "Rectangular Plot", "Setup1 : Sweep", 
    	[
    		"Domain:="		, "Sweep"
    	], 
    	[
    		"Freq:="		, ["All"],
    	], 
    	[
    		"X Component:="		, "Freq",
    		"Y Component:="		, ["re(Z("+m+","+n+"))","im(Z("+m+","+n+"))"]
    	], [])

	oModule.ExportToFile("Z"+m+n, read_data()['paths']['results']+str(simID)+"/files/"+r"datosZ"+str(m)+str(n)+str(nombre)+".csv")

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
	
	oModule.ExportToFile("Amplitud Imbalance", read_data()['paths']['results']+str(simID)+"/files/"+r"amp_imb"+str(nombre)+".csv")

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

	oModule.ExportToFile("Phase Imbalance", read_data()['paths']['results']+str(simID)+"/files/"+r"pha_imb"+str(nombre)+".csv")

#UNDERNEATH THE COMMANDS TO GENERATE THE VSWR, GAIN, BW AND DATA TABLE PARAMETERS.
def creaVSWR(proj,nombre,simID,port):
    oDesign = proj.SetActiveDesign(read_data()['values']['design_name'])
    oModule = oDesign.GetModule("ReportSetup")

    oModule.CreateReport("VSWR("+port+")", "Modal Solution Data", "Rectangular Plot", "Setup1 : Sweep", 
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
		    "Y Component:="		, ["VSWR("+port+")"]
	    ], [])
    direccion = read_data()['paths']['results']+str(simID)+"/files/"+r"datosVSWR("+str(port)+")"+str(nombre)+".csv"
    oModule.ExportToFile("VSWR("+str(port)+")",direccion)

def creaGain(proj,nombre,simID,angulo):
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
   
    direccion = read_data()['paths']['results']+str(simID)+"/files/"+r"datosGananciaPhi"+str(angulo)+str(nombre)+".csv"
    oModule.ExportToFile("Gain Phi "+ str(angulo), direccion)

def creaBW(proj,nombre,simID):
    oDesign = proj.SetActiveDesign(read_data()['values']['design_name'])
    oModule = oDesign.GetModule("ReportSetup")
    oModule.AddTraceCharacteristics("S11", "XWidthAtYVal", ["-12"], ["Full"])
    oModule.AddTraceCharacteristics("S11", "XWidthAtYVal", ["-13"], ["Full"])
    direccion = read_data()['paths']['results']+str(simID)+"/files/"+r"datosBW"+str(nombre)+".csv"
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
    direccion = read_data()['paths']['results']+str(simID)+"/files/"+r"datosTabla"+str(nombre)+".csv"
    oModule.ExportToFile("Variables Table 1", direccion)