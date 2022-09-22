# -*- coding: utf-8 -*-
#import os
#import sys
#from scipy.sparse import data
import logging
import numpy as np
import json
from datetime import datetime
import os

import PSO_core.messages as msg
from PSO_core import commands
from PSO_core.commands import read_data

import PSO_functions.pso as pso
import PSO_functions.simulate as simulate
import PSO_functions.dataManagement as db

def main(fun):
    graph = False
    if commands.Y_N_question("¿Desea graficar los resutados de los reportes solicitados?") == "S":
        graph = True

    addOp = {"type":True, "graph":graph}

    start_time = datetime.today()
    commands.update_data("info","ID",commands.setSimID())
    commands.update_data("paths","files",read_data()['paths']['results']+read_data()['info']['ID']+"/files/")
    commands.update_data("paths","figures", read_data()['paths']['results']+read_data()['info']['ID']+"/figures/")
    commands.make_directory(read_data()['info']['ID'], read_data()['paths']['results'])
    commands.make_directory("",read_data()['paths']['files'])
    commands.make_directory("",read_data()['paths']['figures'])
    commands.clear_screen()
    logging.basicConfig(filename= read_data()['paths']['src']+"control.log", force=True, encoding='utf-8', level=logging.INFO)
    logging.basicConfig(format='%(asctime)s %(message)s')
    logging.info(start_time)
    logging.info(msg.SIM_ID+ str(read_data()['info']['ID']))
    db_manager = db.DBManager(read_data()['info']['ID'])
    db_manager.load_df()

    logging.info(msg.STARTED)
    swarm = set_Swarm() #initialize swarm

    for index in range(len(swarm.particles)):
        particle = swarm.particles[index]
        print(msg.SIM_ID+read_data()['info']['ID'])
        logging.info(msg.INITIAL_PARTICLE + str(particle.id_) + str(particle.values_array))
        
        simulate.create_sim_file(particle.values_array,0,particle.id_)
        logging.info(msg.SIM_FILE_OK)
        logging.info(msg.SIM_PARTICLE_START + str(particle.id_))
        simulate.run_simulation_hfss()
        sim_results = simulate.read_simulation_results(0,particle.id_,addOp['graph'])
        fit = fun(sim_results)
        swarm.pbest[particle.id_] = fit
        logging.info(msg.FITNESS_VALS+str(fit))

    elapsed = commands.get_elapsed_time(start_time)
    
    logging.info(msg.TIME_ELAPSED+str(elapsed))

    best_index=swarm.get_particle_best_fit(swarm.particles)

    logging.info(msg.PBEST + str(swarm.pbest))
    logging.info(msg.GBEST + str(swarm.gbest)) #swarm.gbest comes from get_particle_best_fit
    logging.info(msg.PGVALUE + str(swarm.pg))
    logging.info(msg.BEST_PARTICLE_INDEX + str(best_index)+'\n')

    info = read_data()['info']

    data_to_store={
        "sim_id":info['ID'],
        "created_at":start_time,
        "elapced_time":elapsed,
        "sim_type":"Full simulation",
        "category":info['category'],
        "sub_category":info['sub_category'],
        "sim_setup":json.dumps(simulate.get_simulation_params()),
        "pbest":json.dumps(swarm.pbest.tolist()),
        "gbest":swarm.gbest,
        "best_particle_id":best_index,
        "best_particle": json.dumps(swarm.particles[best_index].values_array.tolist()),
        "iteration":0
    }

    db_manager.load_df()
    db_manager.fill_df(data_to_store)

    ### Iterations
    logging.info(msg.START_ITERATIONS)
    run_iterations(read_data()['values']['iterations'],swarm,db_manager,fun,addOp)
    ### Finished process
    logging.info(msg.FINISHED)

def set_Swarm():
    swarm = pso.Swarm(read_data()['values']['particles'], read_data()['values']['n_var'], read_data()['values']['max'], read_data()['values']['min'])
    swarm.create()
    logging.info(msg.PARTICLES_CREATED)
    return swarm

def run_iterations(iteraciones, swarm:pso.Swarm, db_manager:db.DBManager,fun, addOp:dict):
  
    pi_best = swarm.particles.copy()#array initial particles
    
    for i in range(iteraciones):
        print(msg.NUM_ITERATIONS+str(iteraciones))
        print("current it:"+str(i))

        logging.info(msg.ITERATION + str(i))
        logging.info("Calculando nuevas particulas...")
       
       ### particulas anterior es una copia del objeto arreglo de Particulas
       ### que es propiedad del objeto Swarm
        particulas_anterior = []
        particulas_anterior  = swarm.particles.copy() #Array de particulas
        logging.info("Calculando las velocidades y posiciones siguientes..")

        ### el objeto swarm se ocupa de crear las particulas nuevas
        ### que realmente son actualizaciones de las particulas anteriores
        #array Particulas que se van actualizando
        #array Particulas iniciales
        #pg -> mejor posocion encontrada para cualquier particula
        #arreglo de velocidades
        x , v = swarm.nuevas_particulas(particulas_anterior, pi_best, swarm.pg, swarm.velocidades,i)
        ### se actualizan las particulas originales con las nuevas particulas actualizadas

        for index_, particle in enumerate(x):

            swarm.particles[index_].values_array = particle.values_array
            #swarm.particles  = x.copy() #aqui se está copiando un objeto

        swarm.velocidades = np.copy(v) #aquí un arreglo de vectores
        logging.info(msg.SIM_NEW_PARTICLE+"\n")

        #Array valores se ocupa de recibir los valores de fitness de cada particula en la 
        #actual iteraciòn
        valores = np.zeros(read_data()['values']['particles'])
        
        ### se itera sobre cada particula y se simula
        # [print(i.id_) for i in swarm.particles]

        for index in range(len(swarm.particles)):
            particle = swarm.particles[index]
            start_time = commands.start_timing()

                 
            logging.info(msg.PARTICLE+ str(particle.id_)+':' + str(particle.values_array))

            #Prepare simulation intermediate file

            simulate.create_sim_file(particle.values_array,i+1,particle.id_)

            logging.info(msg.SIM_FILE_OK)

            #start simulation
            logging.info(msg.SIM_PARTICLE_START + str(particle.id_))

            if addOp["type"]:
                simulate.run_simulation_hfss()
                s_type = "Full simulation"
            else:
                s_type = "Fitness function test"

            #get simulation results
            sim_results = simulate.read_simulation_results(i+1,particle.id_,addOp["graph"])
            fit = fun(sim_results)
            
            logging.info(msg.FITNESS_VALS+str(fit))
            logging.info(msg.ITERATION+str(i+1)+'\n')

            #Calculate fitness values for every particle in current iteration
            #if current particle is the best in current iteration
            #sort pbest
            if fit < swarm.pbest[index]:
                swarm.pbest[index] = fit
                pi_best[index] = swarm.particles[index] #swarm particles is updated before with new particle

        ## After each iteration we end up with pbest, pi
        #these values come from the iteration 0
        if np.min(swarm.pbest) < swarm.gbest:

            swarm.gbest = np.min(swarm.pbest) #swarm.gbest comes from get_particle_best_fit
            swarm.pg = pi_best[np.argmin(swarm.pbest)].values_array
        
        best_index=np.argmin(swarm.pbest)


        logging.info(msg.PBEST+ str(swarm.pbest))
        logging.info(msg.GBEST+ str(swarm.gbest))
        logging.info("pi_best  = "+ str(particle.values_array))
            
        elapsed=commands.get_elapsed_time(start_time)

        logging.info(msg.TIME_ELAPSED+elapsed)

        info = read_data()['info']

        data_to_store={
            "sim_id":info['ID'],
            "created_at":start_time,
            "elapced_time":elapsed,
            "sim_type":s_type,
            "category":info['category'],
            "sub_category":info['sub_category'],
            "sim_setup":json.dumps(simulate.get_simulation_params()),
            "pbest":json.dumps(swarm.pbest.tolist()),
            "gbest":swarm.gbest,
            "best_particle_id":best_index,
            "best_particle": json.dumps(swarm.particles[best_index].values_array.tolist()),
            "iteration":i+1
        }
        
        db_manager.load_df()
        db_manager.fill_df(data_to_store)

    ###Cierre del ciclo
    print("Minimo global encontrado: "+str(swarm.gbest))
    logging.info(msg.GLOBAL_MIN_VAL+str(swarm.gbest))

def prepare_simulation_file(particle, id):
    simulate.create_sim_file(particle,0,id +1)

def only_fit(fun):
    graph = False
    if commands.Y_N_question("¿Desea graficar los resutados de los reportes solicitados?") == "S":
        graph = True
    start_time = datetime.today()
    reports_exist = False
    while not reports_exist:
        id_for_read = input("Digite el ID de la simulación previamente ejecutada: ")
        if not os.path.isdir(read_data()['paths']['results']+id_for_read):
            msj = "Error, ID no valido o existente!!\n¿Desea digitar otro ID?"
            if commands.Y_N_question(msj) == "N":
                break
        else:
            reports_exist = True

    if reports_exist:
        addOp = {"type":False, "graph":graph}
        commands.update_data("info","ID", id_for_read)
        commands.update_data("paths","files",read_data()['paths']['results']+read_data()['info']['ID']+"/files/")
        commands.update_data("paths","figures", read_data()['paths']['results']+read_data()['info']['ID']+"/figures/")
        commands.make_directory(read_data()['info']['ID'], read_data()['paths']['results'])
        commands.make_directory("",read_data()['paths']['files'])
        commands.make_directory("",read_data()['paths']['figures'])
        commands.clear_screen()
        logging.basicConfig(filename= read_data()['paths']['src']+"control.log", force=True, encoding='utf-8', level=logging.INFO)
        logging.basicConfig(format='%(asctime)s %(message)s')
        logging.info(start_time)
        logging.info(msg.SIM_ID+ str(read_data()['info']['ID']))
        db_manager = db.DBManager(read_data()['info']['ID'])
        db_manager.load_df()

        logging.info(msg.STARTED)
        swarm = set_Swarm() #initialize swarm

        for index in range(len(swarm.particles)):
            particle = swarm.particles[index]
            print(msg.SIM_ID+read_data()['info']['ID'])
            logging.info(msg.INITIAL_PARTICLE + str(particle.id_) + str(particle.values_array))
            
            sim_results = simulate.read_simulation_results(0,particle.id_,addOp["graph"])
            fit = fun(sim_results)
            swarm.pbest[particle.id_] = fit
            logging.info(msg.FITNESS_VALS+str(fit))

        elapsed = commands.get_elapsed_time(start_time)
        
        logging.info(msg.TIME_ELAPSED+str(elapsed))

        best_index=swarm.get_particle_best_fit(swarm.particles)

        logging.info(msg.PBEST + str(swarm.pbest))
        logging.info(msg.GBEST + str(swarm.gbest)) #swarm.gbest comes from get_particle_best_fit
        logging.info(msg.PGVALUE + str(swarm.pg))
        logging.info(msg.BEST_PARTICLE_INDEX + str(best_index)+'\n')

        info = read_data()['info']

        data_to_store={
            "sim_id":info['ID'],
            "created_at":start_time,
            "elapced_time":elapsed,
            "sim_type":"Fitness function test",
            "category":info['category'],
            "sub_category":info['sub_category'],
            "sim_setup":json.dumps(simulate.get_simulation_params()),
            "pbest":json.dumps(swarm.pbest.tolist()),
            "gbest":swarm.gbest,
            "best_particle_id":best_index,
            "best_particle": json.dumps(swarm.particles[best_index].values_array.tolist()),
            "iteration":0
        }

        db_manager.load_df()
        db_manager.fill_df(data_to_store)

        ### Iterations
        logging.info(msg.START_ITERATIONS)
        run_iterations(read_data()['values']['iterations'],swarm,db_manager,fun,addOp)
        ### Finished process
        logging.info(msg.FINISHED)
    