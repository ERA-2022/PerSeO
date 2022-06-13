# -*- coding: utf-8 -*-

"""
pso.py
Functions related to implementation of PSO algorithm.


"""

from numpy.core.records import array
import temp.global_ as global_
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from numpy.random import seed
from numpy.random import randn

from sklearn.metrics import mean_squared_error

class Particle:
    """
    Particle class enabling the creation of multiple and dynamic number of particles.
    """
    id_ = 0
    values_array = []

    def __init__(self, id ):
        self.id_=id


    def random_array(self, array_size):
        self.values_array = np.array(np.random.random_sample(array_size))

    def fill_zeros_array(self, array_size):
       self.values_array = np.zeros(array_size)
    
    def reset_xParticles_id_counter(self):
        self.id_ = 0


class Swarm:
    
    particles=[] # array with all particles part of the swar
    x_particles=[] # array with all particles part of the swar
    best_index=0 #best integer describing the index corresponding the best particle in 
                #particles array
    vmax = []
    velocidades = []
    gbest = 0  #global  best
    pbest =[]
    pg = []

    def __init__(self, particles_number, variables_number, var_max, var_min):
        #swarm variables
        self.particles_number = particles_number
        self.variables_number = variables_number

        #Set variations
        self.var_max = np.array(var_max)
        self.var_min = np.array(var_min)
        self.particles = []
        self.velocidades = np.zeros([global_.n_particulas,global_.n_variables])
        self.pbest = np.zeros(global_.n_particulas)
        self.pg = np.zeros(global_.n_variables)

    """Create particles swarm"""
    def create(self):
        
        self.particles = [Particle(i) for i in range(self.particles_number )]
        self.x_particles = [Particle(i) for i in range(self.particles_number  )]
        print("particulas creadas:"+str(len(self.particles)))

        self.vmax = (np.array(self.var_max) - np.array(self.var_min) )/2

        for particle in self.particles:
            #Generate random array for each particle
            particle.random_array(self.variables_number)
            #Scale the random values
            particle.values_array = particle.values_array*(self.var_max-self.var_min) + self.var_min

    def velocidad(self,i, pi, pg, vi, particle):
        """ 
        Calcula la velocidad de la particula i, dada su pi, pg y su velocidad
        y posicion anterior 

        pi => una particula especifica
        pbest=> su fitness value

        pg => cualquier particula con la mejor solucion
        gbest=> global bets

        vi => velocidad anterior
        """
        
        phi1 = 0.8 #valores que se pueden revisar
        phi2 = 1.5 #esto va valores componen self-knowledge
        phiv = 0.65 # inicial 0.5

        rand1 = np.random.random() #valores entre 0 y 1
        rand2 = np.random.random()

        ###inercia +  atraccion a la mejor posicion de la particula i +  atraccion a la mejor posición global
       
        vel = phiv * vi + phi1 * rand1 * (pi.values_array - particle.values_array) + \
            phi2 * rand2 * (pg - particle.values_array)

        for i in range(global_.n_variables):
            
            if np.abs(vel[i]) > self.vmax[i]:
                signo = np.sign(vel[i])
                vel[i] =  signo * self.vmax[i]
                
        return vel
    
    

    def nuevas_particulas(self,particulas, pi, pg, vel_anterior):
        #Particulas => xi(t-1)
        #pi => particulas iniciales
        # x son particulas que vienen definidas desde la creacion del enjambre
        # Solo se van actualizando en el transcurso de las iteraciones

        [item.fill_zeros_array(global_.n_variables) for item in self.x_particles]#llenar de ceros las particulas x

        vel = np.zeros([global_.n_particulas, global_.n_variables])#llenar de ceros la variable velocidad
        
        for i in range(global_.n_particulas):

            print(i)
            print( self.x_particles[i].values_array )


            vel[i] = self.velocidad(i , pi[i], pg, vel_anterior[i] , particulas[i])

            print("vel " + str(i)+" "+str(vel[i]))
            
            self.x_particles[i].values_array = particulas[i].values_array + vel[i] ## xi(t-1)+vi(t)
            
            for j in range(global_.n_variables):
                if (self.x_particles[i].values_array)[j] > self.var_max[j]:
                    (self.x_particles[i].values_array)[j] = self.var_max[j]
                elif (self.x_particles[i].values_array)[j] < self.var_min[j]:
                    (self.x_particles[i].values_array)[j] = self.var_min[j]
                    
            if(self.x_particles[i].values_array)[1] < (self.x_particles[i].values_array)[2]:
                (self.x_particles[i].values_array)[2] =(self.x_particles[i].values_array)[1]-0.1
            
        
        
        return self.x_particles,vel

    def get_particle_best_fit(self, pi):
        index_pg = np.argmin(self.pbest) #toma el indice del particle best entre todas las particulas
        self.best_index = index_pg
        print("get particle best pg="+str(pi[index_pg].values_array))
        self.pg = pi[index_pg].values_array # seleccionar la mejor posicion-particula del array de particulas
        self.gbest = np.min(self.pbest)  #best global fitness 
        return index_pg
