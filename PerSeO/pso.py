#  -*- coding: utf-8 -*-
"""
Authors: German Chaparro, Jorge Cardenas,Oscar Restrepo, Sergio Mora, Jhon Vera, and Jaime Angel
Year: 2022
"""
from .commands import read_data
from . import messages as msg
import numpy as np


class Particle:
    """Represents a particle in the PSO algorithm.

    Attributes:
        id_(int): identifier
        values_array(ndarray): Array with the numerical values that the particle has

    Methods:
        random_array(array_size: int):
            Assigns to the values_array attribute a Numpy array (ndarray) of random values between 0 and 1, the number of array elements will be determined by the argument passed in the function.
        fill_zeros_array(array_size: int):
            Assigns to the values_array attribute a Numpy array (ndarray), the number of array elements will be determined by the argument passed in the function and each element will be zero.
        reset_xParticles_id_counter():
            Assigns 0 to the class variable id_.
    """
    id_ = 0
    values_array = []

    def __init__(self, id: int):
        """Initializes a new particle

        Args:
            id (int): identifier
        """
        self.id_ = id

    def random_array(self, array_size: int):
        """Assigns to the values_array attribute a Numpy array (ndarray) of random values between 0 and 1, the number of array elements will be determined by the argument passed in the function.

        Args:
            array_size (int): _description_
        """
        self.values_array = np.array(np.random.random_sample(array_size))

    def fill_zeros_array(self, array_size: int):
        """Assigns to the values_array attribute a Numpy array (ndarray), the number of array elements will be determined by the argument passed in the function and each element will be zero.

        Args:
            array_size (int): _description_
        """
        self.values_array = np.zeros(array_size)

    def reset_xParticles_id_counter(self):
        """Assigns 0 to the class variable id_.
        """
        self.id_ = 0


class Swarm:
    """Represents a swarm of particles in the PSO algorithm.

    Attributes:
        phiv(float): Swarm inertia coefficient
        particles(list): List of all particles that are part of the swarm
        x_particles(list): list to calculate the new particles  (internal use)
        best_index(int): Index of the best particle in the particle list
        vmax(list): List of maximum particle velocities.
        velocities(ndarray): Matrix of current particle velocities.
        gbest(float): Best overall value found by the swarm
        pbest(ndarray): Matrix of the best personal/local values of the particles.
        pg(ndarray): Matrix of the best global positions found by the swarm.
        variables_number(int): Number of variables defining each particle (In the interface provided by PerSeO it is associated to the array of dimensions of the Ansys HFSS model).
        var_max(ndarray): Maximum values that a particle can take
        var_min(ndarray): Minimum values that a particle can take
    Methods:
        create(): Initializes all swarm particles, generating them randomly.
        calculate_new_particles(self, previous_particles, pi_best, pg, vel_anterior, iteration): Generate new particles based on previous particles, personal and global best values, previous velocities and current iteration. At the end it returns a tuple of two elements, the first one is a list with the new calculated particles and the second one is a ndarray with the new calculated velocities.
        drilling_relation(self, dimension, height): Calculate a drilling ratio. ((height / 2) * 1 / dimension)
        get_particle_best_fit(self, pi): Obtains the best particle fit among all particles.
    """
    phiv = 0.9

    particles = []  # array with all particles part of the swarm
    x_particles = []  # array with all particles part of the swarm
    best_index = 0  # best integer describing the index corresponding the best particle in
    # particles array
    vmax = []
    velocities = []
    gbest = 0  # global  best
    pbest = []
    pg = []
    variables_number = 0

    def __init__(self, particles_number: int, variables_number: int, var_max: list | np.ndarray, var_min: list | np.ndarray):
        """Initializes a new swarm

        Args:
            particles_number (int): Number of particles that the swarm will have
            variables_number (int): Number of variables defining each particle (In the interface provided by PerSeO it is associated to the array of dimensions of the Ansys HFSS model).
            var_max (list | ndarray): Maximum values that a particle can take
            var_min (list | ndarray): Minimum values that a particle can take
        """
        # swarm variables
        self.particles_number = particles_number
        self.variables_number = variables_number

        # Set variations

        self.var_max = np.array(var_max)
        self.var_min = np.array(var_min)
        self.particles = []
        self.velocities = np.zeros([read_data()['values']['particles'], read_data()['values']['n_var']])
        self.pbest = np.zeros(read_data()['values']['particles'])
        self.pg = np.zeros(read_data()['values']['n_var'])

    
    def create(self):
        """Initializes all swarm particles, generating them randomly.
        """
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
            #      maximum = particle.values_array[1]-0.1
            #      particle.values_array[2] = random*(maximum-self.var_min[2]) + self.var_min[2]

    def calculate_new_particles(self, previous_particles: list, pi_best: list, pg: np.ndarray, vel_anterior: np.ndarray, iteration: int):
        """Generate new particles based on previous particles, personal and global best values, previous velocities and current iteration. At the end it returns a tuple of two elements, the first one is a list with the new calculated particles and the second one is a ndarray with the new calculated velocities.

        Args:
            previous_particles (list[Particle]): List of previous particles
            pi_best (list[Particle]): Better personal/local values
            pg (ndarray): Better global values
            vel_anterior (ndarray): previous speeds
            iteration (int): current iteration

        Returns:
        tuple(list[Particle], ndArray): Returns a tuple with two elements, the first is a list with the new calculated particles, and the other is a ndarray with the new calculated velocities.
        """
        [
            item.fill_zeros_array(read_data()['values']['n_var']) for item in self.x_particles
        ]  # fill the x-particles with zeros

        vel = np.zeros([read_data()['values']['particles'],
                        read_data()['values']['n_var']])  # fill the velocity variable with zeros

        # Dynamic change of inertia
        phi = 0.85 * self.phiv**(iteration - 0.15)  # 0.8 y 1
        phi1 = 2.0  # values that can be reviewed. Follow the value of your own best fit
        phi2 = 2.1  # this goes values make up self-knowledge. follow the best global fit
        damping = 0.7  # This damping is used when the particles touch the maximum and minimum limits.

        for i in range(read_data()['values']['particles']):

            rand = np.random.random()  # values between 0 and 1
            previous_particle = previous_particles[i]

            for idx, dimension in enumerate(previous_particle.values_array):
                """
                Calculate the velocity of particle i, given its pi, pg, and its previous velocity and position.

                pi => specific particle
                pbest=> its fitness value

                 pg => any particle with the best solution
                 gbest=> global bets

                 vi => previous speed

                 the important thing is the ratio between phi1 and phi2 , if it is large, the convergence speed is high, if the ratio is small, the speed is low.
                
                inertia + attraction to best position of particle i + attraction to best global position
                """

                vel[i][idx] = phi * (vel_anterior[i][idx]) + phi1 * rand * ((pi_best[i].values_array)[idx] - dimension) + \
                     phi2 * rand * (pg[idx] - dimension)

                # Limiting velocity when too large
                if np.abs(vel[i][idx]) > self.vmax[idx]:
                    signo = np.sign(vel[i][idx])
                    vel[i][idx] = self.vmax[idx] * signo

                # Calculating new particles
                self.x_particles[i].values_array[idx] = (previous_particles[i].values_array[idx] + vel[i][idx]).round(
                    decimals=3, out=None
                )  # #  xi(t-1)+vi(t)
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
                    self.x_particles[i].values_array[idx] = (previous_particles[i].values_array[idx] + vel[i][idx]).round(
                        decimals=3, out=None
                    )  # #  xi(t-1)+vi(

                # This sections is used to force a=B*2
                # if idx==global_.A_dimension_index+1:
                #   self.x_particles[i].values_array[idx] = (self.x_particles[i].values_array[idx-1])*0.5

            #  PENDING -> ONLY FOR HYBRIDS
            #  if i>0:
            #      relation = self.drilling_relation( self.x_particles[i].values_array, self.x_particles[i].values_array[global_.A_dimension_index])
            #      print(relation)

        return self.x_particles, vel

    def drilling_relation(self, dimension: float, height: float):
        """Calculate a drilling ratio. ((height / 2) * 1 / dimension)

        Args:
            dimension (float): Model size
            height (float): Model height

        Returns:
            float:  drilling ratio
        """
        relation = (height / 2) * 1 / dimension
        return relation

    def get_particle_best_fit(self, pi: list):
        """Obtains the best particle fit among all particles.

        Args:
            pi (list[Particle]): list of current particles

        Returns:
            int: Best particle index.
        """
        index_pg = np.argmin(self.pbest)  # Take the index of the best particle in the swarm.
        self.best_index = index_pg
        print(msg.GET_BEST_PARTICLE_PG + str(pi[index_pg].values_array))
        self.pg = pi[index_pg].values_array  # select the best particle-position of the particle array
        self.gbest = np.min(self.pbest)  # best global fitness
        return index_pg
