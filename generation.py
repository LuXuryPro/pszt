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

    def step(self):
        """Do one step of generation including mutations, crossovers, and
        selection.
        TODO This will be overwriten by child class
        """
        self.calc_fitness()


        # select parents
        parents = []
        for parent in self.population:
            # roll dice
            dice = random.random()
            for agent in self.population:
                dice -= agent.get_influence()
                if dice <= 0:
                    parents.append(agent)
                    break

        assert(len(parents) == len(self.population))

        list_of_indices = range(self.number_of_individuals)

        assert(self.number_of_individuals % 2 == 0)

        childrens = []
        for pair in range(self.number_of_individuals/2):
            first = random.randint(0, len(list_of_indices) - 1)
            del list_of_indices[first]
            second = random.randint(0, len(list_of_indices) - 1)
            del list_of_indices[second]

            first_parent = parents[first]
            second_parent = parents[second]

            children = first_parent.crossover(second_parent)
            children['a'].mutation()
            children['b'].mutation()

            children['a'].calc_fitness_function(self.destination_sum, self.destination_product)
            children['b'].calc_fitness_function(self.destination_sum, self.destination_product)

            selector = []
            selector.append(first_parent)
            selector.append(second_parent)
            selector.append(children['a'])
            selector.append(children['b'])

            selector.sort(key=lambda x: x.get_fitness(), reverse=False)
            childrens.append(selector[0])
            childrens.append(selector[1])

        assert(len(childrens) == len(self.population))
        self.population = childrens
