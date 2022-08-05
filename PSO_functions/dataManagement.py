# -*- coding: utf-8 -*-

"""dataManagement.py
   Author: Jorge Cardenas

   1. Simulation data logging in CSV Files
   2. Simulation data Retrieval

   Future developments:
   1. Local or remote data storage
"""

#import csv
#import os
from PSO_core.commands import read_data
import pandas as pd
import os.path as path

class DBManager:

   file=None
   df = None
   def __init__(self, simulation_ID ):
        self.simulation_ID=simulation_ID
   
   def load_df(self):

      if path.exists(read_data()['paths']['results']+"output.csv"):
         self.df = pd.read_csv(read_data()['paths']['results']+"output.csv", header=0)
      else:
            
         column_names = ["sim_id", "created_at", "elapced_time", "sim_type", "category", "sub_category", "sim_setup", "pbest","gbest","best_particle_id","best_particle","iteration"]
         
         self.df = pd.DataFrame(columns = column_names)

         self.df['sim_id'] = self.df['sim_id'].astype( 'object')
         self.df['created_at'] = self.df['created_at'].astype( 'datetime64')
         self.df['elapced_time'] = self.df['elapced_time'].astype(str)
         self.df['sim_type'] = self.df['sim_type'].astype(str)
         self.df['category'] = self.df['category'].astype(str)
         self.df['sub_category'] = self.df['sub_category'].astype(str)  
         self.df['sim_setup'] = self.df['sim_setup'].astype( 'object')
         self.df['pbest'] = self.df['pbest'].astype( 'float64')
         self.df['gbest'] = self.df['gbest'].astype( 'float64')
         self.df['best_particle_id'] = self.df['best_particle_id'].astype( 'int64')
         self.df['iteration'] = self.df['iteration'].astype( 'int64')
         

   def save_data_to_plot(self,data_to_plot,iteration,particle_id):
      
      df=pd.DataFrame.from_dict(data_to_plot,orient='index').transpose()
      df.to_csv(read_data()['paths']['results']+str(self.simulation_ID)+"/files/"+r"Derivative_"+str(iteration)+"_"+str(particle_id)+".csv", index=False,sep=',')


   def fill_df(self,data_struct):
      output = pd.DataFrame()
      output = output.append(data_struct, ignore_index=True)
      
      df = pd.concat([self.df, output])
      
      df.to_csv(read_data()['paths']['results']+"output.csv", index=False,sep=',')