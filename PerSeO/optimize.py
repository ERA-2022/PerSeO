# -*- coding: utf-8 -*-
"""
Authors: German Chaparro, Jorge Cardenas,Oscar Restrepo, Sergio Mora, Jhon Vera, and Jaime Angel
Year: 2022
"""
import os
import logging
import json
import numpy as np
from datetime import datetime

from . import messages as msg
from . import commands
from . import pso as pso
from . import simulate as simulate
from . import dataManagement as db

from .commands import read_data


def main(fun):
    """It starts the optimization process taking into account the information previously configured in the ./src/data.json file and a cost function passed as a parameter, here the PSO optimization algorithm will be executed taking into account the simulation of the models generated by it in Ansys HFSS.

    Args:
        fun (function(dataReports: dict)): fitness/cost function to be used by the PSO, it must receive as a parameter a dictionary with the names of the reports generated in Ansys HFSS, where the access key will be the name of the report and the associated value will be the data obtained.
    """
    graph = False
    if commands.Y_N_question(msg.REQUEST_DRAW_GRAPHIC) == msg.YES:
        graph = True

    addOp = {"type": True, "graph": graph}

    start_time = datetime.today()
    commands.update_data("info", "ID", commands.setSimID())
    commands.update_data("paths", "files", read_data()['paths']['results'] + read_data()['info']['ID'] + "/files/")
    commands.update_data("paths", "figures", read_data()['paths']['results'] + read_data()['info']['ID'] + "/figures/")
    commands.make_directory(read_data()['info']['ID'], read_data()['paths']['results'])
    commands.make_directory("", read_data()['paths']['files'])
    commands.make_directory("", read_data()['paths']['figures'])
    commands.clear_screen()
    logging.basicConfig(
        filename=read_data()['paths']['src'] + "control.log", force=True, encoding='utf-8', level=logging.INFO
    )
    logging.basicConfig(format='%(asctime)s %(message)s')
    logging.info(start_time)
    logging.info(msg.SIM_ID + str(read_data()['info']['ID']))
    db_manager = db.DBManager(read_data()['info']['ID'])
    db_manager.load_df()


    logging.info(msg.STARTED)
    swarm = set_Swarm()

    for index in range(len(swarm.particles)):
        particle = swarm.particles[index]
        print(msg.SIM_ID + read_data()['info']['ID'])
        logging.info(msg.INITIAL_PARTICLE + str(particle.id_) + str(particle.values_array))

        simulate.create_sim_file(particle.values_array, 0, particle.id_)
        logging.info(msg.SIM_FILE_OK)
        logging.info(msg.SIM_PARTICLE_START + str(particle.id_))
        simulate.run_simulation_hfss()
        sim_results = simulate.read_simulation_results(0, particle.id_, addOp['graph'])
        fit = fun(sim_results)
        swarm.pbest[particle.id_] = fit
        logging.info(msg.FITNESS_VALS + str(fit))

    elapsed = commands.get_elapsed_time(start_time)

    logging.info(msg.TIME_ELAPSED + str(elapsed))

    best_index = swarm.get_particle_best_fit(swarm.particles)

    logging.info(msg.PBEST + str(swarm.pbest))
    logging.info(msg.GBEST + str(swarm.gbest))
    logging.info(msg.PGVALUE + str(swarm.pg))
    logging.info(msg.BEST_PARTICLE_INDEX + str(best_index) + '\n')

    info = read_data()['info']

    data_to_store = {
        "sim_id": info['ID'],
        "created_at": start_time,
        "elapsed_time": elapsed,
        "sim_type": "Full simulation",
        "category": info['category'],
        "sub_category": info['sub_category'],
        "sim_setup": json.dumps(simulate.get_simulation_params()),
        "pbest": json.dumps(swarm.pbest.tolist()),
        "gbest": swarm.gbest,
        "best_particle_id": best_index,
        "best_particle": json.dumps(swarm.particles[best_index].values_array.tolist()),
        "iteration": 0
    }

    db_manager.load_df()
    db_manager.fill_df(data_to_store)

    
    logging.info(msg.START_ITERATIONS)
    run_iterations(read_data()['values']['iterations'], swarm, db_manager, fun, addOp)
    
    logging.info(msg.FINISHED)


def set_Swarm():
    """Returns the instance of a swarm with its initialized particles.

    Returns:
        Swarm: Instance of a swarm with its initialized particles
    """
    swarm = pso.Swarm(
        read_data()['values']['particles'],
        read_data()['values']['n_var'],
        read_data()['values']['max'],
        read_data()['values']['min']
    )
    swarm.create()
    logging.info(msg.PARTICLES_CREATED)
    return swarm


def run_iterations(iterations: int, swarm: pso.Swarm, db_manager: db.DBManager, fun, addOp: dict):
    """Execution of optimization process using PSO taking into account iterations, initialized swarm, database, cost function and additional options

    Args:
        iterations (int): Total number of iterations to be executed by the PSO
        swarm (PerSeO.pso.Swarm): initialized swarm
        db_manager (PerSeO.db.DBManager): Instance of DBManager
        fun (function(dataReports: dict)): fitness/cost function to be used by the PSO, it must receive as a parameter a dictionary with the names of the reports generated in Ansys HFSS, where the access key will be the name of the report and the associated value will be the data obtained.
        addOp (dict): dictionary with two keywords, the first, type, will have a boolean value associated with it which indicates whether to simulate the particles in Ansys HFSS, the second, graph, will also have a boolean value associated with it which indicates whether to graph the reports. example: {"type": True, "graph": false}
    """

    pi_best = swarm.particles.copy()  # list of initial particles

    for i in range(iterations):
        print(msg.NUM_ITERATIONS + str(iterations))
        print(msg.CURRENT_ITERATION + str(i))

        logging.info(msg.ITERATION + str(i))
        logging.info(msg.CALC_NEW_PARTICLES)

        # previous_particles is a copy of the Particle array belonging to the swarm instance
        previous_particles = []
        previous_particles = swarm.particles.copy()
        logging.info(msg.CALC_VEL_AND_POS)

        # the swarm object is in charge of creating the new particles, which are actually updates of the previous particles
        # x -> particle arrays that are being updated
        # previous_particles -> array of initial/current particles
        # pg -> best position found for any particle
        # v -> velocity array
        x, v = swarm.calculate_new_particles(previous_particles, pi_best, swarm.pg, swarm.velocities, i)
        # the original particles are updated with the new updated particles

        for index_, particle in enumerate(x):
            swarm.particles[index_].values_array = particle.values_array

        swarm.velocities = np.copy(v)  # swarm velocities are updated
        logging.info(msg.SIM_NEW_PARTICLE + "\n")

        # iterate over each swarm particle and simulate the model in Ansys HFSS if necessary.
        for index in range(len(swarm.particles)):
            particle = swarm.particles[index]
            start_time = commands.start_timing()

            logging.info(msg.PARTICLE + str(particle.id_) + ':' + str(particle.values_array))

            #Prepare simulation intermediate file

            simulate.create_sim_file(particle.values_array, i + 1, particle.id_)

            logging.info(msg.SIM_FILE_OK)

            #start simulation
            logging.info(msg.SIM_PARTICLE_START + str(particle.id_))

            if addOp["type"]:
                simulate.run_simulation_hfss()
                s_type = "Full simulation"
            else:
                s_type = "Fitness function test"

            #get simulation results
            sim_results = simulate.read_simulation_results(i + 1, particle.id_, addOp["graph"])
            
            #Calculate fitness values for every particle in current iteration
            fit = fun(sim_results)

            logging.info(msg.FITNESS_VALS + str(fit))
            logging.info(msg.ITERATION + str(i + 1) + '\n')

            #if current particle is the best in current iteration
            #sort pbest
            if fit < swarm.pbest[index]:
                swarm.pbest[index] = fit
                pi_best[index] = swarm.particles[index]  # swarm particles is updated before with new particle

        # After each iteration we end up with pbest, pi, these values come from the iteration 0
        if np.min(swarm.pbest) < swarm.gbest:
            swarm.gbest = np.min(swarm.pbest)
            swarm.pg = pi_best[np.argmin(swarm.pbest)].values_array

        best_index = np.argmin(swarm.pbest)

        logging.info(msg.PBEST + str(swarm.pbest))
        logging.info(msg.GBEST + str(swarm.gbest))
        logging.info("pi_best  = " + str(particle.values_array))

        elapsed = commands.get_elapsed_time(start_time)

        logging.info(msg.TIME_ELAPSED + elapsed)

        info = read_data()['info']

        data_to_store = {
            "sim_id": info['ID'],
            "created_at": start_time,
            "elapsed_time": elapsed,
            "sim_type": s_type,
            "category": info['category'],
            "sub_category": info['sub_category'],
            "sim_setup": json.dumps(simulate.get_simulation_params()),
            "pbest": json.dumps(swarm.pbest.tolist()),
            "gbest": swarm.gbest,
            "best_particle_id": best_index,
            "best_particle": json.dumps(swarm.particles[best_index].values_array.tolist()),
            "iteration": i + 1
        }

        db_manager.load_df()
        db_manager.fill_df(data_to_store)

    # Closing of the iterative cycle
    print(msg.GLOBAL_MIN_VAL + str(swarm.gbest))
    logging.info(msg.GLOBAL_MIN_VAL + str(swarm.gbest))


def prepare_simulation_file(particle, id):
    """Creates the simulation file that Ansys HFSS will run given a particle and its id

    Args:
        particle (ndarray): Particle value, commonly associated with the array of values containing the dimensions of the model in Ansys HFSS.
        id (str): particle id
    """
    simulate.create_sim_file(particle, 0, id + 1)


def only_fit(fun):
    """It starts the optimization process taking into account the information previously configured in the file ./src/data.json, a cost function passed as parameter, the reports of a previously executed optimization and the ID of the optimization. Here the PSO optimization algorithm will be run with previously obtained data, since the models will not be simulated in Ansys HFSS.

    Args:
        fun (function(dataReports: dict)): fitness/cost function to be used by the PSO, it must receive as a parameter a dictionary with the names of the reports previously generated by Ansys HFSS, where the access key will be the name of the report and the associated value will be the data obtained.
    """
    reports_exist = False
    while not reports_exist:
        id_for_read = input(msg.REQUEST_ID)
        if not os.path.isdir(read_data()['paths']['results'] + id_for_read) or id_for_read == "":
            if commands.Y_N_question(msg.INVALID_ID_ERR) == msg.NO:
                break
        else:
            reports_exist = True

    if reports_exist:
        graph = False
        if commands.Y_N_question(msg.REQUEST_DRAW_GRAPHIC) == msg.YES:
            graph = True
        start_time = datetime.today()
        addOp = {"type": False, "graph": graph}
        commands.update_data("info", "ID", id_for_read)
        commands.update_data("paths", "files", read_data()['paths']['results'] + read_data()['info']['ID'] + "/files/")
        commands.update_data(
            "paths", "figures",
            read_data()['paths']['results'] + read_data()['info']['ID'] + "/figures/"
        )
        commands.make_directory(read_data()['info']['ID'], read_data()['paths']['results'])
        commands.make_directory("", read_data()['paths']['files'])
        commands.make_directory("", read_data()['paths']['figures'])
        commands.clear_screen()
        logging.basicConfig(
            filename=read_data()['paths']['src'] + "control.log", force=True, encoding='utf-8', level=logging.INFO
        )
        logging.basicConfig(format='%(asctime)s %(message)s')
        logging.info(start_time)
        logging.info(msg.SIM_ID + str(read_data()['info']['ID']))
        db_manager = db.DBManager(read_data()['info']['ID'])
        db_manager.load_df()


        logging.info(msg.STARTED)
        swarm = set_Swarm()

        for index in range(len(swarm.particles)):
            particle = swarm.particles[index]
            print(msg.SIM_ID + read_data()['info']['ID'])
            logging.info(msg.INITIAL_PARTICLE + str(particle.id_) + str(particle.values_array))

            sim_results = simulate.read_simulation_results(0, particle.id_, addOp["graph"])
            fit = fun(sim_results)
            swarm.pbest[particle.id_] = fit
            logging.info(msg.FITNESS_VALS + str(fit))

        elapsed = commands.get_elapsed_time(start_time)

        logging.info(msg.TIME_ELAPSED + str(elapsed))

        best_index = swarm.get_particle_best_fit(swarm.particles)

        logging.info(msg.PBEST + str(swarm.pbest))
        logging.info(msg.GBEST + str(swarm.gbest))
        logging.info(msg.PGVALUE + str(swarm.pg))
        logging.info(msg.BEST_PARTICLE_INDEX + str(best_index) + '\n')

        info = read_data()['info']

        data_to_store = {
            "sim_id": info['ID'],
            "created_at": start_time,
            "elapsed_time": elapsed,
            "sim_type": "Fitness function test",
            "category": info['category'],
            "sub_category": info['sub_category'],
            "sim_setup": json.dumps(simulate.get_simulation_params()),
            "pbest": json.dumps(swarm.pbest.tolist()),
            "gbest": swarm.gbest,
            "best_particle_id": best_index,
            "best_particle": json.dumps(swarm.particles[best_index].values_array.tolist()),
            "iteration": 0
        }

        db_manager.load_df()
        db_manager.fill_df(data_to_store)


        logging.info(msg.START_ITERATIONS)
        run_iterations(read_data()['values']['iterations'], swarm, db_manager, fun, addOp)

        logging.info(msg.FINISHED)
