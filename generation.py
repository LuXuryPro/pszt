#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import phenotype
import ipdb


class Generation:
    def __init__(self, number_of_individuals, size_of_genotype):
        self.population = [phenotype.Phenotype(size=size_of_genotype)
                           for i in range(number_of_individuals)]
        self.num_iterations = 0
        self.number_of_individuals = number_of_individuals

    def __str__(self):
        s = "\n".join([str(x) for x in self.population])
        s = "Population: \n" + s
        return s

    def set_destination(self, destination_sum, destination_product):
        self.destination_sum = destination_sum
        self.destination_product = destination_product

    def calc_fitness(self):
        for individiual in self.population:
            individiual.calc_fitness_function(self.destination_sum,
                                              self.destination_product)
        s = 0
        m = 0

        # Sum all influences and get the biggest one - we will use it
        # in calc_influence
        for agent in self.population:
            s += agent.get_fitness()
            if m < agent.get_fitness():
                m = agent.get_fitness()

        for x in self.population:
            x.calc_influence(s, m, self.number_of_individuals)

        self.population.sort(key=lambda x: x.get_influence(), reverse=True)

    def mutation(self):
        i = 0
        while i < self.number_of_individuals*0.1:
            self.population[
                    random.randint(0, len(self.population) - 1)
                    ].mutation()
            i += 1

    def get_best(self):
        for individiual in self.population:
            individiual.calc_fitness_function(self.destination_sum,
                                              self.destination_product)
        self.population.sort(key=lambda x: x.get_fitness(), reverse=False)
        return self.population[0]

    def step(self):
        """Do one step of generation including mutations, crossovers, and
        selection.
        TODO This will be overwriten by child class
        """

        a = random.choice(self.population)
        b = random.choice(self.population)

        a.calc_fitness_function(self.destination_sum, self.destination_product)
        b.calc_fitness_function(self.destination_sum, self.destination_product)

        if a.get_fitness() < b.get_fitness():
            w = a
            l = b
        else:
            w = b
            l = a

        for bit in enumerate(w.genotype):
            if random.random() < 0.5:
                l.genotype[bit[0]] = bit[1]
            if random.random() < 0.4:
                l.genotype[bit[0]] ^= 1






