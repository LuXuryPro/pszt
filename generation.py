#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import phenotype


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

    def step(self):
        """Do one step of generation including mutations, crossovers, and
        selection.
        TODO This will be overwriten by child class
        """
        self.calc_fitness()

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

        new_population = []
        for agent in self.population:
            for count in range(int(agent.get_fitness() *
                               self.number_of_individuals)):
                new_population.append(agent)
        self.population = new_population

        # Mutation
        i = 0
        while (i < self.population[0].get_fitness() *
                self.number_of_individuals/5 and
                i < (self.number_of_individuals - 1)):
            self.population[
                    random.randint(0, self.number_of_individuals - 1)
                    ].mutation()
            i += 1
        # Crossovers
        i = 0
        while (i < self.population[0].get_fitness() and
                i < self.number_of_individuals - 1):
            one = self.population[i]
            i += 1
            second = self.population[i]
            i += 1
            r = one.crossover(second)
            self.population.append(r['a'])
            self.population.append(r['b'])

        self.population = self.population[0:self.number_of_individuals]
