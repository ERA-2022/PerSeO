# -*- coding: utf-8 -*-
import logging
import os
from datetime import date
import numpy as np
import json
import sys

from scipy.sparse import data
from PSO import commands
import PSO_functions.simulate as simulate
from PSO_core.commands import read_data
import PSO_functions.pso as pso
import PSO_core.messages as msg
import PSO_functions.dataManagement as db

def main(fun):
    commands.update_data("info","ID",commands.setSimID())
    commands.update_data("paths","files",read_data()['paths']['results']+read_data()['info']['ID']+"/files/")
    commands.update_data("paths","figures", read_data()['paths']['results']+read_data()['info']['ID']+"/figures/")
    commands.make_directory(read_data()['info']['ID'], read_data()['paths']['results'])
    commands.make_directory("",read_data()['paths']['files'])
    commands.make_directory("",read_data()['paths']['figures'])
    logging.basicConfig(filename= read_data()['paths']['src']+"control.log", force=True, encoding='utf-8', level=logging.INFO)
    logging.basicConfig(format='%(asctime)s %(message)s')
    logging.info(date.today())
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
        s11 = simulate.read_simulation_results(0,particle.id_)
        fit = fun(s11)
        swarm.pbest[particle.id_] = fit
        logging.info(msg.FITNESS_VALS+str(fit))

    elapsed = commands.get_elapsed_time()
    
    logging.info(msg.TIME_ELAPSED+str(elapsed))

    best_index=swarm.get_particle_best_fit(swarm.particles)

    logging.info(msg.PBEST + str(swarm.pbest))
    logging.info(msg.GBEST + str(swarm.gbest)) #swarm.gbest comes from get_particle_best_fit
    logging.info(msg.PGVALUE + str(swarm.pg))
    logging.info(msg.BEST_PARTICLE_INDEX + str(best_index)+'\n')

    sim_results = {
        "elapsed_time": str(elapsed),
        "data_to_store": json.dumps(data_to_store)

    }

    data_to_store={
        "sim_id":read_data()['info']['ID'],
        "created_at":date.today(),
        "sim_setup":json.dumps(simulate.get_simulation_params()),
        "sim_results":json.dumps(sim_results),
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
    run_iterations(read_data()['values']['iterations'],swarm,fun)
    ### Finished process
    logging.info(msg.FINISHED)

def set_Swarm():
    swarm = pso.Swarm(read_data()['values']['particles'], read_data()['values']['n_var'], read_data()['values']['max'], read_data()['values']['min'])
    swarm.create()
    logging.info(msg.PARTICLES_CREATED)
    return swarm

def run_iterations(iteraciones, swarm, fun):
  
    pi_best = swarm.particles.copy()#array initial particles
    db_manager = db.DBManager(read_data()['info']['ID'])
    
    for i in range(iteraciones):
        print(msg.NUM_ITERATIONS+str(iteraciones))
        print("current it.:"+str(i))

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
            commands.start_timing()

                 
            logging.info(msg.PARTICLE+ str(particle.id_)+':' + str(particle.values_array))

            #Prepare simulation intermediate file

            simulate.create_sim_file(particle.values_array,i+1,particle.id_)

            logging.info(msg.SIM_FILE_OK)

            #start simulation
            logging.info(msg.SIM_PARTICLE_START + str(particle.id_))

            simulate.run_simulation_hfss()
            s11 = simulate.read_simulation_results(i+1,particle.id_)
            fit = fun(s11)
            #get simulation results
            #s11,s21,s31,s41, amp_imbalance = simulate.read_simulation_results(i+1,particle.id_)
            
            #fit
            # valores[index], data_to_store,derivative_array = pso.fitness([s11,s21,s31,s41,amp_imbalance],[i+1,particle.id_]) #get the index of the particle (geometry)
            # data_to_plot={
            #     "dy2_31":derivative_array[0],
            #     "x_31":derivative_array[1],
            #     "y2_21":derivative_array[2],
            #     "x_21":derivative_array[3]
            # }
    
            # db_manager.save_data_to_plot(data_to_plot,i+1,particle.id_)
            
            logging.info(msg.FITNESS_VALS+str(valores))
            logging.info(msg.ITERATION+str(i+1)+'\n')

            #Calculate fitness values for every particle in current iteration
            #if current particle is the best in current iteration
            #sort pbest
            if valores[index] < swarm.pbest[index]:
                swarm.pbest[index] = valores[index]
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
            
        elapsed=commands.get_elapsed_time()

        logging.info(msg.TIME_ELAPSED+elapsed)

        sim_results = {
            "elapsed_time": str(elapsed),
            "data_to_store": json.dumps(data_to_store)
        }

        data_to_store={
            "sim_id":read_data()['info']['ID'],
            "created_at":date.today(),
            "sim_setup":json.dumps(simulate.get_simulation_params()),
            "sim_results":json.dumps(sim_results),
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