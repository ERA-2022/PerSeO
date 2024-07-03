# -*- coding: utf-8 -*-
"""
This module defines a Data Base Manager (DBManager) class that manages the operations of reading, writing and updating data by saving them in a CSV file for storing the results of the optimizations made.

Classes:
    DBManager
"""

import os.path as path
import pandas as pd
from .commands import read_data


class DBManager:
    """A class to manage database operations for optimization data.

    Attributes:
        df(pd.DataFrame | None): The DataFrame to hold simulation data.
        simulation_ID(str): simulation ID
    Methods:
        def load_df(): Loads the DataFrame from a CSV file if it exists, otherwise creates an empty DataFrame with predefined columns.
        save_data_to_plot(self, data_to_plot: dict, iteration: int, particle_id: str): Saves data to a CSV file for plotting purposes, this file is located in ./results/{particle_id}/files/Derivative_{iteration}_{particle_id}.csv
        fill_df(self, data_struct: dict): Adds new data to the DataFrame and saves it in a CSV file, this file is located in ./results/output.csv
    """

    def __init__(self, simulation_ID: str):
        """Creates an instance of the DBManager class taking into account a simulation ID

        Args:
            simulation_ID (str): simulation ID
        """
        self.simulation_ID = simulation_ID
        self.df = None

    def load_df(self):
        """Loads the DataFrame from a CSV file if it exists, otherwise creates an empty DataFrame with predefined columns.
        """
        if path.exists(read_data()['paths']['results'] + "output.csv"):
            self.df = pd.read_csv(read_data()['paths']['results'] + "output.csv", header=0)
        else:

            column_names = [
                "sim_id", "created_at", "elapsed_time", "sim_type", "category", "sub_category", "sim_setup", "pbest",
                "gbest", "best_particle_id", "best_particle", "iteration"
            ]

            self.df = pd.DataFrame(columns=column_names)

            self.df['sim_id'] = self.df['sim_id'].astype('object')
            self.df['created_at'] = self.df['created_at'].astype('datetime64')
            self.df['elapsed_time'] = self.df['elapsed_time'].astype(str)
            self.df['sim_type'] = self.df['sim_type'].astype(str)
            self.df['category'] = self.df['category'].astype(str)
            self.df['sub_category'] = self.df['sub_category'].astype(str)
            self.df['sim_setup'] = self.df['sim_setup'].astype('object')
            self.df['pbest'] = self.df['pbest'].astype('float64')
            self.df['gbest'] = self.df['gbest'].astype('float64')
            self.df['best_particle_id'] = self.df['best_particle_id'].astype('int64')
            self.df['iteration'] = self.df['iteration'].astype('int64')

    def save_data_to_plot(self, data_to_plot: dict, iteration: int, particle_id: str):
        """Saves data to a CSV file for plotting purposes, this file is located in ./results/{particle_id}/files/Derivative_{iteration}_{particle_id}.csv

        Args:
            data_to_plot (dict): The data to be saved.
            iteration (int): The current iteration number.
            particle_id (str): The ID of the particle.
        """
        df = pd.DataFrame.from_dict(data_to_plot, orient='index').transpose()
        df.to_csv(
            read_data()['paths']['results'] + str(self.simulation_ID) + "/files/" + r"Derivative_" + str(iteration) +
            "_" + str(particle_id) + ".csv",
            index=False,
            sep=','
        )

    def fill_df(self, data_struct: dict):
        """Adds new data to the DataFrame and saves it in a CSV file, this file is located in ./results/output.csv

        Args:
            data_struct (dict): The data structure containing the new data to be added, it is recommended that this structure contain the following keys and that all its values are text strings: sim_id, created_at, elapsed_time, sim_type, category, sub_category, sim_setup, pbest, gbest, best_particle_id, best_particle, iteration
        """
        output = pd.DataFrame()
        output = output.append(data_struct, ignore_index=True)

        df = pd.concat([self.df, output])

        df.to_csv(read_data()['paths']['results'] + "output.csv", index=False, sep=',')
