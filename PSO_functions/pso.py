#  -*- coding: utf-8 -*-
"""
Authors: German Chaparro, Jorge Cardenas,Oscar Restrepo, Sergio Mora, Jhon Vera, and Jaime Angel
Year: 2022
"""
# import os
# import importlib
# import matplotlib.pyplot as plt
# from scipy import stats
# from scipy import integrate
# from sklearn.metrics import mean_squared_error
# from PSO import fitness_func as fit
from numpy.core.records import array
from PSO_core.commands import read_data
import PSO_core.messages as msg
import numpy as np
from numpy.random import seed
from numpy.random import randn


class Particle:
    """
    Particle class enabling the creation of multiple and dynamic number of particles.
    """
    id_ = 0
    values_array = []

    def __init__(self, id):
        self.id_ = id

    def random_array(self, array_size):
        self.values_array = np.array(np.random.random_sample(array_size))

    def fill_zeros_array(self, array_size):
        self.values_array = np.zeros(array_size)

    def reset_xParticles_id_counter(self):
        self.id_ = 0


class Swarm:

    phiv = 0.9

    particles = []  # array with all particles part of the swarm
    x_particles = []  # array with all particles part of the swarm
    best_index = 0  # best integer describing the index corresponding the best particle in
    # particles array
    vmax = []
    velocidades = []
    gbest = 0  # global  best
    pbest = []
    pg = []
    variables_number = 0

    def __init__(self, particles_number, variables_number, var_max, var_min):
        # swarm variables
        self.particles_number = particles_number
        self.variables_number = variables_number

        # Set variations

        self.var_max = np.array(var_max)
        self.var_min = np.array(var_min)
        self.particles = []
        self.velocidades = np.zeros([read_data()['values']['particles'], read_data()['values']['n_var']])
        self.pbest = np.zeros(read_data()['values']['particles'])
        self.pg = np.zeros(read_data()['values']['n_var'])

    """Create particles swarm"""

    def create(self):

        self.particles = [Particle(i) for i in range(self.particles_number)]
        self.x_particles = [Particle(i) for i in range(self.particles_number)]
        print(msg.CREATED_PARTICLES + str(len(self.particles)))

        interval_array = np.array(self.var_max) - np.array(self.var_min)
        self.vmax = interval_array * 0.6

        for particle in self.particles:
            # Generate random array for each particle
            particle.random_array(self.variables_number)
            # Scale the random values
            particle.values_array = particle.values_array * (self.var_max - self.var_min) + self.var_min

            #  if particle.values_array[2] < particle.values_array[1]:

            #      random = np.random.random_sample()
            #      máximo = particle.values_array[1]-0.1
            #      particle.values_array[2] = random*(máximo-self.var_min[2]) + self.var_min[2]

    def nuevas_particulas(self, particulas_ant, pi_best, pg, vel_anterior, iteration):
        #      # Partículas => xi(t-1)
        #      # pi => individual optimal position!?
        #      #  x son partículas que vienen definidas desde la creación del enjambre
        #      #  Solo se van actualizando en el transcurso de las iteraciones

        [
            item.fill_zeros_array(read_data()['values']['n_var']) for item in self.x_particles
        ]  # llenar de ceros las partículas x

        vel = np.zeros([read_data()['values']['particles'],
                        read_data()['values']['n_var']])  # llenar de ceros la variable velocidad

        # Cambio dinámico de la inercia
        phi = 0.85 * self.phiv**(iteration - 0.15)  # 0.8 y 1
        phi1 = 2.0  # valores que se pueden revisar. Seguir el valor el mejor fit propio
        phi2 = 2.1  # esto va valores componen self-knowledge.  seguir el mejor fit global
        damping = 0.7  # este damping se utiliza cando las partículas tocan los limites máximos y mínimos.

        for i in range(read_data()['values']['particles']):

            rand = np.random.random()  # valores entre 0 y 1
            particula_anterior = particulas_ant[i]

            for idx, dimension in enumerate(particula_anterior.values_array):
                """
                Calcula la velocidad de la partícula i, dada su pi, pg y su velocidad
                 y posición anterior

                 pi => una partícula especifica
                pbest=> su fitness value

                 pg => cualquier partícula con la mejor solución
                 gbest=> global bets

                 vi => velocidad anterior
                """
                """lo importante es la relación entre phi1 y phi2 , si es grande la velocidad de convergencia es alta
                si la relación es pequeña, la velocidad es baja"""

                # # # inercia +  atracción a la mejor posición de la partícula i +  atracción a la mejor posición global
                # # #

                vel[i][idx] = phi * (vel_anterior[i][idx]) + phi1 * rand * ((pi_best[i].values_array)[idx] - dimension) + \
                     phi2 * rand * (pg[idx] - dimension)

                # Limiting velocity when too large
                if np.abs(vel[i][idx]) > self.vmax[idx]:
                    signo = np.sign(vel[i][idx])
                    vel[i][idx] = self.vmax[idx] * signo

                # Calculating new particles
                self.x_particles[i].values_array[idx] = (particulas_ant[i].values_array[idx] + vel[i][idx]).round(
                    decimals=3, out=None
                )  # #  xi(t-1)+vi(
                """In this part we apply a bounce technique in the wall defined
                by the limits of max and min values for dimensions"""
                if self.x_particles[i].values_array[idx] > self.var_max[idx]:

                    vel[i][idx] = vel[i][idx] * damping

                    self.x_particles[i].values_array[idx] = (self.var_max[idx] - np.abs(vel[i][idx])).round(
                        decimals=3, out=None
                    )  # #  xi(t-1)+vi(t)

                elif self.x_particles[i].values_array[idx] < self.var_min[idx]:

                    vel[i][idx] = vel[i][idx] * damping

                    self.x_particles[i].values_array[idx] = (self.var_min[idx] + np.abs(vel[i][idx])).round(
                        decimals=3, out=None
                    )  # #  xi(t-1)+vi(t)

                else:
                    self.x_particles[i].values_array[idx] = (particulas_ant[i].values_array[idx] + vel[i][idx]).round(
                        decimals=3, out=None
                    )  # #  xi(t-1)+vi(

                # This sections is used to force a=B*2
                # if idx==global_.A_dimension_index+1:
                #   self.x_particles[i].values_array[idx] = (self.x_particles[i].values_array[idx-1])*0.5

            #  PENDIENTE -> SOLO PARA HÍBRIDOS
            #  if i>0:
            #      relation = self.drilling_relation( self.x_particles[i].values_array, self.x_particles[i].values_array[global_.A_dimension_index])
            #      print(relation)

        return self.x_particles, vel

    def drilling_relation(self, dimension, height):
        relation = (height / 2) * 1 / dimension
        return relation

    def get_particle_best_fit(self, pi):
        index_pg = np.argmin(self.pbest)  # toma el indice del particle best entre todas las particulas
        self.best_index = index_pg
        print(msg.GET_BEST_PARTICLE_PG + str(pi[index_pg].values_array))
        self.pg = pi[index_pg].values_array  # seleccionar la mejor posición-partícula del array de particulas
        self.gbest = np.min(self.pbest)  # best global fitness
        return index_pg
